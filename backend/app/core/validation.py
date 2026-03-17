"""
Validation functions for optimization problems and algorithm parameters.

This module provides comprehensive validation for optimization problems and
algorithm-specific parameters. It returns both errors (blocking) and warnings
(educational, non-blocking) to help users configure algorithms effectively.
"""
from typing import Dict, List, Tuple, Any
from app.config import MAX_DIMENSIONS, MAX_ITERATIONS


# ==============================================================================
# Warning Message Templates (Educational & Clear)
# ==============================================================================

WARNING_MESSAGES = {
    # General warnings
    'low_iterations': (
        "⚠️ Low iteration count ({value}) may not allow the algorithm to converge. "
        "Consider using at least 20-50 iterations for better results. "
        "Most optimization problems benefit from more iterations to explore the search space."
    ),
    'high_dimensions': (
        "⚠️ High dimension count ({value}) will increase computation time significantly. "
        "Optimization difficulty grows exponentially with dimensions. "
        "Consider whether all dimensions are necessary for your problem."
    ),

    # PSO warnings
    'pso_low_swarm': (
        "⚠️ Swarm size below 20 may cause premature convergence in PSO. "
        "Consider using 30-100 particles for better exploration of the search space. "
        "Larger swarms provide more diverse search trajectories."
    ),
    'pso_high_w': (
        "⚠️ Inertia weight (w={value}) >= 1.0 may cause particle velocities to diverge. "
        "Standard PSO uses w between 0.4-0.9 for stable convergence. "
        "Consider using 0.7-0.9 for balanced exploration/exploitation."
    ),
    'pso_negative_w': (
        "⚠️ Negative inertia weight (w={value}) is non-standard and may produce unexpected behavior. "
        "While used in some research variants, standard PSO uses positive w values. "
        "Typical range: 0.4-0.9 for stable convergence."
    ),
    'pso_no_movement': (
        "⚠️ With w≈0, c1≈0, and c2 very small ({c2}), particles will barely move. "
        "PSO requires velocity components to search effectively. "
        "Consider: w=0.7, c1=1.5, c2=1.5 for balanced search behavior."
    ),
    'pso_high_acceleration': (
        "⚠️ High acceleration coefficients (c1={c1}, c2={c2}) may cause erratic particle movement. "
        "Values above 4.0 can lead to instability. "
        "Recommended: c1 + c2 ≤ 4.0, typically c1=c2=1.5 or 2.0."
    ),

    # GA warnings
    'ga_low_population': (
        "⚠️ Population size below 20 may limit genetic diversity in GA. "
        "Consider using 30-100 individuals for better exploration. "
        "Small populations can lead to premature convergence to suboptimal solutions."
    ),
    'ga_no_variation': (
        "⚠️ Both crossover_rate and mutation_rate are 0 — the GA cannot evolve! "
        "Without genetic operators, the algorithm will only perform selection on the initial population. "
        "Recommended: crossover_rate=0.7-0.9, mutation_rate=0.01-0.1."
    ),
    'ga_mutation_only': (
        "⚠️ Crossover is disabled (rate=0). GA will rely solely on mutation for variation. "
        "This reduces the algorithm's ability to combine good solutions. "
        "Consider enabling crossover (0.6-0.9) for better performance."
    ),
    'ga_crossover_only': (
        "⚠️ Mutation is disabled (rate=0). GA cannot introduce new genetic material. "
        "Without mutation, the algorithm may get stuck in local optima. "
        "Recommended mutation rate: 0.01-0.1 per gene."
    ),
    'ga_high_mutation': (
        "⚠️ High mutation rate ({value}) may turn GA into random search. "
        "Mutation rates above 0.3 disrupt good solutions too frequently. "
        "Recommended: 0.01-0.1 for continuous problems, 0.001-0.05 for discrete."
    ),
    'ga_low_diversity': (
        "⚠️ Small population ({pop}) with low mutation ({mut}) and few iterations ({iter}) "
        "may not provide enough genetic diversity. "
        "Consider increasing population to 30+, or mutation to 0.1+, or iterations to 30+."
    ),
    'ga_high_tournament': (
        "⚠️ Tournament size ({value}) is large relative to population ({pop}). "
        "This creates very high selection pressure, reducing diversity. "
        "Recommended: tournament_size = 2-5 for most problems."
    ),

    # DE warnings
    'de_low_population': (
        "⚠️ Population size below 20 may limit DE's differential mutation effectiveness. "
        "DE typically works best with population = 5-10 × number of dimensions. "
        "Consider using at least 30-50 individuals."
    ),
    'de_extreme_f': (
        "⚠️ Differential weight F={value} is at the extreme. "
        "F=2.0 causes very large mutations, which may overshoot optima. "
        "F<0.1 causes very small mutations, slowing convergence. "
        "Recommended: F=0.5-0.9 for most problems."
    ),
    'de_low_cr': (
        "⚠️ Crossover probability CR={value} is very low. "
        "Low CR means few dimensions are modified per generation. "
        "This can slow convergence significantly. Recommended: CR=0.7-1.0."
    ),
    'de_rand2_small_pop': (
        "⚠️ Strategy 'rand/2/bin' requires 5 distinct vectors but population is only {value}. "
        "This limits mutation diversity. Consider using population ≥ 20 for rand/2 strategies, "
        "or switch to 'rand/1/bin' for smaller populations."
    ),

    # SA warnings
    'sa_fast_cooling': (
        "⚠️ Cooling rate {value} is very fast (< 0.8). "
        "The algorithm may not explore enough before converging. "
        "Recommended: 0.9-0.99 for thorough exploration."
    ),
    'sa_narrow_temp_range': (
        "⚠️ Temperature range is narrow (initial={init}, final={final}). "
        "SA needs sufficient temperature range for effective exploration→exploitation transition. "
        "Consider: initial_temp = 100-1000, final_temp = 0.001-0.1."
    ),
    'sa_large_neighbor_std': (
        "⚠️ Neighbor step size (std={value}) is large. "
        "This may cause excessive jumping, missing fine-grained optima. "
        "Recommended: 0.05-0.2 for continuous optimization."
    ),

    # ACOR warnings
    'acor_small_archive': (
        "⚠️ Archive size ({value}) is very small relative to colony size ({colony}). "
        "Small archives may not maintain enough solution diversity. "
        "Recommended: archive_size = 30-50% of colony_size."
    ),
    'acor_extreme_q': (
        "⚠️ Locality parameter q={value} is extreme. "
        "Very small q (<0.001) concentrates search too narrowly. "
        "Very large q (>0.5) spreads search too widely. "
        "Recommended: q=0.01-0.1 for balanced intensification."
    ),
    'acor_low_xi': (
        "⚠️ Convergence speed xi={value} is very low. "
        "Low xi values cause very slow convergence. "
        "Recommended: xi=0.7-0.95 for practical optimization."
    ),
}


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
        warnings.append(WARNING_MESSAGES['low_iterations'].format(value=max_iterations))

    # Algorithm-specific validation
    if algorithm == 'particle_swarm':
        pso_errors, pso_warnings = _validate_pso_params(params)
        errors.extend(pso_errors)
        warnings.extend(pso_warnings)
    elif algorithm == 'genetic_algorithm':
        ga_errors, ga_warnings = _validate_ga_params(params)
        errors.extend(ga_errors)
        warnings.extend(ga_warnings)
    elif algorithm == 'differential_evolution':
        de_errors, de_warnings = _validate_de_params(params)
        errors.extend(de_errors)
        warnings.extend(de_warnings)
    elif algorithm == 'simulated_annealing':
        sa_errors, sa_warnings = _validate_sa_params(params)
        errors.extend(sa_errors)
        warnings.extend(sa_warnings)
    elif algorithm == 'ant_colony':
        acor_errors, acor_warnings = _validate_acor_params(params)
        errors.extend(acor_errors)
        warnings.extend(acor_warnings)

    return len(errors) == 0, errors, warnings


def _validate_pso_params(params: Dict[str, Any]) -> Tuple[List[str], List[str]]:
    """Validate PSO-specific parameters with educational warnings."""
    errors = []
    warnings = []

    # Swarm size
    swarm_size = params.get('swarm_size', 30)
    if not isinstance(swarm_size, int):
        errors.append(f"'swarm_size' must be an integer, got {type(swarm_size).__name__}")
    elif swarm_size < 10:
        errors.append(f"'swarm_size' must be at least 10 for viable swarm behavior, got {swarm_size}")
    elif swarm_size < 20:
        warnings.append(WARNING_MESSAGES['pso_low_swarm'])
    elif swarm_size > 200:
        warnings.append(f"⚠️ Large swarm size ({swarm_size}) may be computationally expensive without proportional benefit.")

    # Inertia weight
    w = params.get('w', 0.7)
    if not isinstance(w, (int, float)):
        errors.append(f"'w' (inertia weight) must be numeric, got {type(w).__name__}")
    elif w < 0:
        warnings.append(WARNING_MESSAGES['pso_negative_w'].format(value=w))
    elif w >= 1.0:
        warnings.append(WARNING_MESSAGES['pso_high_w'].format(value=w))

    # Cognitive coefficient
    c1 = params.get('c1', 1.5)
    if not isinstance(c1, (int, float)):
        errors.append(f"'c1' (cognitive coefficient) must be numeric, got {type(c1).__name__}")

    # Social coefficient
    c2 = params.get('c2', 1.5)
    if not isinstance(c2, (int, float)):
        errors.append(f"'c2' (social coefficient) must be numeric, got {type(c2).__name__}")

    # Check for problematic coefficient combinations
    if isinstance(c1, (int, float)) and isinstance(c2, (int, float)) and isinstance(w, (int, float)):
        # Both c1 and c2 cannot be zero
        if c1 == 0 and c2 == 0:
            errors.append("Both 'c1' and 'c2' cannot be zero - particles would not move")

        # Check for near-zero movement configuration
        if abs(w) < 0.1 and abs(c1) < 0.1 and abs(c2) < 0.5:
            warnings.append(WARNING_MESSAGES['pso_no_movement'].format(c2=c2))

        # Check for excessive acceleration
        if c1 > 4.0 or c2 > 4.0:
            warnings.append(WARNING_MESSAGES['pso_high_acceleration'].format(c1=c1, c2=c2))

    return errors, warnings


def _validate_ga_params(params: Dict[str, Any]) -> Tuple[List[str], List[str]]:
    """Validate GA-specific parameters with educational warnings."""
    errors = []
    warnings = []

    # Population size
    population_size = params.get('population_size', 50)
    if not isinstance(population_size, int):
        errors.append(f"'population_size' must be an integer, got {type(population_size).__name__}")
    elif population_size < 10:
        errors.append(f"'population_size' must be at least 10, got {population_size}")
    elif population_size < 20:
        warnings.append(WARNING_MESSAGES['ga_low_population'])
    elif population_size > 200:
        warnings.append(f"⚠️ Large population size ({population_size}) may be computationally expensive without proportional benefit.")

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
    elif mutation_rate > 0.3:
        warnings.append(WARNING_MESSAGES['ga_high_mutation'].format(value=mutation_rate))

    # Tournament size
    tournament_size = params.get('tournament_size', 3)
    if not isinstance(tournament_size, int):
        errors.append(f"'tournament_size' must be an integer, got {type(tournament_size).__name__}")
    elif tournament_size < 2:
        errors.append(f"'tournament_size' must be at least 2, got {tournament_size}")
    elif isinstance(population_size, int) and tournament_size > population_size:
        errors.append(f"'tournament_size' ({tournament_size}) cannot exceed population_size ({population_size})")
    elif isinstance(population_size, int) and tournament_size > population_size * 0.5:
        warnings.append(WARNING_MESSAGES['ga_high_tournament'].format(value=tournament_size, pop=population_size))

    # Check for problematic operator combinations
    if isinstance(crossover_rate, (int, float)) and isinstance(mutation_rate, (int, float)):
        # No variation at all
        if crossover_rate == 0 and mutation_rate == 0:
            warnings.append(WARNING_MESSAGES['ga_no_variation'])
        # Mutation only
        elif crossover_rate == 0 and mutation_rate > 0:
            warnings.append(WARNING_MESSAGES['ga_mutation_only'])
        # Crossover only
        elif crossover_rate > 0 and mutation_rate == 0:
            warnings.append(WARNING_MESSAGES['ga_crossover_only'])

    # Check for low diversity configuration
    max_iterations = params.get('max_iterations', 50)
    if (isinstance(population_size, int) and isinstance(mutation_rate, (int, float)) and
        isinstance(max_iterations, int)):
        if population_size < 20 and mutation_rate < 0.05 and max_iterations < 20:
            warnings.append(WARNING_MESSAGES['ga_low_diversity'].format(
                pop=population_size, mut=mutation_rate, iter=max_iterations
            ))

    return errors, warnings


def _validate_de_params(params: Dict[str, Any]) -> Tuple[List[str], List[str]]:
    """Validate Differential Evolution parameters with educational warnings."""
    errors = []
    warnings = []

    # Population size
    population_size = params.get('population_size', 50)
    if not isinstance(population_size, int):
        errors.append(f"'population_size' must be an integer, got {type(population_size).__name__}")
    elif population_size < 10:
        errors.append(f"'population_size' must be at least 10, got {population_size}")
    elif population_size < 20:
        warnings.append(WARNING_MESSAGES['de_low_population'])

    # Differential weight F
    F = params.get('F', 0.8)
    if not isinstance(F, (int, float)):
        errors.append(f"'F' (differential weight) must be numeric, got {type(F).__name__}")
    elif F <= 0 or F > 2.0:
        errors.append(f"'F' must be in range (0, 2.0], got {F}")
    elif F < 0.1 or F > 1.5:
        warnings.append(WARNING_MESSAGES['de_extreme_f'].format(value=F))

    # Crossover probability CR
    CR = params.get('CR', 0.9)
    if not isinstance(CR, (int, float)):
        errors.append(f"'CR' (crossover probability) must be numeric, got {type(CR).__name__}")
    elif CR < 0 or CR > 1.0:
        errors.append(f"'CR' must be in range [0, 1.0], got {CR}")
    elif CR < 0.3:
        warnings.append(WARNING_MESSAGES['de_low_cr'].format(value=CR))

    # Strategy validation
    strategy = params.get('strategy', 'rand/1/bin')
    valid_strategies = ['rand/1/bin', 'best/1/bin', 'rand/2/bin']
    if strategy not in valid_strategies:
        errors.append(f"'strategy' must be one of {valid_strategies}, got '{strategy}'")
    elif strategy == 'rand/2/bin' and isinstance(population_size, int) and population_size < 15:
        warnings.append(WARNING_MESSAGES['de_rand2_small_pop'].format(value=population_size))

    # Boundary handling
    boundary_handling = params.get('boundary_handling', 'clip')
    valid_boundaries = ['clip', 'reflect', 'wrap']
    if boundary_handling not in valid_boundaries:
        errors.append(f"'boundary_handling' must be one of {valid_boundaries}, got '{boundary_handling}'")

    return errors, warnings


def _validate_sa_params(params: Dict[str, Any]) -> Tuple[List[str], List[str]]:
    """Validate Simulated Annealing parameters with educational warnings."""
    errors = []
    warnings = []

    # Initial temperature
    initial_temp = params.get('initial_temp', 100.0)
    if not isinstance(initial_temp, (int, float)):
        errors.append(f"'initial_temp' must be numeric, got {type(initial_temp).__name__}")
    elif initial_temp <= 0:
        errors.append(f"'initial_temp' must be positive, got {initial_temp}")

    # Final temperature
    final_temp = params.get('final_temp', 0.01)
    if not isinstance(final_temp, (int, float)):
        errors.append(f"'final_temp' must be numeric, got {type(final_temp).__name__}")
    elif final_temp <= 0:
        errors.append(f"'final_temp' must be positive, got {final_temp}")

    # Temperature relationship
    if isinstance(initial_temp, (int, float)) and isinstance(final_temp, (int, float)):
        if initial_temp <= final_temp:
            errors.append(f"'initial_temp' ({initial_temp}) must be greater than 'final_temp' ({final_temp})")
        elif initial_temp < final_temp * 10:
            warnings.append(WARNING_MESSAGES['sa_narrow_temp_range'].format(init=initial_temp, final=final_temp))

    # Cooling rate
    cooling_rate = params.get('cooling_rate', 0.95)
    cooling_schedule = params.get('cooling_schedule', 'geometric')
    if cooling_schedule == 'geometric':
        if not isinstance(cooling_rate, (int, float)):
            errors.append(f"'cooling_rate' must be numeric, got {type(cooling_rate).__name__}")
        elif cooling_rate <= 0 or cooling_rate >= 1:
            errors.append(f"'cooling_rate' must be in range (0, 1) for geometric cooling, got {cooling_rate}")
        elif cooling_rate < 0.8:
            warnings.append(WARNING_MESSAGES['sa_fast_cooling'].format(value=cooling_rate))

    # Neighbor standard deviation
    neighbor_std = params.get('neighbor_std', 0.1)
    if not isinstance(neighbor_std, (int, float)):
        errors.append(f"'neighbor_std' must be numeric, got {type(neighbor_std).__name__}")
    elif neighbor_std <= 0:
        errors.append(f"'neighbor_std' must be positive, got {neighbor_std}")
    elif neighbor_std > 1.0:
        errors.append(f"'neighbor_std' must be <= 1.0, got {neighbor_std}")
    elif neighbor_std > 0.5:
        warnings.append(WARNING_MESSAGES['sa_large_neighbor_std'].format(value=neighbor_std))

    # Cooling schedule
    valid_schedules = ['geometric', 'linear', 'logarithmic']
    if cooling_schedule not in valid_schedules:
        errors.append(f"'cooling_schedule' must be one of {valid_schedules}, got '{cooling_schedule}'")

    return errors, warnings


def _validate_acor_params(params: Dict[str, Any]) -> Tuple[List[str], List[str]]:
    """Validate Ant Colony Optimization (ACOR) parameters with educational warnings."""
    errors = []
    warnings = []

    # Colony size
    colony_size = params.get('colony_size', 30)
    if not isinstance(colony_size, int):
        errors.append(f"'colony_size' must be an integer, got {type(colony_size).__name__}")
    elif colony_size < 5:
        errors.append(f"'colony_size' must be at least 5, got {colony_size}")
    elif colony_size < 15:
        warnings.append(f"⚠️ Colony size ({colony_size}) is small. Consider using 20-50 ants for better exploration.")

    # Archive size
    archive_size = params.get('archive_size', 10)
    if not isinstance(archive_size, int):
        errors.append(f"'archive_size' must be an integer, got {type(archive_size).__name__}")
    elif archive_size < 1:
        errors.append(f"'archive_size' must be at least 1, got {archive_size}")
    elif isinstance(colony_size, int) and archive_size > colony_size:
        errors.append(f"'archive_size' ({archive_size}) cannot exceed 'colony_size' ({colony_size})")
    elif isinstance(colony_size, int) and archive_size < colony_size * 0.2:
        warnings.append(WARNING_MESSAGES['acor_small_archive'].format(value=archive_size, colony=colony_size))

    # Locality parameter q
    q = params.get('q', 0.01)
    if not isinstance(q, (int, float)):
        errors.append(f"'q' (locality parameter) must be numeric, got {type(q).__name__}")
    elif q <= 0:
        errors.append(f"'q' must be positive, got {q}")
    elif q < 0.001 or q > 0.5:
        warnings.append(WARNING_MESSAGES['acor_extreme_q'].format(value=q))

    # Convergence speed xi
    xi = params.get('xi', 0.85)
    if not isinstance(xi, (int, float)):
        errors.append(f"'xi' (convergence speed) must be numeric, got {type(xi).__name__}")
    elif xi <= 0 or xi > 1:
        errors.append(f"'xi' must be in range (0, 1], got {xi}")
    elif xi < 0.5:
        warnings.append(WARNING_MESSAGES['acor_low_xi'].format(value=xi))

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
