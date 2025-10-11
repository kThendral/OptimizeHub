"""
Validation functions for optimization problems and algorithm parameters.
"""
from typing import Dict, List, Tuple, Any
from app.config import MAX_DIMENSIONS, MAX_ITERATIONS


def validate_problem(problem: Dict[str, Any]) -> Tuple[bool, List[str], List[str]]:
    """
    Validate optimization problem definition.

    Args:
        problem: Dictionary containing problem definition

    Returns:
        Tuple of (is_valid, errors, warnings)
    """
    errors = []
    warnings = []

    # Check required fields
    required_fields = ['dimensions', 'bounds']
    for field in required_fields:
        if field not in problem:
            errors.append(f"Missing required field: '{field}'")

    if errors:
        return False, errors, warnings

    # Validate dimensions
    dimensions = problem.get('dimensions')
    if not isinstance(dimensions, int):
        errors.append(f"'dimensions' must be an integer, got {type(dimensions).__name__}")
    elif dimensions <= 0:
        errors.append(f"'dimensions' must be positive, got {dimensions}")
    elif dimensions > MAX_DIMENSIONS:
        errors.append(f"'dimensions' exceeds maximum allowed ({MAX_DIMENSIONS}), got {dimensions}")
    elif dimensions > 30:
        warnings.append(f"High dimension count ({dimensions}) may increase computation time")

    # Validate bounds
    bounds = problem.get('bounds')
    if not isinstance(bounds, list):
        errors.append(f"'bounds' must be a list, got {type(bounds).__name__}")
    elif dimensions and len(bounds) != dimensions:
        errors.append(f"'bounds' length ({len(bounds)}) must match 'dimensions' ({dimensions})")
    else:
        for i, bound in enumerate(bounds):
            bound_errors = validate_bound(bound, i)
            errors.extend(bound_errors)

    # Validate objective if provided
    objective = problem.get('objective', 'minimize')
    if objective not in ['minimize', 'maximize']:
        errors.append(f"'objective' must be 'minimize' or 'maximize', got '{objective}'")

    return len(errors) == 0, errors, warnings


def validate_bound(bound: Any, index: int) -> List[str]:
    """
    Validate a single bound tuple.

    Args:
        bound: Bound tuple (lower, upper)
        index: Index of the bound in the bounds list

    Returns:
        List of error messages
    """
    errors = []

    if not isinstance(bound, (tuple, list)):
        errors.append(f"Bound at index {index} must be a tuple or list, got {type(bound).__name__}")
        return errors

    if len(bound) != 2:
        errors.append(f"Bound at index {index} must have exactly 2 elements (lower, upper), got {len(bound)}")
        return errors

    lower, upper = bound

    if not isinstance(lower, (int, float)):
        errors.append(f"Bound at index {index}: lower bound must be numeric, got {type(lower).__name__}")

    if not isinstance(upper, (int, float)):
        errors.append(f"Bound at index {index}: upper bound must be numeric, got {type(upper).__name__}")

    if isinstance(lower, (int, float)) and isinstance(upper, (int, float)):
        if lower >= upper:
            errors.append(f"Bound at index {index}: lower ({lower}) must be less than upper ({upper})")

    return errors


def validate_algorithm_params(algorithm: str, params: Dict[str, Any]) -> Tuple[bool, List[str], List[str]]:
    """
    Validate algorithm-specific parameters.

    Args:
        algorithm: Algorithm name
        params: Dictionary of algorithm parameters

    Returns:
        Tuple of (is_valid, errors, warnings)
    """
    errors = []
    warnings = []

    # Validate max_iterations (common to all algorithms)
    max_iterations = params.get('max_iterations', 50)
    if not isinstance(max_iterations, int):
        errors.append(f"'max_iterations' must be an integer, got {type(max_iterations).__name__}")
    elif max_iterations < 1:
        errors.append(f"'max_iterations' must be at least 1, got {max_iterations}")
    elif max_iterations > MAX_ITERATIONS:
        errors.append(f"'max_iterations' exceeds maximum ({MAX_ITERATIONS}), got {max_iterations}")
    elif max_iterations < 10:
        warnings.append(f"Low iteration count ({max_iterations}) may not find optimal solution")

    # Algorithm-specific validation
    if algorithm == 'particle_swarm':
        pso_errors, pso_warnings = _validate_pso_params(params)
        errors.extend(pso_errors)
        warnings.extend(pso_warnings)
    elif algorithm == 'genetic_algorithm':
        ga_errors, ga_warnings = _validate_ga_params(params)
        errors.extend(ga_errors)
        warnings.extend(ga_warnings)

    return len(errors) == 0, errors, warnings


def _validate_pso_params(params: Dict[str, Any]) -> Tuple[List[str], List[str]]:
    """Validate PSO-specific parameters."""
    errors = []
    warnings = []

    # Swarm size
    swarm_size = params.get('swarm_size', 30)
    if not isinstance(swarm_size, int):
        errors.append(f"'swarm_size' must be an integer, got {type(swarm_size).__name__}")
    elif swarm_size < 10:
        errors.append(f"'swarm_size' must be at least 10 for viable swarm behavior, got {swarm_size}")
    elif swarm_size > 200:
        warnings.append(f"Large swarm size ({swarm_size}) may be computationally expensive")

    # Inertia weight
    w = params.get('w', 0.7)
    if not isinstance(w, (int, float)):
        errors.append(f"'w' (inertia weight) must be numeric, got {type(w).__name__}")
    elif w < 0:
        warnings.append(f"Negative inertia weight ({w}) is non-standard")
    elif w >= 1.0:
        warnings.append(f"Inertia weight >= 1.0 ({w}) may cause divergence")

    # Cognitive coefficient
    c1 = params.get('c1', 1.5)
    if not isinstance(c1, (int, float)):
        errors.append(f"'c1' (cognitive coefficient) must be numeric, got {type(c1).__name__}")

    # Social coefficient
    c2 = params.get('c2', 1.5)
    if not isinstance(c2, (int, float)):
        errors.append(f"'c2' (social coefficient) must be numeric, got {type(c2).__name__}")

    # Both c1 and c2 cannot be zero
    if isinstance(c1, (int, float)) and isinstance(c2, (int, float)):
        if c1 == 0 and c2 == 0:
            errors.append("Both 'c1' and 'c2' cannot be zero - particles would not move")

    return errors, warnings


def _validate_ga_params(params: Dict[str, Any]) -> Tuple[List[str], List[str]]:
    """Validate GA-specific parameters."""
    errors = []
    warnings = []

    # Population size
    population_size = params.get('population_size', 50)
    if not isinstance(population_size, int):
        errors.append(f"'population_size' must be an integer, got {type(population_size).__name__}")
    elif population_size < 10:
        errors.append(f"'population_size' must be at least 10, got {population_size}")
    elif population_size > 200:
        warnings.append(f"Large population size ({population_size}) may be computationally expensive")

    # Crossover rate
    crossover_rate = params.get('crossover_rate', 0.8)
    if not isinstance(crossover_rate, (int, float)):
        errors.append(f"'crossover_rate' must be numeric, got {type(crossover_rate).__name__}")
    elif not (0.0 <= crossover_rate <= 1.0):
        errors.append(f"'crossover_rate' must be between 0.0 and 1.0, got {crossover_rate}")

    # Mutation rate
    mutation_rate = params.get('mutation_rate', 0.1)
    if not isinstance(mutation_rate, (int, float)):
        errors.append(f"'mutation_rate' must be numeric, got {type(mutation_rate).__name__}")
    elif not (0.0 <= mutation_rate <= 1.0):
        errors.append(f"'mutation_rate' must be between 0.0 and 1.0, got {mutation_rate}")
    elif mutation_rate > 0.5:
        warnings.append(f"High mutation rate ({mutation_rate}) may hinder convergence")

    # Tournament size
    tournament_size = params.get('tournament_size', 3)
    if not isinstance(tournament_size, int):
        errors.append(f"'tournament_size' must be an integer, got {type(tournament_size).__name__}")
    elif tournament_size < 2:
        errors.append(f"'tournament_size' must be at least 2, got {tournament_size}")
    elif tournament_size > population_size:
        errors.append(f"'tournament_size' ({tournament_size}) cannot exceed population_size ({population_size})")

    return errors, warnings


def validate_bounds(bounds: List[Tuple[float, float]], dimensions: int) -> Tuple[bool, List[str]]:
    """
    Validate bounds for all dimensions.

    Args:
        bounds: List of (lower, upper) tuples
        dimensions: Expected number of dimensions

    Returns:
        Tuple of (is_valid, errors)
    """
    errors = []

    if len(bounds) != dimensions:
        errors.append(f"Bounds length ({len(bounds)}) must match dimensions ({dimensions})")
        return False, errors

    for i, bound in enumerate(bounds):
        bound_errors = validate_bound(bound, i)
        errors.extend(bound_errors)

    return len(errors) == 0, errors
