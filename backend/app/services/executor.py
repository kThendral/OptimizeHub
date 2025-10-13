"""
Algorithm execution service for running optimization algorithms.
"""
import time
import importlib
from typing import Dict, Any, Optional
from app.config import ALGORITHM_REGISTRY, is_algorithm_available, get_algorithm_info, EXECUTION_TIMEOUT
from app.core.utils import get_fitness_function, create_problem_dict


class AlgorithmExecutor:
    """
    Service class for executing optimization algorithms.

    Handles algorithm instantiation, execution, and result formatting.
    Gracefully handles both implemented and not-yet-implemented algorithms.
    """

    def __init__(self):
        """Initialize the algorithm executor."""
        self.registry = ALGORITHM_REGISTRY

    def run_algorithm(
        self,
        algorithm_name: str,
        problem: Dict[str, Any],
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Run an optimization algorithm.

        Args:
            algorithm_name: Name of the algorithm to run (e.g., 'particle_swarm')
            problem: Problem definition dictionary
            params: Algorithm-specific parameters

        Returns:
            Dictionary with results or error information
        """
        # Check if algorithm exists in registry
        if algorithm_name not in self.registry:
            return self._create_error_result(
                algorithm_name,
                f"Unknown algorithm '{algorithm_name}'",
                "error"
            )

        # Check if algorithm is implemented
        if not is_algorithm_available(algorithm_name):
            algorithm_info = get_algorithm_info(algorithm_name)
            return self._create_not_implemented_result(algorithm_name, algorithm_info)

        # Execute the algorithm
        try:
            result = self._execute_algorithm(algorithm_name, problem, params)
            return result
        except Exception as e:
            return self._create_error_result(
                algorithm_name,
                f"Execution error: {str(e)}",
                "error"
            )

    def _execute_algorithm(
        self,
        algorithm_name: str,
        problem: Dict[str, Any],
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Internal method to execute an available algorithm.

        Args:
            algorithm_name: Name of the algorithm
            problem: Problem definition
            params: Algorithm parameters

        Returns:
            Algorithm results dictionary
        """
        start_time = time.time()

        # Get algorithm info from registry
        algo_info = get_algorithm_info(algorithm_name)

        # Dynamically import the algorithm class
        module_path = algo_info['module']
        class_name = algo_info['class_name']

        try:
            module = importlib.import_module(module_path)
            algorithm_class = getattr(module, class_name)
        except (ImportError, AttributeError) as e:
            return self._create_error_result(
                algorithm_name,
                f"Failed to import algorithm: {str(e)}",
                "error"
            )

        # Get fitness function
        fitness_function_name = problem.get('fitness_function_name')
        if not fitness_function_name:
            return self._create_error_result(
                algorithm_name,
                "Missing 'fitness_function_name' in problem definition",
                "error"
            )

        try:
            fitness_function = get_fitness_function(fitness_function_name)
        except ValueError as e:
            return self._create_error_result(
                algorithm_name,
                str(e),
                "error"
            )

        # Create problem dictionary for algorithm
        problem_dict = create_problem_dict(
            dimensions=problem['dimensions'],
            bounds=problem['bounds'],
            fitness_function=fitness_function,
            objective=problem.get('objective', 'minimize')
        )

        # Merge default params with user-provided params
        default_params = algo_info['default_params'].copy()
        default_params.update(params)

        # Instantiate and run algorithm
        try:
            algorithm = algorithm_class(problem_dict, default_params)
            algorithm.initialize()
            algorithm.optimize()
            raw_results = algorithm.get_results()
        except Exception as e:
            return self._create_error_result(
                algorithm_name,
                f"Algorithm execution failed: {str(e)}",
                "error"
            )

        # Calculate execution time
        execution_time = time.time() - start_time

        # Check if execution timed out
        status = "timeout" if execution_time >= EXECUTION_TIMEOUT else "success"

        # Format results
        result = {
            'algorithm': raw_results.get('algorithm', class_name),
            'status': status,
            'best_solution': raw_results.get('best_solution'),
            'best_fitness': (
                raw_results['convergence_curve'][-1]
                if raw_results.get('convergence_curve')
                else None
            ),
            'convergence_curve': raw_results.get('convergence_curve'),
            'params': raw_results.get('params', default_params),
            'iterations_completed': len(raw_results.get('convergence_curve', [])),
            'execution_time': round(execution_time, 3),
            'error_message': None
        }

        return result

    def _create_not_implemented_result(
        self,
        algorithm_name: str,
        algorithm_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create a result for algorithms that are not yet implemented.

        Args:
            algorithm_name: Name of the algorithm
            algorithm_info: Algorithm information from registry

        Returns:
            Not implemented result dictionary
        """
        return {
            'algorithm': algorithm_info.get('display_name', algorithm_name),
            'status': 'not_implemented',
            'best_solution': None,
            'best_fitness': None,
            'convergence_curve': None,
            'params': None,
            'iterations_completed': None,
            'execution_time': None,
            'error_message': (
                f"Algorithm '{algorithm_info.get('display_name', algorithm_name)}' "
                f"is not yet implemented. Status: Coming Soon"
            )
        }

    def _create_error_result(
        self,
        algorithm_name: str,
        error_message: str,
        status: str = "error"
    ) -> Dict[str, Any]:
        """
        Create an error result.

        Args:
            algorithm_name: Name of the algorithm
            error_message: Error message
            status: Status string

        Returns:
            Error result dictionary
        """
        return {
            'algorithm': algorithm_name,
            'status': status,
            'best_solution': None,
            'best_fitness': None,
            'convergence_curve': None,
            'params': None,
            'iterations_completed': None,
            'execution_time': None,
            'error_message': error_message
        }

    def get_algorithm_list(self) -> Dict[str, Any]:
        """
        Get information about all algorithms.

        Returns:
            Dictionary with algorithm list and statistics
        """
        algorithms = []

        for name, info in self.registry.items():
            algo_dict = {
                'name': name,
                'display_name': info['display_name'],
                'status': info['status'],
                'description': info['description'],
                'default_params': info['default_params']
            }

            # Include parameter info if available
            if 'parameter_info' in info:
                algo_dict['parameter_info'] = info['parameter_info']

            # Include use cases if available
            if 'use_cases' in info:
                algo_dict['use_cases'] = info['use_cases']

            algorithms.append(algo_dict)

        # Count statuses
        available_count = sum(1 for a in algorithms if a['status'] == 'available')
        coming_soon_count = sum(1 for a in algorithms if a['status'] == 'coming_soon')

        return {
            'total': len(algorithms),
            'available': available_count,
            'coming_soon': coming_soon_count,
            'algorithms': algorithms
        }

    def get_algorithm_details(self, algorithm_name: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a specific algorithm.

        Args:
            algorithm_name: Name of the algorithm

        Returns:
            Algorithm details or None if not found
        """
        if algorithm_name not in self.registry:
            return None

        info = self.registry[algorithm_name]

        details = {
            'name': algorithm_name,
            'display_name': info['display_name'],
            'status': info['status'],
            'description': info['description'],
            'use_cases': info.get('use_cases', []),
            'default_params': info['default_params'],
            'parameter_info': info.get('parameter_info', {}),
            'implementation_status': (
                'Available for use' if info['status'] == 'available'
                else 'In development - Coming Soon'
            )
        }

        # Include characteristics if available
        if 'characteristics' in info:
            details['characteristics'] = info['characteristics']

        return details
