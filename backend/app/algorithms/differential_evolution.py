"""
Differential Evolution (DE) - base-class compatible implementation

Variant: default DE/rand/1/bin, configurable strategies.
Compatible with OptimizationAlgorithm base class.
"""

import numpy as np
import time
from typing import Any, Dict
from .base import OptimizationAlgorithm


class DifferentialEvolution(OptimizationAlgorithm):
    """Differential Evolution (configurable DE/rand/1/bin)."""

    def __init__(self, problem: Dict[str, Any], params: Dict[str, Any]):
        super().__init__(problem, params)

        # Problem validation
        self._validate_problem_schema(problem)
        self.dimensions = problem['dimensions']
        self.bounds = np.array(problem['bounds'], dtype=float)
        self.fitness_function = problem['fitness_function']
        self.objective = problem.get('objective', 'minimize')

        # Algorithm parameters
        self.population_size = params.get('population_size', 50)
        self.max_iterations = params.get('max_iterations', 50)
        self.F = params.get('F', 0.8)
        self.CR = params.get('CR', 0.9)
        self.strategy = params.get('strategy', 'rand/1/bin')
        self.boundary_handling = params.get('boundary_handling', 'clip')
        self.timeout = params.get('timeout', 30)

        # Validate parameters
        self._validate_parameters()

        # Internal state
        self.population = None
        self.fitness_values = None
        self.best_individual = None
        self.best_fitness = None
        self.start_time = None

    # --------------------------- Base-class compatible initialize ---------------------------
    def initialize(self):
        """Setup initial population (required by base class)."""
        lower, upper = self.bounds[:, 0], self.bounds[:, 1]
        self.population = np.zeros((self.population_size, self.dimensions))
        for i in range(self.population_size):
            for d in range(self.dimensions):
                self.population[i, d] = np.random.uniform(lower[d], upper[d])
        self.fitness_values = np.array([self._evaluate(ind) for ind in self.population])

        if self.objective == 'minimize':
            best_idx = np.argmin(self.fitness_values)
        else:
            best_idx = np.argmax(self.fitness_values)

        self.best_individual = self.population[best_idx].copy()
        self.best_fitness = self.fitness_values[best_idx]
        self.best_solution = self.best_individual.tolist()
        self.convergence_curve = [float(self.best_fitness)]
        self.start_time = time.time()

    # --------------------------- Validation ---------------------------
    def _validate_problem_schema(self, problem: Dict[str, Any]):
        required = ['dimensions', 'bounds', 'fitness_function']
        for r in required:
            if r not in problem:
                raise ValueError(f"Problem missing required key: '{r}'")

        if not isinstance(problem['dimensions'], int) or problem['dimensions'] <= 0:
            raise ValueError("'dimensions' must be a positive integer")

        bounds = problem['bounds']
        if len(bounds) != problem['dimensions']:
            raise ValueError("Length of 'bounds' must equal 'dimensions'")

        for i, b in enumerate(bounds):
            if not isinstance(b, (list, tuple)) or len(b) != 2:
                raise ValueError(f"Bound at index {i} must be (lower, upper)")
            lower, upper = b
            if not (isinstance(lower, (int, float)) and isinstance(upper, (int, float))):
                raise ValueError(f"Bound values must be numeric at index {i}")
            if lower >= upper:
                raise ValueError(f"Invalid bound at {i}: lower >= upper")

        if not callable(problem['fitness_function']):
            raise ValueError("'fitness_function' must be callable")

        if problem.get('objective', 'minimize') not in ['minimize', 'maximize']:
            raise ValueError("'objective' must be 'minimize' or 'maximize'")

    def _validate_parameters(self):
        if not isinstance(self.population_size, int) or self.population_size < 10:
            raise ValueError("population_size must be >= 10")
        if not isinstance(self.max_iterations, int) or self.max_iterations < 1:
            raise ValueError("max_iterations must be >= 1")
        if not (0.0 < self.F <= 2.0):
            raise ValueError("F must be in (0, 2]")
        if not (0.0 <= self.CR <= 1.0):
            raise ValueError("CR must be in [0, 1]")
        if self.strategy not in ['rand/1/bin', 'best/1/bin', 'rand/2/bin']:
            raise ValueError("strategy must be 'rand/1/bin', 'best/1/bin', or 'rand/2/bin'")
        if self.boundary_handling not in ['clip', 'reflect', 'wrap']:
            raise ValueError("boundary_handling must be 'clip', 'reflect', or 'wrap'")
        if not isinstance(self.timeout, (int, float)) or self.timeout <= 0:
            raise ValueError("timeout must be positive number")

    # --------------------------- Utils ---------------------------
    def _evaluate(self, individual: np.ndarray) -> float:
        try:
            val = self.fitness_function(individual)
            if not isinstance(val, (int, float, np.number)):
                raise ValueError(f"Fitness function must return numeric scalar")
            if np.isnan(val) or np.isinf(val):
                raise ValueError("Fitness function returned NaN or Inf")
            return float(val)
        except Exception as e:
            raise RuntimeError(f"Error evaluating individual {individual}: {e}")

    def _apply_boundary(self, vec: np.ndarray) -> np.ndarray:
        lower, upper = self.bounds[:, 0], self.bounds[:, 1]
        if self.boundary_handling == 'clip':
            return np.clip(vec, lower, upper)
        if self.boundary_handling == 'reflect':
            reflected = vec.copy()
            for i in range(self.dimensions):
                if reflected[i] < lower[i]:
                    reflected[i] = lower[i] + (lower[i] - reflected[i])
                if reflected[i] > upper[i]:
                    reflected[i] = upper[i] - (reflected[i] - upper[i])
            return np.clip(reflected, lower, upper)
        # wrap
        return lower + ((vec - lower) % (upper - lower))

    # --------------------------- Mutation Strategies ---------------------------
    def _mutate_rand_1(self, i):
        idxs = [idx for idx in range(self.population_size) if idx != i]
        a, b, c = self.population[np.random.choice(idxs, 3, replace=False)]
        return a + self.F * (b - c)

    def _mutate_best_1(self, i):
        idxs = [idx for idx in range(self.population_size) if idx != i]
        b, c = self.population[np.random.choice(idxs, 2, replace=False)]
        return self.best_individual + self.F * (b - c)

    def _mutate_rand_2(self, i):
        idxs = [idx for idx in range(self.population_size) if idx != i]
        a, b, c, d, e = self.population[np.random.choice(idxs, 5, replace=False)]
        return a + self.F * (b - c + d - e)

    # --------------------------- Core Optimization Loop ---------------------------
    def optimize(self):
        """Run the DE optimization loop."""
        if self.population is None:
            self.initialize()
        self.start_time = time.time()

        for iteration in range(self.max_iterations):
            if time.time() - self.start_time > self.timeout:
                break

            for i in range(self.population_size):
                # Mutation
                if self.strategy == 'rand/1/bin':
                    mutant = self._mutate_rand_1(i)
                elif self.strategy == 'best/1/bin':
                    mutant = self._mutate_best_1(i)
                else:  # rand/2/bin
                    mutant = self._mutate_rand_2(i)

                mutant = self._apply_boundary(mutant)

                # Binomial crossover
                cross_mask = np.random.rand(self.dimensions) < self.CR
                if not np.any(cross_mask):
                    cross_mask[np.random.randint(0, self.dimensions)] = True
                trial = np.where(cross_mask, mutant, self.population[i])
                trial = self._apply_boundary(trial)

                trial_fitness = self._evaluate(trial)

                # Selection
                better = (
                    trial_fitness < self.fitness_values[i]
                    if self.objective == 'minimize'
                    else trial_fitness > self.fitness_values[i]
                )

                if better:
                    self.population[i] = trial
                    self.fitness_values[i] = trial_fitness

                    if (
                        trial_fitness < self.best_fitness
                        if self.objective == 'minimize'
                        else trial_fitness > self.best_fitness
                    ):
                        self.best_fitness = trial_fitness
                        self.best_individual = trial.copy()
                        self.best_solution = self.best_individual.tolist()

            self.convergence_curve.append(float(self.best_fitness))

        return self.get_results(iteration + 1 if 'iteration' in locals() else 0)


    # --------------------------- Results ---------------------------
    def get_results(self, iterations: int = None) -> Dict[str, Any]:
        if iterations is None:
            iterations = self.max_iterations  # fallback
        return {
            "algorithm": f"DE/{self.strategy} (CR={self.CR}, F={self.F})",
            "best_solution": self.best_solution,
            "best_fitness": float(self.best_fitness),
            "convergence_curve": self.convergence_curve,
            "params": self.params,
            "iterations": iterations,
            "elapsed_time": time.time() - (self.start_time or time.time()),
            "status": "success"
        }



