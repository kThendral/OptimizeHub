#!/usr/bin/env python3
"""
Runner script for executing custom fitness functions in Docker sandbox.
This script runs inside the isolated Docker container.
"""

import sys
import json
import time
import traceback
from pathlib import Path


def load_fitness_function(fitness_file_path):
    """
    Dynamically load the fitness function from the user's file.

    Args:
        fitness_file_path: Path to the fitness function Python file

    Returns:
        The fitness function callable

    Raises:
        ValueError: If fitness function is not found or invalid
    """
    try:
        # Read the fitness function code
        with open(fitness_file_path, 'r') as f:
            code = f.read()

        # Create a namespace for execution
        namespace = {'__name__': '__main__'}

        # Execute the code in the namespace
        exec(code, namespace)

        # Check if 'fitness' function exists
        if 'fitness' not in namespace:
            raise ValueError("Fitness function must be named 'fitness'")

        fitness_func = namespace['fitness']

        # Validate it's callable
        if not callable(fitness_func):
            raise ValueError("'fitness' must be a function")

        return fitness_func

    except Exception as e:
        raise ValueError(f"Failed to load fitness function: {str(e)}")


def run_optimization(fitness_func, config):
    """
    Run the optimization algorithm with the custom fitness function.

    Args:
        fitness_func: The custom fitness function
        config: Configuration dictionary with algorithm and parameters

    Returns:
        Dictionary with optimization results
    """
    import numpy as np

    algorithm = config.get('algorithm', 'PSO')
    params = config.get('parameters', {})
    problem = config.get('problem', {})

    # Extract problem parameters
    dimensions = problem.get('dimensions', 10)
    lower_bound = problem.get('lower_bound', -5.0)
    upper_bound = problem.get('upper_bound', 5.0)

    # Run the appropriate algorithm
    if algorithm == 'PSO':
        return run_pso(fitness_func, dimensions, lower_bound, upper_bound, params)
    elif algorithm == 'GA':
        return run_ga(fitness_func, dimensions, lower_bound, upper_bound, params)
    elif algorithm == 'DE':
        return run_de(fitness_func, dimensions, lower_bound, upper_bound, params)
    elif algorithm == 'SA':
        return run_sa(fitness_func, dimensions, lower_bound, upper_bound, params)
    elif algorithm == 'ACOR':
        return run_acor(fitness_func, dimensions, lower_bound, upper_bound, params)
    else:
        raise ValueError(f"Unknown algorithm: {algorithm}")


def run_pso(fitness_func, dimensions, lb, ub, params):
    """Particle Swarm Optimization implementation"""
    import numpy as np

    num_particles = params.get('num_particles', 30)
    max_iterations = params.get('max_iterations', 100)
    w = params.get('w', 0.7)
    c1 = params.get('c1', 1.5)
    c2 = params.get('c2', 1.5)

    # Initialize particles
    particles = np.random.uniform(lb, ub, (num_particles, dimensions))
    velocities = np.random.uniform(-1, 1, (num_particles, dimensions))

    # Evaluate initial fitness
    fitness_values = np.array([fitness_func(p) for p in particles])

    # Initialize personal best
    pbest = particles.copy()
    pbest_fitness = fitness_values.copy()

    # Initialize global best
    gbest_idx = np.argmin(fitness_values)
    gbest = particles[gbest_idx].copy()
    gbest_fitness = fitness_values[gbest_idx]

    convergence_history = [gbest_fitness]

    # Main PSO loop
    for iteration in range(max_iterations):
        for i in range(num_particles):
            # Update velocity
            r1, r2 = np.random.rand(2)
            velocities[i] = (w * velocities[i] +
                           c1 * r1 * (pbest[i] - particles[i]) +
                           c2 * r2 * (gbest - particles[i]))

            # Update position
            particles[i] = particles[i] + velocities[i]

            # Enforce bounds
            particles[i] = np.clip(particles[i], lb, ub)

            # Evaluate fitness
            fitness_values[i] = fitness_func(particles[i])

            # Update personal best
            if fitness_values[i] < pbest_fitness[i]:
                pbest[i] = particles[i].copy()
                pbest_fitness[i] = fitness_values[i]

                # Update global best
                if fitness_values[i] < gbest_fitness:
                    gbest = particles[i].copy()
                    gbest_fitness = fitness_values[i]

        convergence_history.append(gbest_fitness)

    return {
        'best_solution': gbest.tolist(),
        'best_fitness': float(gbest_fitness),
        'iterations': max_iterations,
        'convergence_history': convergence_history
    }


def run_ga(fitness_func, dimensions, lb, ub, params):
    """Genetic Algorithm implementation"""
    import numpy as np

    population_size = params.get('population_size', 50)
    max_generations = params.get('max_generations', 100)
    mutation_rate = params.get('mutation_rate', 0.1)
    crossover_rate = params.get('crossover_rate', 0.8)

    # Initialize population
    population = np.random.uniform(lb, ub, (population_size, dimensions))
    fitness_values = np.array([fitness_func(ind) for ind in population])

    best_idx = np.argmin(fitness_values)
    best_solution = population[best_idx].copy()
    best_fitness = fitness_values[best_idx]

    convergence_history = [best_fitness]

    for generation in range(max_generations):
        # Selection (tournament)
        new_population = []
        for _ in range(population_size):
            idx1, idx2 = np.random.choice(population_size, 2, replace=False)
            winner = idx1 if fitness_values[idx1] < fitness_values[idx2] else idx2
            new_population.append(population[winner].copy())

        new_population = np.array(new_population)

        # Crossover
        for i in range(0, population_size - 1, 2):
            if np.random.rand() < crossover_rate:
                alpha = np.random.rand()
                new_population[i] = alpha * new_population[i] + (1 - alpha) * new_population[i + 1]
                new_population[i + 1] = alpha * new_population[i + 1] + (1 - alpha) * new_population[i]

        # Mutation
        for i in range(population_size):
            if np.random.rand() < mutation_rate:
                mutation = np.random.uniform(-0.5, 0.5, dimensions)
                new_population[i] += mutation
                new_population[i] = np.clip(new_population[i], lb, ub)

        population = new_population
        fitness_values = np.array([fitness_func(ind) for ind in population])

        # Update best
        best_idx = np.argmin(fitness_values)
        if fitness_values[best_idx] < best_fitness:
            best_solution = population[best_idx].copy()
            best_fitness = fitness_values[best_idx]

        convergence_history.append(best_fitness)

    return {
        'best_solution': best_solution.tolist(),
        'best_fitness': float(best_fitness),
        'iterations': max_generations,
        'convergence_history': convergence_history
    }


def run_de(fitness_func, dimensions, lb, ub, params):
    """Differential Evolution implementation"""
    import numpy as np

    population_size = params.get('population_size', 50)
    max_generations = params.get('max_generations', 100)
    F = params.get('F', 0.8)
    CR = params.get('CR', 0.9)

    # Initialize population
    population = np.random.uniform(lb, ub, (population_size, dimensions))
    fitness_values = np.array([fitness_func(ind) for ind in population])

    best_idx = np.argmin(fitness_values)
    best_solution = population[best_idx].copy()
    best_fitness = fitness_values[best_idx]

    convergence_history = [best_fitness]

    for generation in range(max_generations):
        for i in range(population_size):
            # Mutation
            indices = [idx for idx in range(population_size) if idx != i]
            a, b, c = population[np.random.choice(indices, 3, replace=False)]
            mutant = a + F * (b - c)
            mutant = np.clip(mutant, lb, ub)

            # Crossover
            cross_points = np.random.rand(dimensions) < CR
            if not np.any(cross_points):
                cross_points[np.random.randint(0, dimensions)] = True

            trial = np.where(cross_points, mutant, population[i])

            # Selection
            trial_fitness = fitness_func(trial)
            if trial_fitness < fitness_values[i]:
                population[i] = trial
                fitness_values[i] = trial_fitness

                if trial_fitness < best_fitness:
                    best_solution = trial.copy()
                    best_fitness = trial_fitness

        convergence_history.append(best_fitness)

    return {
        'best_solution': best_solution.tolist(),
        'best_fitness': float(best_fitness),
        'iterations': max_generations,
        'convergence_history': convergence_history
    }


def run_sa(fitness_func, dimensions, lb, ub, params):
    """Simulated Annealing implementation"""
    import numpy as np

    max_iterations = params.get('max_iterations', 1000)
    initial_temp = params.get('initial_temperature', 100.0)
    cooling_rate = params.get('cooling_rate', 0.95)

    # Initialize solution
    current = np.random.uniform(lb, ub, dimensions)
    current_fitness = fitness_func(current)

    best_solution = current.copy()
    best_fitness = current_fitness

    convergence_history = [best_fitness]
    temperature = initial_temp

    for iteration in range(max_iterations):
        # Generate neighbor
        neighbor = current + np.random.uniform(-1, 1, dimensions)
        neighbor = np.clip(neighbor, lb, ub)
        neighbor_fitness = fitness_func(neighbor)

        # Acceptance criterion
        delta = neighbor_fitness - current_fitness
        if delta < 0 or np.random.rand() < np.exp(-delta / temperature):
            current = neighbor
            current_fitness = neighbor_fitness

            if current_fitness < best_fitness:
                best_solution = current.copy()
                best_fitness = current_fitness

        # Cool down
        temperature *= cooling_rate

        if iteration % 10 == 0:
            convergence_history.append(best_fitness)

    return {
        'best_solution': best_solution.tolist(),
        'best_fitness': float(best_fitness),
        'iterations': max_iterations,
        'convergence_history': convergence_history
    }


def run_acor(fitness_func, dimensions, lb, ub, params):
    """Ant Colony Optimization for Continuous domains (ACOR) implementation"""
    import numpy as np

    num_ants = params.get('num_ants', 50)
    max_iterations = params.get('max_iterations', 100)
    archive_size = params.get('archive_size', 50)
    q = params.get('q', 0.5)
    xi = params.get('xi', 0.85)

    # Initialize archive with random solutions
    archive = np.random.uniform(lb, ub, (archive_size, dimensions))
    fitness_values = np.array([fitness_func(sol) for sol in archive])

    # Sort archive by fitness
    sorted_indices = np.argsort(fitness_values)
    archive = archive[sorted_indices]
    fitness_values = fitness_values[sorted_indices]

    best_solution = archive[0].copy()
    best_fitness = fitness_values[0]

    convergence_history = [best_fitness]

    for iteration in range(max_iterations):
        new_solutions = []

        for ant in range(num_ants):
            # Calculate weights
            weights = np.array([np.exp(-i**2 / (2 * q**2 * archive_size**2))
                              for i in range(archive_size)])
            weights /= weights.sum()

            # Select solution from archive
            selected_idx = np.random.choice(archive_size, p=weights)

            # Generate new solution around selected one
            sigma = xi * np.sum([np.abs(archive[i] - archive[selected_idx])
                               for i in range(archive_size)], axis=0) / archive_size

            new_solution = archive[selected_idx] + np.random.normal(0, sigma, dimensions)
            new_solution = np.clip(new_solution, lb, ub)
            new_solutions.append(new_solution)

        # Evaluate new solutions
        new_solutions = np.array(new_solutions)
        new_fitness = np.array([fitness_func(sol) for sol in new_solutions])

        # Update archive
        archive = np.vstack([archive, new_solutions])
        fitness_values = np.concatenate([fitness_values, new_fitness])

        # Sort and keep best solutions
        sorted_indices = np.argsort(fitness_values)
        archive = archive[sorted_indices[:archive_size]]
        fitness_values = fitness_values[sorted_indices[:archive_size]]

        best_solution = archive[0].copy()
        best_fitness = fitness_values[0]

        convergence_history.append(best_fitness)

    return {
        'best_solution': best_solution.tolist(),
        'best_fitness': float(best_fitness),
        'iterations': max_iterations,
        'convergence_history': convergence_history
    }


def main():
    """Main execution function"""
    try:
        if len(sys.argv) != 3:
            raise ValueError("Usage: runner.py <fitness_file> <config_file>")

        fitness_file = sys.argv[1]
        config_file = sys.argv[2]

        # Load configuration
        with open(config_file, 'r') as f:
            config = json.load(f)

        # Load fitness function
        fitness_func = load_fitness_function(fitness_file)

        # Test fitness function with a sample input
        import numpy as np
        test_input = np.zeros(config.get('problem', {}).get('dimensions', 10))
        try:
            result = fitness_func(test_input)
            if not isinstance(result, (int, float, np.number)):
                raise ValueError("Fitness function must return a numeric value")
        except Exception as e:
            raise ValueError(f"Fitness function test failed: {str(e)}")

        # Record start time
        start_time = time.time()

        # Run optimization
        results = run_optimization(fitness_func, config)

        # Add execution time
        results['execution_time'] = time.time() - start_time
        results['success'] = True

        # Output results as JSON
        print(json.dumps(results))

    except Exception as e:
        # Output error as JSON
        error_result = {
            'success': False,
            'error': str(e),
            'error_type': type(e).__name__,
            'traceback': traceback.format_exc()
        }
        print(json.dumps(error_result))
        sys.exit(1)


if __name__ == '__main__':
    main()
