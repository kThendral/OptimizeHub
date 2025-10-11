import numpy as np
import time
from typing import Any, Dict, List, Tuple
from .base import OptimizationAlgorithm


class ParticleSwarmOptimization(OptimizationAlgorithm):
    """
    Particle Swarm Optimization (PSO) implementation.

    PSO is a population-based metaheuristic inspired by social behavior of birds.
    Each particle has a position and velocity, and moves through the search space
    influenced by its own best position and the global best position.
    """

    def __init__(self, problem: Dict[str, Any], params: Dict[str, Any]):
        super().__init__(problem, params)

        # Validate problem schema
        self._validate_problem_schema(problem)

        # PSO parameters with defaults (NO auto-correction)
        self.swarm_size = params.get('swarm_size', 30)
        self.max_iterations = params.get('max_iterations', 50)
        self.w = params.get('w', 0.7)  # Inertia weight
        self.c1 = params.get('c1', 1.5)  # Cognitive coefficient
        self.c2 = params.get('c2', 1.5)  # Social coefficient

        # Validate PSO parameters (explicit errors, no silent fixes)
        self._validate_parameters()

        # Problem parameters
        self.dimensions = problem['dimensions']
        self.bounds = problem['bounds']
        self.objective = problem.get('objective', 'minimize')
        self.fitness_function = problem['fitness_function']

        # PSO state variables
        self.positions = None
        self.velocities = None
        self.personal_best_positions = None
        self.personal_best_scores = None
        self.global_best_position = None
        self.global_best_score = None

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
        """
        Validate PSO-specific parameters with explicit errors (no silent corrections).

        Research notes:
        - Negative inertia weight: Recent research (ACM 2022) shows negative w can work
          in mirror-image strategies, but standard PSO uses w ∈ (0, 1.2)
        - c1=0 or c2=0: Valid for social-only or cognition-only variants
        - Negative c1/c2: Not standard, but we allow for research flexibility
        """
        # Swarm size: Minimum 10 for viable PSO behavior
        # Size 1 is random search, sizes 2-9 don't exhibit swarm intelligence
        if not isinstance(self.swarm_size, int) or self.swarm_size < 10:
            raise ValueError(
                f"swarm_size must be ≥10 for viable PSO behavior (got {self.swarm_size}). "
                f"Sizes < 10 don't exhibit proper swarm intelligence."
            )

        # Iterations: Hard limit for SaaS platform (can be tier-based)
        if not isinstance(self.max_iterations, int) or self.max_iterations < 1:
            raise ValueError(f"max_iterations must be ≥1, got {self.max_iterations}")

        if self.max_iterations > 100:
            raise ValueError(
                f"max_iterations limited to 100 (platform constraint), got {self.max_iterations}. "
                f"Contact support for higher limits."
            )

        # Inertia weight: Warn about unconventional values but allow for research
        if not isinstance(self.w, (int, float)):
            raise ValueError(f"Inertia weight (w) must be numeric, got {type(self.w)}")

        # Standard PSO uses w ∈ [0.4, 1.2], but we allow wider range with warnings
        if self.w < 0:
            # Negative w is non-standard but used in some research (mirror-image PSO)
            pass  # Allow but document in logs/warnings if needed
        elif self.w >= 1.0:
            # w ≥ 1 can cause divergence, but some adaptive schemes use it temporarily
            pass  # Allow but user should know risks

        # Acceleration coefficients: Allow wide range including zero and negative
        # c1=0: social-only PSO, c2=0: cognition-only PSO (both valid variants)
        if not isinstance(self.c1, (int, float)):
            raise ValueError(f"Cognitive coefficient (c1) must be numeric, got {type(self.c1)}")

        if not isinstance(self.c2, (int, float)):
            raise ValueError(f"Social coefficient (c2) must be numeric, got {type(self.c2)}")

        # Both zero is invalid - no movement
        if self.c1 == 0 and self.c2 == 0:
            raise ValueError(
                "Both c1 and c2 cannot be zero - particles would not move. "
                "Use c1>0 for cognition-only or c2>0 for social-only PSO."
            )

    def initialize(self):
        """Initialize swarm with random positions and velocities."""
        # Initialize positions within bounds
        self.positions = np.zeros((self.swarm_size, self.dimensions))
        self.velocities = np.zeros((self.swarm_size, self.dimensions))

        for d in range(self.dimensions):
            lower, upper = self.bounds[d]
            self.positions[:, d] = np.random.uniform(lower, upper, self.swarm_size)

            # Initialize velocities to small random values
            velocity_range = (upper - lower) * 0.1
            self.velocities[:, d] = np.random.uniform(-velocity_range, velocity_range, self.swarm_size)

        # Evaluate initial positions
        self.personal_best_positions = self.positions.copy()
        self.personal_best_scores = np.array([self._evaluate(p) for p in self.positions])

        # Set global best
        if self.objective == 'minimize':
            best_idx = np.argmin(self.personal_best_scores)
        else:
            best_idx = np.argmax(self.personal_best_scores)

        self.global_best_position = self.personal_best_positions[best_idx].copy()
        self.global_best_score = self.personal_best_scores[best_idx]
        self.best_solution = self.global_best_position.tolist()

        # Record initial convergence
        self.convergence_curve.append(float(self.global_best_score))

    def optimize(self):
        """Execute PSO optimization loop."""
        self.start_time = time.time()

        for iteration in range(self.max_iterations):
            # Check timeout
            if time.time() - self.start_time > self.timeout:
                break

            # Update velocities and positions
            for i in range(self.swarm_size):
                # Random coefficients
                r1 = np.random.random(self.dimensions)
                r2 = np.random.random(self.dimensions)

                # Velocity update
                cognitive = self.c1 * r1 * (self.personal_best_positions[i] - self.positions[i])
                social = self.c2 * r2 * (self.global_best_position - self.positions[i])
                self.velocities[i] = self.w * self.velocities[i] + cognitive + social

                # Position update
                self.positions[i] = self.positions[i] + self.velocities[i]

                # Apply bounds
                self.positions[i] = self._apply_bounds(self.positions[i])

            # Evaluate new positions
            for i in range(self.swarm_size):
                fitness = self._evaluate(self.positions[i])

                # Update personal best
                if self._is_better(fitness, self.personal_best_scores[i]):
                    self.personal_best_positions[i] = self.positions[i].copy()
                    self.personal_best_scores[i] = fitness

                    # Update global best
                    if self._is_better(fitness, self.global_best_score):
                        self.global_best_position = self.positions[i].copy()
                        self.global_best_score = fitness
                        self.best_solution = self.global_best_position.tolist()

            # Record convergence
            self.convergence_curve.append(float(self.global_best_score))

    def _evaluate(self, position: np.ndarray) -> float:
        """Evaluate fitness function at given position."""
        try:
            result = self.fitness_function(position)
            if not isinstance(result, (int, float, np.number)):
                raise ValueError(f"Fitness function must return a numeric value, got {type(result)}")
            if np.isnan(result) or np.isinf(result):
                raise ValueError(f"Fitness function returned invalid value: {result}")
            return float(result)
        except Exception as e:
            raise RuntimeError(f"Error evaluating fitness function at position {position}: {str(e)}")

    def _apply_bounds(self, position: np.ndarray) -> np.ndarray:
        """Ensure position stays within bounds."""
        bounded_position = position.copy()
        for d in range(self.dimensions):
            lower, upper = self.bounds[d]
            bounded_position[d] = np.clip(position[d], lower, upper)
        return bounded_position

    def _is_better(self, new_fitness: float, old_fitness: float) -> bool:
        """Check if new fitness is better than old fitness based on objective."""
        if self.objective == 'minimize':
            return new_fitness < old_fitness
        else:
            return new_fitness > old_fitness
