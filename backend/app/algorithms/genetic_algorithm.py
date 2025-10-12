"""
Genetic Algorithm implementation for continuous optimization problems.

Genetic Algorithm (GA) is an evolutionary computation technique inspired by 
natural selection. It evolves a population of candidate solutions through
selection, crossover, and mutation operators.
"""

import numpy as np
import time
from typing import Any, Dict, List, Tuple
from .base import OptimizationAlgorithm


class GeneticAlgorithm(OptimizationAlgorithm):
    """
    Genetic Algorithm implementation for continuous optimization.
    
    Uses real-valued encoding with tournament selection, simulated binary crossover,
    and polynomial mutation for continuous optimization problems.
    """

    def __init__(self, problem: Dict[str, Any], params: Dict[str, Any]):
        super().__init__(problem, params)
        
        # Validate problem schema
        self._validate_problem_schema(problem)
        
        # GA parameters with defaults
        self.population_size = params.get('population_size', 50)
        self.max_iterations = params.get('max_iterations', 50)
        self.crossover_rate = params.get('crossover_rate', 0.8)
        self.mutation_rate = params.get('mutation_rate', 0.1)
        self.tournament_size = params.get('tournament_size', 3)
        
        # Validate GA parameters
        self._validate_parameters()
        
        # Problem parameters
        self.dimensions = problem['dimensions']
        self.bounds = problem['bounds']
        self.objective = problem.get('objective', 'minimize')
        self.fitness_function = problem['fitness_function']
        
        # GA state variables
        self.population = None
        self.fitness_values = None
        self.best_individual = None
        self.best_fitness = None
        
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
        """Validate GA-specific parameters."""
        # Population size
        if not isinstance(self.population_size, int) or self.population_size < 10:
            raise ValueError(
                f"population_size must be ≥10 for viable GA behavior (got {self.population_size}). "
                f"Small populations don't provide sufficient genetic diversity."
            )

        # Iterations
        if not isinstance(self.max_iterations, int) or self.max_iterations < 1:
            raise ValueError(f"max_iterations must be ≥1, got {self.max_iterations}")

        if self.max_iterations > 100:
            raise ValueError(
                f"max_iterations limited to 100 (platform constraint), got {self.max_iterations}. "
                f"Contact support for higher limits."
            )

        # Crossover rate
        if not isinstance(self.crossover_rate, (int, float)):
            raise ValueError(f"crossover_rate must be numeric, got {type(self.crossover_rate)}")
        
        if not (0.0 <= self.crossover_rate <= 1.0):
            raise ValueError(f"crossover_rate must be between 0.0 and 1.0, got {self.crossover_rate}")

        # Mutation rate
        if not isinstance(self.mutation_rate, (int, float)):
            raise ValueError(f"mutation_rate must be numeric, got {type(self.mutation_rate)}")
        
        if not (0.0 <= self.mutation_rate <= 1.0):
            raise ValueError(f"mutation_rate must be between 0.0 and 1.0, got {self.mutation_rate}")

        # Tournament size
        if not isinstance(self.tournament_size, int):
            raise ValueError(f"tournament_size must be an integer, got {type(self.tournament_size)}")
        
        if self.tournament_size < 2:
            raise ValueError(f"tournament_size must be ≥2, got {self.tournament_size}")
        
        if self.tournament_size > self.population_size:
            raise ValueError(
                f"tournament_size ({self.tournament_size}) cannot exceed population_size ({self.population_size})"
            )

    def initialize(self):
        """Initialize population with random individuals."""
        # Create random population within bounds
        self.population = np.zeros((self.population_size, self.dimensions))
        
        for i in range(self.population_size):
            for d in range(self.dimensions):
                lower, upper = self.bounds[d]
                self.population[i, d] = np.random.uniform(lower, upper)
        
        # Evaluate initial population
        self.fitness_values = np.array([self._evaluate(individual) for individual in self.population])
        
        # Find best individual
        if self.objective == 'minimize':
            best_idx = np.argmin(self.fitness_values)
        else:
            best_idx = np.argmax(self.fitness_values)
        
        self.best_individual = self.population[best_idx].copy()
        self.best_fitness = self.fitness_values[best_idx]
        self.best_solution = self.best_individual.tolist()
        
        # Record initial convergence
        self.convergence_curve.append(float(self.best_fitness))

    def optimize(self):
        """Execute GA optimization loop."""
        self.start_time = time.time()
        
        for generation in range(self.max_iterations):
            # Check timeout
            if time.time() - self.start_time > self.timeout:
                break
            
            # Create new population
            new_population = []
            
            # Generate offspring
            while len(new_population) < self.population_size:
                # Selection
                parent1 = self._tournament_selection()
                parent2 = self._tournament_selection()
                
                # Crossover
                if np.random.random() < self.crossover_rate:
                    child1, child2 = self._simulated_binary_crossover(parent1, parent2)
                else:
                    child1, child2 = parent1.copy(), parent2.copy()
                
                # Mutation
                child1 = self._polynomial_mutation(child1)
                child2 = self._polynomial_mutation(child2)
                
                # Apply bounds
                child1 = self._apply_bounds(child1)
                child2 = self._apply_bounds(child2)
                
                new_population.extend([child1, child2])
            
            # Trim to exact population size if needed
            new_population = new_population[:self.population_size]
            self.population = np.array(new_population)
            
            # Evaluate new population
            self.fitness_values = np.array([self._evaluate(individual) for individual in self.population])
            
            # Update best solution
            if self.objective == 'minimize':
                current_best_idx = np.argmin(self.fitness_values)
                current_best_fitness = self.fitness_values[current_best_idx]
                if current_best_fitness < self.best_fitness:
                    self.best_fitness = current_best_fitness
                    self.best_individual = self.population[current_best_idx].copy()
                    self.best_solution = self.best_individual.tolist()
            else:
                current_best_idx = np.argmax(self.fitness_values)
                current_best_fitness = self.fitness_values[current_best_idx]
                if current_best_fitness > self.best_fitness:
                    self.best_fitness = current_best_fitness
                    self.best_individual = self.population[current_best_idx].copy()
                    self.best_solution = self.best_individual.tolist()
            
            # Record convergence
            self.convergence_curve.append(float(self.best_fitness))

    def _tournament_selection(self) -> np.ndarray:
        """Tournament selection to choose a parent."""
        # Select random individuals for tournament
        tournament_indices = np.random.choice(self.population_size, self.tournament_size, replace=False)
        tournament_fitness = self.fitness_values[tournament_indices]
        
        # Find winner based on objective
        if self.objective == 'minimize':
            winner_idx = tournament_indices[np.argmin(tournament_fitness)]
        else:
            winner_idx = tournament_indices[np.argmax(tournament_fitness)]
        
        return self.population[winner_idx].copy()

    def _simulated_binary_crossover(self, parent1: np.ndarray, parent2: np.ndarray, eta_c: float = 20.0) -> Tuple[np.ndarray, np.ndarray]:
        """Simulated Binary Crossover (SBX) for real-valued vectors."""
        child1 = parent1.copy()
        child2 = parent2.copy()
        
        for i in range(self.dimensions):
            if np.random.random() <= 0.5:  # 50% chance to crossover each gene
                if abs(parent1[i] - parent2[i]) > 1e-14:
                    # Calculate beta
                    u = np.random.random()
                    if u <= 0.5:
                        beta = (2 * u) ** (1.0 / (eta_c + 1))
                    else:
                        beta = (1.0 / (2 * (1 - u))) ** (1.0 / (eta_c + 1))
                    
                    # Generate offspring
                    child1[i] = 0.5 * ((1 + beta) * parent1[i] + (1 - beta) * parent2[i])
                    child2[i] = 0.5 * ((1 - beta) * parent1[i] + (1 + beta) * parent2[i])
        
        return child1, child2

    def _polynomial_mutation(self, individual: np.ndarray, eta_m: float = 20.0) -> np.ndarray:
        """Polynomial mutation for real-valued vectors."""
        mutated = individual.copy()
        
        for i in range(self.dimensions):
            if np.random.random() < self.mutation_rate:
                lower, upper = self.bounds[i]
                
                # Calculate delta
                u = np.random.random()
                if u < 0.5:
                    delta = (2 * u) ** (1.0 / (eta_m + 1)) - 1
                else:
                    delta = 1 - (2 * (1 - u)) ** (1.0 / (eta_m + 1))
                
                # Apply mutation
                mutated[i] = individual[i] + delta * (upper - lower)
        
        return mutated

    def _apply_bounds(self, individual: np.ndarray) -> np.ndarray:
        """Ensure individual stays within bounds."""
        bounded_individual = individual.copy()
        for d in range(self.dimensions):
            lower, upper = self.bounds[d]
            bounded_individual[d] = np.clip(individual[d], lower, upper)
        return bounded_individual

    def _evaluate(self, individual: np.ndarray) -> float:
        """Evaluate fitness function for an individual."""
        try:
            result = self.fitness_function(individual)
            if not isinstance(result, (int, float, np.number)):
                raise ValueError(f"Fitness function must return a numeric value, got {type(result)}")
            if np.isnan(result) or np.isinf(result):
                raise ValueError(f"Fitness function returned invalid value: {result}")
            return float(result)
        except Exception as e:
            raise RuntimeError(f"Error evaluating fitness function for individual {individual}: {str(e)}")
