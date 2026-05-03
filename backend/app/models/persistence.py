"""
Pydantic models for user persistence features.
"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID


class OptimizationRunCreate(BaseModel):
    """Model for saving an optimization run to database."""
    algorithm: str
    problem_name: Optional[str] = None
    best_fitness: float
    best_solution: List[float]
    convergence_curve: List[float]
    iterations_completed: int
    execution_time: float
    problem_definition: Dict[str, Any]
    algorithm_parameters: Dict[str, Any]
    fitness_function_name: Optional[str] = None


class OptimizationRunResponse(OptimizationRunCreate):
    """Model for returning saved optimization run."""
    id: UUID
    user_id: UUID
    created_at: datetime
    shared: bool = False
    shared_by: Optional[str] = None

    class Config:
        from_attributes = True


class SavedConfigurationCreate(BaseModel):
    """Model for saving a configuration."""
    config_name: str
    description: Optional[str] = None
    algorithm: str
    problem_definition: Dict[str, Any]
    algorithm_parameters: Dict[str, Any]
    tags: Optional[List[str]] = Field(default_factory=list)
    is_public: bool = False


class SavedConfigurationResponse(SavedConfigurationCreate):
    """Model for returning saved configuration."""
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserStatsResponse(BaseModel):
    """User statistics."""
    total_runs: int
    total_configurations: int
    last_run_at: Optional[datetime] = None
    favorite_algorithm: Optional[str] = None


class UserProfileResponse(BaseModel):
    """User profile information."""
    id: UUID
    email: str
    username: str
    stats: UserStatsResponse
    created_at: datetime

    class Config:
        from_attributes = True