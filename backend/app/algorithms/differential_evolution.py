import numpy as np
import time
from typing import Any, Dict
from .base import OptimizationAlgorithm


class DifferentialEvolution(OptimizationAlgorithm):
    """
    Differential Evolution optimization algorithm for continuous domains.
    """

    def __init__(self, problem: Dict[str, Any], params: Dict[str, Any]):
        super().__init__(problem, params)

        # Extract DE parameters (with reasonable defaults)
        self.population_size = params.get("population_size", 50)
        self.max_iterations = min(params.get("max_iterations", 50), 100)
        self.F = params.get("F", 0.8)   # Differential weight
        self.CR = params.get("CR", 0.9) # Crossover probability

        # Problem setup
        self.dimensions = problem["dimensions"]
        self.bounds = np.array(problem["bounds"])
        self.fitness_function = problem["fitness_function"]
        self.objective = problem.get("objective", "minimize")

        # Internal trackers
        self.population = None
        self.fitness = None
        self.best_solution = None
        self.best_fitness = None
        self.convergence = []
        self.start_time = None

    def initialize(self):
        """Initialize population uniformly within bounds and evaluate fitness."""
        lower, upper = self.bounds[:, 0], self.bounds[:, 1]
        self.population = np.random.uniform(lower, upper, (self.population_size, self.dimensions))
        self.fitness = np.array([self.fitness_function(ind) for ind in self.population])

        best_idx = np.argmin(self.fitness)
        self.best_solution = self.population[best_idx].copy()
        self.best_fitness = self.fitness[best_idx]
        self.convergence = [self.best_fitness]
        self.start_time = time.time()

    def optimize(self):
        """Run Differential Evolution optimization loop."""
        self.initialize()
        lower, upper = self.bounds[:, 0], self.bounds[:, 1]

        for iteration in range(self.max_iterations):
            for i in range(self.population_size):
                # Choose 3 random distinct indices not equal to i
                idxs = [idx for idx in range(self.population_size) if idx != i]
                a, b, c = self.population[np.random.choice(idxs, 3, replace=False)]

                # Mutation (DE/rand/1)
                mutant = a + self.F * (b - c)
                mutant = np.clip(mutant, lower, upper)

                # Crossover
                cross_points = np.random.rand(self.dimensions) < self.CR
                if not np.any(cross_points):
                    cross_points[np.random.randint(0, self.dimensions)] = True
                trial = np.where(cross_points, mutant, self.population[i])

                # Selection
                trial_fitness = self.fitness_function(trial)
                if trial_fitness < self.fitness[i]:
                    self.population[i] = trial
                    self.fitness[i] = trial_fitness

                    if trial_fitness < self.best_fitness:
                        self.best_fitness = trial_fitness
                        self.best_solution = trial.copy()

            self.convergence.append(self.best_fitness)

            # Timeout safeguard (30 seconds)
            if time.time() - self.start_time > 30:
                break

        return self.get_results(iteration + 1)

    def get_results(self, iterations: int) -> Dict[str, Any]:
        """Return standardized output for API response."""
        return {
            "best_position": self.best_solution.tolist(),
            "best_fitness": float(self.best_fitness),
            "convergence": self.convergence,
            "iterations": iterations,
            "status": "success"
        }
