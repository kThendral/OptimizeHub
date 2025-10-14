"""
Pydantic models for optimization problem input validation.
"""
from typing import List, Tuple, Optional, Literal, Dict, Any
from pydantic import BaseModel, Field, field_validator


class ProblemInput(BaseModel):
    """
    Optimization problem definition.

    This model defines the problem structure that users submit to the API.
    The fitness_function field is handled separately at runtime since it cannot
    be serialized in JSON.
    """
    dimensions: int = Field(
        ...,
        ge=1,
        le=50,
        description="Number of dimensions in the optimization problem (1-50)"
    )

    bounds: List[Tuple[float, float]] = Field(
        ...,
        description="List of (lower, upper) bound tuples for each dimension"
    )

    objective: Literal["minimize", "maximize"] = Field(
        default="minimize",
        description="Optimization objective: 'minimize' or 'maximize'"
    )

    fitness_function_name: Optional[str] = Field(
        default=None,
        description="Name of the fitness function (e.g., 'sphere', 'rastrigin', 'rosenbrock')"
    )

    # Real-world problem support
    problem_type: Optional[str] = Field(
        default=None,
        description="Type of problem: 'knapsack', 'tsp', or None for benchmarks"
    )

    # Knapsack problem specific fields
    items: Optional[List[Dict[str, Any]]] = Field(
        default=None,
        description="List of items for knapsack problem with {name, weight, value}"
    )

    capacity: Optional[float] = Field(
        default=None,
        description="Maximum capacity for knapsack problem"
    )

    # TSP problem specific fields
    cities: Optional[List[Dict[str, Any]]] = Field(
        default=None,
        description="List of cities for TSP with {name, x, y}"
    )

    @field_validator('bounds')
    @classmethod
    def validate_bounds(cls, v, info):
        """Validate bounds structure and values."""
        # For real-world problems, bounds will be set by the executor
        if info.data.get('problem_type') in ['knapsack', 'tsp']:
            # Bounds will be automatically set to [0, 1] for each dimension
            return v if v else []
        
        if 'dimensions' not in info.data:
            return v

        dimensions = info.data['dimensions']

        # Check length matches dimensions
        if len(v) != dimensions:
            raise ValueError(
                f"Bounds length ({len(v)}) must match dimensions ({dimensions})"
            )

        # Validate each bound
        for i, bound in enumerate(v):
            if len(bound) != 2:
                raise ValueError(
                    f"Bound at index {i} must be a tuple of (lower, upper), got {bound}"
                )

            lower, upper = bound

            if not isinstance(lower, (int, float)) or not isinstance(upper, (int, float)):
                raise ValueError(
                    f"Bound at index {i} must contain numeric values, got {bound}"
                )

            if lower >= upper:
                raise ValueError(
                    f"Invalid bound at index {i}: lower ({lower}) must be < upper ({upper})"
                )

        return v

    class Config:
        json_schema_extra = {
            "example": {
                "dimensions": 2,
                "bounds": [[-5.0, 5.0], [-5.0, 5.0]],
                "objective": "minimize",
                "fitness_function_name": "sphere"
            }
        }


class AlgorithmParams(BaseModel):
    """Base model for algorithm parameters."""
    max_iterations: int = Field(
        default=50,
        ge=1,
        le=100,
        description="Maximum number of iterations (1-100)"
    )


class PSOParams(AlgorithmParams):
    """Parameters specific to Particle Swarm Optimization."""
    swarm_size: int = Field(
        default=30,
        ge=10,
        description="Number of particles in the swarm (minimum 10)"
    )

    w: float = Field(
        default=0.7,
        description="Inertia weight"
    )

    c1: float = Field(
        default=1.5,
        description="Cognitive coefficient"
    )

    c2: float = Field(
        default=1.5,
        description="Social coefficient"
    )

    @field_validator('c2')
    @classmethod
    def validate_coefficients(cls, v, info):
        """Both c1 and c2 cannot be zero."""
        if 'c1' in info.data:
            if info.data['c1'] == 0 and v == 0:
                raise ValueError(
                    "Both c1 and c2 cannot be zero - particles would not move"
                )
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "swarm_size": 30,
                "max_iterations": 50,
                "w": 0.7,
                "c1": 1.5,
                "c2": 1.5
            }
        }


class GAParams(AlgorithmParams):
    """Parameters specific to Genetic Algorithm."""
    population_size: int = Field(
        default=50,
        ge=10,
        description="Number of individuals in the population (minimum 10)"
    )

    crossover_rate: float = Field(
        default=0.8,
        ge=0.0,
        le=1.0,
        description="Probability of crossover (0.0-1.0)"
    )

    mutation_rate: float = Field(
        default=0.1,
        ge=0.0,
        le=1.0,
        description="Probability of mutation (0.0-1.0)"
    )

    tournament_size: int = Field(
        default=3,
        ge=2,
        description="Tournament selection size (minimum 2)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "population_size": 50,
                "max_iterations": 50,
                "crossover_rate": 0.8,
                "mutation_rate": 0.1,
                "tournament_size": 3
            }
        }


class OptimizationRequest(BaseModel):
    """
    Complete optimization request combining problem and algorithm selection.
    """
    algorithm: str = Field(
        ...,
        description="Algorithm name: 'particle_swarm', 'genetic_algorithm', etc."
    )

    problem: ProblemInput = Field(
        ...,
        description="Problem definition"
    )

    params: dict = Field(
        default_factory=dict,
        description="Algorithm-specific parameters"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "algorithm": "particle_swarm",
                "problem": {
                    "dimensions": 2,
                    "bounds": [[-5.0, 5.0], [-5.0, 5.0]],
                    "objective": "minimize",
                    "fitness_function_name": "sphere"
                },
                "params": {
                    "swarm_size": 30,
                    "max_iterations": 50,
                    "w": 0.7,
                    "c1": 1.5,
                    "c2": 1.5
                }
            }
        }
