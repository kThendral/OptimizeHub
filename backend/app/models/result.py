"""
Pydantic models for optimization algorithm output.
"""
from typing import List, Any, Optional
from pydantic import BaseModel, Field


class OptimizationResult(BaseModel):
    """
    Standard result format for all optimization algorithms.

    This model ensures consistent output structure across all algorithms,
    making it easier for frontend developers to integrate and visualize results.
    """
    algorithm: str = Field(
        ...,
        description="Name of the algorithm that produced these results"
    )

    status: str = Field(
        ...,
        description="Execution status: 'success', 'error', 'not_implemented', 'timeout'"
    )

    best_solution: Optional[List[float]] = Field(
        None,
        description="Best solution found (list of coordinates)"
    )

    best_fitness: Optional[float] = Field(
        None,
        description="Fitness value of the best solution"
    )

    convergence_curve: Optional[List[float]] = Field(
        None,
        description="Best fitness value at each iteration"
    )

    params: Optional[dict] = Field(
        None,
        description="Algorithm parameters used for this run"
    )

    iterations_completed: Optional[int] = Field(
        None,
        description="Number of iterations completed"
    )

    execution_time: Optional[float] = Field(
        None,
        description="Execution time in seconds"
    )

    error_message: Optional[str] = Field(
        None,
        description="Error message if status is 'error'"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "algorithm": "ParticleSwarmOptimization",
                "status": "success",
                "best_solution": [0.001, -0.002],
                "best_fitness": 0.000005,
                "convergence_curve": [10.5, 5.2, 2.1, 0.5, 0.1, 0.000005],
                "params": {
                    "swarm_size": 30,
                    "max_iterations": 50,
                    "w": 0.7,
                    "c1": 1.5,
                    "c2": 1.5
                },
                "iterations_completed": 50,
                "execution_time": 1.23
            }
        }


class ValidationResult(BaseModel):
    """Result of problem validation without running optimization."""
    valid: bool = Field(
        ...,
        description="Whether the problem definition is valid"
    )

    errors: Optional[List[str]] = Field(
        None,
        description="List of validation errors if any"
    )

    warnings: Optional[List[str]] = Field(
        None,
        description="List of warnings (non-blocking issues)"
    )

    problem_summary: Optional[dict] = Field(
        None,
        description="Summary of the validated problem"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "valid": True,
                "errors": None,
                "warnings": ["Dimension count is high (45), may increase computation time"],
                "problem_summary": {
                    "dimensions": 2,
                    "objective": "minimize",
                    "bounds_range": "[-5.0, 5.0] for all dimensions"
                }
            }
        }


class AlgorithmInfo(BaseModel):
    """Information about a specific algorithm."""
    name: str = Field(
        ...,
        description="Internal algorithm name (e.g., 'particle_swarm')"
    )

    display_name: str = Field(
        ...,
        description="Human-readable name (e.g., 'Particle Swarm Optimization')"
    )

    status: str = Field(
        ...,
        description="Implementation status: 'available' or 'coming_soon'"
    )

    description: str = Field(
        ...,
        description="Brief description of the algorithm"
    )

    use_cases: Optional[List[str]] = Field(
        None,
        description="List of common use cases for this algorithm"
    )

    default_params: dict = Field(
        ...,
        description="Default parameter values"
    )

    parameter_info: Optional[dict] = Field(
        None,
        description="Detailed information about parameters"
    )

    implementation_status: Optional[str] = Field(
        None,
        description="Human-readable implementation status message"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "name": "particle_swarm",
                "display_name": "Particle Swarm Optimization",
                "status": "available",
                "description": "Bio-inspired algorithm simulating social behavior of birds",
                "default_params": {
                    "swarm_size": 30,
                    "max_iterations": 50,
                    "w": 0.7,
                    "c1": 1.5,
                    "c2": 1.5
                }
            }
        }


class AlgorithmListResponse(BaseModel):
    """Response for listing all algorithms."""
    total: int = Field(
        ...,
        description="Total number of algorithms"
    )

    available: int = Field(
        ...,
        description="Number of available algorithms"
    )

    coming_soon: int = Field(
        ...,
        description="Number of algorithms in development"
    )

    algorithms: List[AlgorithmInfo] = Field(
        ...,
        description="List of all algorithms with their details"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "total": 5,
                "available": 2,
                "coming_soon": 3,
                "algorithms": [
                    {
                        "name": "particle_swarm",
                        "display_name": "Particle Swarm Optimization",
                        "status": "available",
                        "description": "Bio-inspired algorithm simulating social behavior",
                        "default_params": {"swarm_size": 30, "max_iterations": 50}
                    }
                ]
            }
        }


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = Field(
        ...,
        description="Service health status"
    )

    available_algorithms: int = Field(
        ...,
        description="Number of algorithms ready to use"
    )

    max_dimensions: int = Field(
        ...,
        description="Maximum number of dimensions supported"
    )

    max_iterations: int = Field(
        ...,
        description="Maximum iterations allowed"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "available_algorithms": 2,
                "max_dimensions": 50,
                "max_iterations": 100
            }
        }
