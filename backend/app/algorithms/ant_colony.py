"""
Ant Colony Optimization for Continuous Domains (ACOR) implementation.

This implementation uses the ACOR (Ant Colony Optimization for Continuous domains)
approach, where ants construct solutions by sampling from a weighted archive of
good solutions using Gaussian kernels.

Key differences from traditional ACO:
- Solution archive replaces pheromone matrix
- Gaussian sampling replaces discrete path selection
- Weighted probability based on solution quality
- Suitable for continuous optimization problems
"""

import numpy as np
import time
from typing import Any, Dict
from .base import OptimizationAlgorithm


class AntColonyOptimization(OptimizationAlgorithm):
    """
    Ant Colony Optimization for Continuous domains (ACOR).

    Uses an archive-based approach where ants sample solutions from a weighted
    archive of good solutions using Gaussian distributions. The archive represents
    the pheromone memory in continuous space.
    """

    def __init__(self, problem: Dict[str, Any], params: Dict[str, Any]):
        super().__init__(problem, params)

        # Validate problem schema
        self._validate_problem_schema(problem)

        # ACO parameters with defaults
        self.colony_size = params.get('colony_size', 30)
        self.max_iterations = params.get('max_iterations', 50)
        self.archive_size = params.get('archive_size', 10)
        self.q = params.get('q', 0.01)  # Locality of search (intensification)
        self.xi = params.get('xi', 0.85)  # Speed of convergence

        # Validate ACO parameters
        self._validate_parameters()

        # Problem parameters
        self.dimensions = problem['dimensions']
        self.bounds = problem['bounds']
        self.objective = problem.get('objective', 'minimize')
        self.fitness_function = problem['fitness_function']

        # ACO state variables
        self.archive_solutions = None  # Archive of solutions
        self.archive_fitness = None    # Fitness values of archived solutions
        self.archive_weights = None    # Selection weights for each archived solution
        self.best_solution_fitness = None

        # Timeout handling (30 seconds)
        self.timeout = 30
        self.start_time = None

    def _validate_problem_schema(self, problem: Dict[str, Any]):
        """Validate that problem dictionary contains required fields with valid values."""
        # Check required fields exist
        required_fields = ['dimensions', 'bounds', 'fitness_function']
        for field in required_fields:
            if field not in problem:
                raise ValueError(f"Problem schema missing required field: '{field}'")

        # Validate dimensions
        if not isinstance(problem['dimensions'], int) or problem['dimensions'] <= 0:
            raise ValueError(f"Invalid dimensions: {problem['dimensions']}. Must be a positive integer.")

        # Validate bounds
        bounds = problem['bounds']
        if not isinstance(bounds, list):
            raise ValueError(f"Bounds must be a list of tuples, got {type(bounds)}")

        if len(bounds) != problem['dimensions']:
            raise ValueError(
                f"Bounds length ({len(bounds)}) does not match dimensions ({problem['dimensions']})"
            )

        # Validate each bound
        for i, bound in enumerate(bounds):
            if not isinstance(bound, (tuple, list)) or len(bound) != 2:
                raise ValueError(f"Bound at index {i} must be a tuple/list of (lower, upper)")

            lower, upper = bound
            if not isinstance(lower, (int, float)) or not isinstance(upper, (int, float)):
                raise ValueError(f"Bound at index {i} contains non-numeric values: {bound}")

            if lower >= upper:
                raise ValueError(f"Invalid bound at index {i}: lower ({lower}) >= upper ({upper})")

        # Validate fitness function is callable
        if not callable(problem['fitness_function']):
            raise ValueError("fitness_function must be callable")

        # Validate objective if provided
        objective = problem.get('objective', 'minimize')
        if objective not in ['minimize', 'maximize']:
            raise ValueError(f"Invalid objective: {objective}. Must be 'minimize' or 'maximize'")

    def _validate_parameters(self):
        """Validate ACO-specific parameters with explicit errors."""
        # Colony size: Minimum 5 for viable ACO behavior
        if not isinstance(self.colony_size, int) or self.colony_size < 5:
            raise ValueError(
                f"colony_size must be ≥5 for viable ACO behavior (got {self.colony_size}). "
                f"Small colonies don't provide sufficient exploration."
            )

        # Iterations: Hard limit for SaaS platform
        if not isinstance(self.max_iterations, int) or self.max_iterations < 1:
            raise ValueError(f"max_iterations must be ≥1, got {self.max_iterations}")

        if self.max_iterations > 100:
            raise ValueError(
                f"max_iterations limited to 100 (platform constraint), got {self.max_iterations}. "
                f"Contact support for higher limits."
            )

        # Archive size: Must be between 1 and colony_size
        if not isinstance(self.archive_size, int) or self.archive_size < 1:
            raise ValueError(f"archive_size must be ≥1, got {self.archive_size}")

        if self.archive_size > self.colony_size:
            raise ValueError(
                f"archive_size ({self.archive_size}) cannot exceed colony_size ({self.colony_size}). "
                f"Archive stores best solutions from colony."
            )

        # q parameter: Controls locality of search
        if not isinstance(self.q, (int, float)) or self.q <= 0:
            raise ValueError(
                f"q (locality parameter) must be > 0, got {self.q}. "
                f"Typical range: 0.001 to 0.1"
            )

        # xi parameter: Speed of convergence (0 to 1)
        if not isinstance(self.xi, (int, float)):
            raise ValueError(f"xi (convergence speed) must be numeric, got {type(self.xi)}")

        if not (0 < self.xi <= 1):
            raise ValueError(
                f"xi must be between 0 and 1 (exclusive 0, inclusive 1), got {self.xi}. "
                f"Typical range: 0.7 to 0.95"
            )

    def initialize(self):
        """Initialize solution archive with random solutions."""
        # Initialize archive with random solutions within bounds
        self.archive_solutions = np.zeros((self.archive_size, self.dimensions))

        for i in range(self.archive_size):
            for d in range(self.dimensions):
                lower, upper = self.bounds[d]
                self.archive_solutions[i, d] = np.random.uniform(lower, upper)

        # Evaluate initial archive
        self.archive_fitness = np.array([self._evaluate(sol) for sol in self.archive_solutions])

        # Sort archive by fitness (best first)
        sorted_indices = self._get_sorted_indices(self.archive_fitness)
        self.archive_solutions = self.archive_solutions[sorted_indices]
        self.archive_fitness = self.archive_fitness[sorted_indices]

        # Calculate initial weights
        self._update_weights()

        # Set best solution
        self.best_solution = self.archive_solutions[0].copy()
        self.best_solution_fitness = self.archive_fitness[0]

        # Record initial convergence
        self.convergence_curve.append(float(self.best_solution_fitness))

    def optimize(self):
        """Execute ACOR optimization loop."""
        self.start_time = time.time()

        for iteration in range(self.max_iterations):
            # Check timeout
            if time.time() - self.start_time > self.timeout:
                break

            # Generate new solutions (ants construct solutions)
            new_solutions = []
            new_fitness = []

            for ant in range(self.colony_size):
                # Construct solution by sampling from archive
                new_solution = self._construct_solution()

                # Apply bounds
                new_solution = self._apply_bounds(new_solution)

                # Evaluate fitness
                fitness = self._evaluate(new_solution)

                new_solutions.append(new_solution)
                new_fitness.append(fitness)

            # Combine archive and new solutions
            combined_solutions = np.vstack([self.archive_solutions, np.array(new_solutions)])
            combined_fitness = np.concatenate([self.archive_fitness, np.array(new_fitness)])

            # Sort and keep best archive_size solutions
            sorted_indices = self._get_sorted_indices(combined_fitness)
            sorted_indices = sorted_indices[:self.archive_size]

            self.archive_solutions = combined_solutions[sorted_indices]
            self.archive_fitness = combined_fitness[sorted_indices]

            # Update weights for next iteration
            self._update_weights()

            # Update best solution
            if self._is_better(self.archive_fitness[0], self.best_solution_fitness):
                self.best_solution = self.archive_solutions[0].copy()
                self.best_solution_fitness = self.archive_fitness[0]

            # Record convergence
            self.convergence_curve.append(float(self.best_solution_fitness))

    def _construct_solution(self) -> np.ndarray:
        """
        Construct a new solution by sampling from the archive.

        Uses weighted probabilistic selection of archive solution,
        then samples around it using Gaussian distribution.
        """
        # Select archive solution based on weights
        selected_idx = np.random.choice(self.archive_size, p=self.archive_weights)
        selected_solution = self.archive_solutions[selected_idx]

        # Calculate standard deviation for Gaussian sampling
        # For each dimension, calculate diversity in archive
        new_solution = np.zeros(self.dimensions)

        for d in range(self.dimensions):
            # Calculate standard deviation based on archive diversity
            if self.archive_size > 1:
                # Average distance from selected solution to other solutions
                distances = np.abs(self.archive_solutions[:, d] - selected_solution[d])
                sigma = self.xi * np.sum(distances) / (self.archive_size - 1)
            else:
                # Fallback: use 10% of bound range
                lower, upper = self.bounds[d]
                sigma = 0.1 * (upper - lower)

            # Sample from Gaussian distribution
            new_solution[d] = selected_solution[d] + np.random.normal(0, sigma)

        return new_solution

    def _update_weights(self):
        """
        Update selection weights for archive solutions.

        Better solutions (lower rank) get higher weights using Gaussian function.
        Weight formula: w_i = (1 / (q * k * sqrt(2π))) * exp(-(rank-1)^2 / (2*q^2*k^2))
        where k = archive_size
        """
        k = self.archive_size
        q_k = self.q * k

        weights = np.zeros(self.archive_size)

        for i in range(self.archive_size):
            rank = i + 1  # Rank starts at 1 for best solution
            exponent = -((rank - 1) ** 2) / (2 * (q_k ** 2))
            weights[i] = (1.0 / (q_k * np.sqrt(2 * np.pi))) * np.exp(exponent)

        # Normalize weights to sum to 1
        weights_sum = np.sum(weights)
        if weights_sum > 0:
            self.archive_weights = weights / weights_sum
        else:
            # Fallback: uniform weights
            self.archive_weights = np.ones(self.archive_size) / self.archive_size

    def _get_sorted_indices(self, fitness_array: np.ndarray) -> np.ndarray:
        """Get indices that would sort fitness array (best first)."""
        if self.objective == 'minimize':
            return np.argsort(fitness_array)  # Ascending order
        else:
            return np.argsort(fitness_array)[::-1]  # Descending order

    def _is_better(self, new_fitness: float, old_fitness: float) -> bool:
        """Check if new fitness is better than old fitness based on objective."""
        if self.objective == 'minimize':
            return new_fitness < old_fitness
        else:
            return new_fitness > old_fitness

    def _apply_bounds(self, solution: np.ndarray) -> np.ndarray:
        """Ensure solution stays within bounds."""
        bounded_solution = solution.copy()
        for d in range(self.dimensions):
            lower, upper = self.bounds[d]
            bounded_solution[d] = np.clip(solution[d], lower, upper)
        return bounded_solution

    def _evaluate(self, solution: np.ndarray) -> float:
        """Evaluate fitness function at given solution."""
        try:
            result = self.fitness_function(solution)
            if not isinstance(result, (int, float, np.number)):
                raise ValueError(f"Fitness function must return a numeric value, got {type(result)}")
            if np.isnan(result) or np.isinf(result):
                raise ValueError(f"Fitness function returned invalid value: {result}")
            return float(result)
        except Exception as e:
            raise RuntimeError(f"Error evaluating fitness function at solution {solution}: {str(e)}")
