"""
Algorithm execution service for running optimization algorithms via Modal.

All algorithm execution is now delegated to Modal cloud functions, which enforce
the same security constraints as the original Docker sandbox:
  - 30-second timeout, 512 MB memory, no network access.

Public API (function signatures, return types) is unchanged so that API routes
and Celery tasks do not need modification.
"""

import time
from typing import Dict, Any, Optional

from app.config import (
    ALGORITHM_REGISTRY,
    is_algorithm_available,
    get_algorithm_info,
    EXECUTION_TIMEOUT,
)
from app.core.utils import get_fitness_function


class AlgorithmExecutor:
    """
    Service class for executing optimization algorithms.

    Delegates execution to Modal cloud functions while preserving the original
    result format expected by API routes and Celery tasks.
    """

    def __init__(self):
        self.registry = ALGORITHM_REGISTRY

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run_algorithm(
        self,
        algorithm_name: str,
        problem: Dict[str, Any],
        params: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Run an optimization algorithm via Modal.

        Args:
            algorithm_name: Registry key (e.g. ``"genetic_algorithm"``).
            problem:        Problem definition dict (dimensions, bounds, etc.).
            params:         Algorithm-specific parameter overrides.

        Returns:
            Result dict with status, best_solution, convergence_curve, etc.
        """
        if algorithm_name not in self.registry:
            return self._create_error_result(
                algorithm_name,
                f"Unknown algorithm '{algorithm_name}'",
                "error",
            )

        if not is_algorithm_available(algorithm_name):
            algo_info = get_algorithm_info(algorithm_name)
            return self._create_not_implemented_result(algorithm_name, algo_info)

        # Fast pre-flight validation: check fitness function name / problem config
        # before incurring Modal cold-start cost.
        validation_error = self._validate_problem_preflight(algorithm_name, problem)
        if validation_error:
            return validation_error

        # Delegate execution to Modal
        try:
            result = self._execute_via_modal(algorithm_name, problem, params)
            return result
        except ValueError as exc:
            # Validation errors from Modal runner (bad algorithm name, missing fitness fn)
            return self._create_error_result(algorithm_name, str(exc), "error")
        except Exception as exc:
            # Classify Modal-specific exceptions for user-friendly messages
            exc_type = type(exc).__name__
            err_str = str(exc)
            if exc_type in ("FunctionTimeoutError", "TimeoutError") or "timeout" in err_str.lower():
                return self._create_error_result(
                    algorithm_name,
                    "Optimization exceeded the 30-second time limit. "
                    "Try reducing 'max_iterations' or 'population_size'.",
                    "timeout",
                )
            if exc_type in ("ExecutionError", "UserCodeException"):
                return self._create_error_result(
                    algorithm_name,
                    f"Algorithm execution failed in the sandbox: {err_str}",
                    "error",
                )
            return self._create_error_result(
                algorithm_name,
                f"Unexpected error during execution: {err_str}",
                "error",
            )

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _validate_problem_preflight(
        self,
        algorithm_name: str,
        problem: Dict[str, Any],
    ) -> Optional[Dict[str, Any]]:
        """
        Lightweight validation before calling Modal (avoids cold-start on bad input).
        Returns an error result dict on failure, or None on success.
        """
        problem_type = problem.get("problem_type")

        if problem_type == "knapsack":
            if not problem.get("items"):
                return self._create_error_result(
                    algorithm_name, "Knapsack problem requires 'items' list", "error"
                )

        elif problem_type == "tsp":
            cities = problem.get("cities", [])
            if len(cities) < 3:
                return self._create_error_result(
                    algorithm_name, "TSP problem requires at least 3 cities", "error"
                )

        else:
            fitness_fn_name = problem.get("fitness_function_name")
            if not fitness_fn_name:
                return self._create_error_result(
                    algorithm_name,
                    "Missing 'fitness_function_name' in problem definition",
                    "error",
                )
            try:
                get_fitness_function(fitness_fn_name)  # validate existence only
            except ValueError as exc:
                return self._create_error_result(algorithm_name, str(exc), "error")

        return None

    def _execute_via_modal(
        self,
        algorithm_name: str,
        problem: Dict[str, Any],
        params: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Dispatch the algorithm to Modal and translate the result.

        Uses Modal's synchronous `.remote()` API so that the existing
        synchronous callers (FastAPI routes, tests) do not need to change.
        """
        wall_start = time.time()

        # Merge registry defaults with caller-supplied params
        algo_info = get_algorithm_info(algorithm_name)
        merged_params = {**algo_info["default_params"], **params}

        # Look up the deployed Modal function by app/function name
        # (avoids importing modal_runner locally, which creates a disconnected app object)
        import modal
        _modal_run = modal.Function.lookup("optimizehub-executor", "run_algorithm")

        raw_result: dict = _modal_run.remote(algorithm_name, problem, merged_params)

        wall_time = time.time() - wall_start

        result: Dict[str, Any] = {
            "algorithm": raw_result.get("algorithm", algorithm_name),
            "status": "success",
            "best_solution": raw_result.get("best_solution"),
            "best_fitness": raw_result.get("best_fitness"),
            "convergence_curve": raw_result.get("convergence_curve", []),
            "params": raw_result.get("params", merged_params),
            "iterations_completed": len(raw_result.get("convergence_curve") or []),
            "execution_time": round(wall_time, 3),
            "error_message": None,
        }

        # Add problem-specific decoded context (knapsack items chosen, TSP route, etc.)
        from app.core.solution_decoder import add_problem_context_to_result
        result = add_problem_context_to_result(result, problem)

        return result

    # ------------------------------------------------------------------
    # Result factory helpers (unchanged from original)
    # ------------------------------------------------------------------

    def _create_not_implemented_result(
        self,
        algorithm_name: str,
        algorithm_info: Dict[str, Any],
    ) -> Dict[str, Any]:
        return {
            "algorithm": algorithm_info.get("display_name", algorithm_name),
            "status": "not_implemented",
            "best_solution": None,
            "best_fitness": None,
            "convergence_curve": None,
            "params": None,
            "iterations_completed": None,
            "execution_time": None,
            "error_message": (
                f"Algorithm '{algorithm_info.get('display_name', algorithm_name)}' "
                "is not yet implemented. Status: Coming Soon"
            ),
        }

    def _create_error_result(
        self,
        algorithm_name: str,
        error_message: str,
        status: str = "error",
    ) -> Dict[str, Any]:
        return {
            "algorithm": algorithm_name,
            "status": status,
            "best_solution": None,
            "best_fitness": None,
            "convergence_curve": None,
            "params": None,
            "iterations_completed": None,
            "execution_time": None,
            "error_message": error_message,
        }

    # ------------------------------------------------------------------
    # Algorithm info (unchanged)
    # ------------------------------------------------------------------

    def get_algorithm_list(self) -> Dict[str, Any]:
        algorithms = []
        for name, info in self.registry.items():
            algo_dict = {
                "name": name,
                "display_name": info["display_name"],
                "status": info["status"],
                "description": info["description"],
                "default_params": info["default_params"],
            }
            if "parameter_info" in info:
                algo_dict["parameter_info"] = info["parameter_info"]
            if "use_cases" in info:
                algo_dict["use_cases"] = info["use_cases"]
            algorithms.append(algo_dict)

        available_count = sum(1 for a in algorithms if a["status"] == "available")
        coming_soon_count = sum(1 for a in algorithms if a["status"] == "coming_soon")

        return {
            "total": len(algorithms),
            "available": available_count,
            "coming_soon": coming_soon_count,
            "algorithms": algorithms,
        }

    def get_algorithm_details(self, algorithm_name: str) -> Optional[Dict[str, Any]]:
        if algorithm_name not in self.registry:
            return None

        info = self.registry[algorithm_name]
        details = {
            "name": algorithm_name,
            "display_name": info["display_name"],
            "status": info["status"],
            "description": info["description"],
            "use_cases": info.get("use_cases", []),
            "default_params": info["default_params"],
            "parameter_info": info.get("parameter_info", {}),
            "implementation_status": (
                "Available for use"
                if info["status"] == "available"
                else "In development - Coming Soon"
            ),
        }
        if "characteristics" in info:
            details["characteristics"] = info["characteristics"]
        return details
