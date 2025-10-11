"""
Helper utility functions for optimization algorithms.
"""
import numpy as np
from typing import Callable, Dict, Any, List, Tuple


# ==============================================================================
# Benchmark Fitness Functions
# ==============================================================================

def sphere(x: np.ndarray) -> float:
    """
    Sphere function: f(x) = sum(x_i^2)
    Global minimum: f(0, ..., 0) = 0
    Domain: typically [-5.12, 5.12]
    """
    return float(np.sum(x ** 2))


def rastrigin(x: np.ndarray) -> float:
    """
    Rastrigin function: highly multimodal function
    f(x) = 10*n + sum(x_i^2 - 10*cos(2*pi*x_i))
    Global minimum: f(0, ..., 0) = 0
    Domain: typically [-5.12, 5.12]
    """
    n = len(x)
    return float(10 * n + np.sum(x ** 2 - 10 * np.cos(2 * np.pi * x)))


def rosenbrock(x: np.ndarray) -> float:
    """
    Rosenbrock function: non-convex function with narrow valley
    f(x) = sum(100*(x_{i+1} - x_i^2)^2 + (1 - x_i)^2)
    Global minimum: f(1, ..., 1) = 0
    Domain: typically [-2.048, 2.048] or [-5, 10]
    """
    return float(np.sum(100 * (x[1:] - x[:-1] ** 2) ** 2 + (1 - x[:-1]) ** 2))


def ackley(x: np.ndarray) -> float:
    """
    Ackley function: multimodal function with many local minima
    Global minimum: f(0, ..., 0) = 0
    Domain: typically [-32.768, 32.768]
    """
    n = len(x)
    sum1 = np.sum(x ** 2)
    sum2 = np.sum(np.cos(2 * np.pi * x))
    return float(-20 * np.exp(-0.2 * np.sqrt(sum1 / n)) - np.exp(sum2 / n) + 20 + np.e)


def griewank(x: np.ndarray) -> float:
    """
    Griewank function: multimodal function
    Global minimum: f(0, ..., 0) = 0
    Domain: typically [-600, 600]
    """
    sum_part = np.sum(x ** 2) / 4000
    prod_part = np.prod(np.cos(x / np.sqrt(np.arange(1, len(x) + 1))))
    return float(sum_part - prod_part + 1)


# Fitness function registry
FITNESS_FUNCTIONS: Dict[str, Callable] = {
    'sphere': sphere,
    'rastrigin': rastrigin,
    'rosenbrock': rosenbrock,
    'ackley': ackley,
    'griewank': griewank
}


# ==============================================================================
# Helper Functions
# ==============================================================================

def get_fitness_function(name: str) -> Callable:
    """
    Get fitness function by name.

    Args:
        name: Name of the fitness function

    Returns:
        Callable fitness function

    Raises:
        ValueError: If function name not found
    """
    if name not in FITNESS_FUNCTIONS:
        available = ', '.join(FITNESS_FUNCTIONS.keys())
        raise ValueError(
            f"Unknown fitness function '{name}'. Available functions: {available}"
        )
    return FITNESS_FUNCTIONS[name]


def create_problem_dict(
    dimensions: int,
    bounds: List[tuple],
    fitness_function: Callable,
    objective: str = 'minimize'
) -> Dict[str, Any]:
    """
    Create a problem dictionary for algorithm initialization.

    Args:
        dimensions: Number of dimensions
        bounds: List of (lower, upper) tuples
        fitness_function: Callable fitness function
        objective: 'minimize' or 'maximize'

    Returns:
        Problem dictionary compatible with OptimizationAlgorithm base class
    """
    return {
        'dimensions': dimensions,
        'bounds': bounds,
        'fitness_function': fitness_function,
        'objective': objective
    }


def format_convergence_curve(convergence_curve: List[float], max_points: int = 100) -> List[float]:
    """
    Downsample convergence curve if it has too many points.

    Args:
        convergence_curve: Full convergence curve
        max_points: Maximum number of points to return

    Returns:
        Downsampled convergence curve
    """
    if len(convergence_curve) <= max_points:
        return convergence_curve

    # Sample evenly across the curve
    indices = np.linspace(0, len(convergence_curve) - 1, max_points, dtype=int)
    return [convergence_curve[i] for i in indices]


def calculate_statistics(convergence_curve: List[float]) -> Dict[str, float]:
    """
    Calculate statistics from convergence curve.

    Args:
        convergence_curve: List of fitness values over iterations

    Returns:
        Dictionary with statistics
    """
    if not convergence_curve:
        return {}

    return {
        'initial_fitness': float(convergence_curve[0]),
        'final_fitness': float(convergence_curve[-1]),
        'improvement': float(convergence_curve[0] - convergence_curve[-1]),
        'improvement_percent': float(
            ((convergence_curve[0] - convergence_curve[-1]) / abs(convergence_curve[0]) * 100)
            if convergence_curve[0] != 0 else 0
        )
    }


def get_recommended_bounds(function_name: str, dimensions: int) -> List[Tuple[float, float]]:
    """
    Get recommended bounds for standard benchmark functions.

    Args:
        function_name: Name of the fitness function
        dimensions: Number of dimensions

    Returns:
        List of (lower, upper) tuples for each dimension
    """
    bounds_map = {
        'sphere': (-5.12, 5.12),
        'rastrigin': (-5.12, 5.12),
        'rosenbrock': (-2.048, 2.048),
        'ackley': (-32.768, 32.768),
        'griewank': (-600.0, 600.0)
    }

    bound = bounds_map.get(function_name, (-10.0, 10.0))
    return [bound] * dimensions
