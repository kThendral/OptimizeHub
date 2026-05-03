"""
API endpoints for user persistence features.
Requires authentication for all endpoints.
"""
from typing import List, Optional, Dict
from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Optional
from ..services.persistence_service import PersistenceService
from ..models.persistence import (
    OptimizationRunCreate,
    OptimizationRunResponse,
    SavedConfigurationCreate,
    SavedConfigurationResponse,
    UserStatsResponse
)
from ..api.auth import get_current_user  # See Step 5

router = APIRouter(prefix="/api/persistence", tags=["Persistence"])
service = PersistenceService()


# ============================================================================
# OPTIMIZATION RUNS ENDPOINTS
# ============================================================================

@router.post("/runs/save", response_model=OptimizationRunResponse)
async def save_run(
    run_data: OptimizationRunCreate,
    user_id: str = Depends(get_current_user)
) -> OptimizationRunResponse:
    """
    Save an optimization run to user history.
    
    **Authentication Required**
    
    Args:
        run_data: Optimization run details
        user_id: Current authenticated user
        
    Returns:
        Saved run with ID and timestamp
    """
    try:
        return service.save_optimization_run(user_id, run_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to save run: {str(e)}"
        )


@router.get("/runs/history", response_model=List[OptimizationRunResponse])
async def get_run_history(
    limit: int = 50,
    offset: int = 0,
    user_id: str = Depends(get_current_user)
) -> List[OptimizationRunResponse]:
    """
    Retrieve user's optimization run history.
    
    **Authentication Required**
    
    Args:
        limit: Maximum runs to return
        offset: Pagination offset
        user_id: Current authenticated user
        
    Returns:
        List of user's optimization runs
    """
    return service.get_user_run_history(user_id, limit, offset)


@router.get("/runs/public", response_model=List[OptimizationRunResponse])
async def get_public_runs(
    algorithm: Optional[str] = None,
    limit: int = 50
) -> List[OptimizationRunResponse]:
    """
    Browse public optimization runs shared by the community.
    
    **No authentication required - public data only**
    
    Args:
        algorithm: Filter by algorithm (optional)
        limit: Maximum results
        
    Returns:
        List of public runs
    """
    return service.get_public_runs(algorithm, limit)


@router.get("/runs/{run_id}", response_model=OptimizationRunResponse)
async def get_run(
    run_id: str,
    user_id: str = Depends(get_current_user)
) -> OptimizationRunResponse:
    """
    Get a specific optimization run.
    
    Can retrieve owned runs or any public/shared runs.
    
    Args:
        run_id: UUID of the run
        user_id: Current authenticated user
        
    Returns:
        Run details
    """
    run = service.get_run_by_id(run_id, user_id)
    if not run:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Run not found or you don't have access"
        )
    return run


@router.post("/runs/{run_id}/share")
async def share_run(
    run_id: str,
    shared_by: Optional[str] = None,
    user_id: str = Depends(get_current_user)
) -> Dict[str, str]:
    """
    Make an optimization run public for community sharing.
    
    Args:
        run_id: UUID of run to share
        shared_by: Your username for attribution
        user_id: Current authenticated user
        
    Returns:
        Confirmation message
    """
    try:
        service.share_run(run_id, user_id, shared_by)
        return {
            "message": "Run shared successfully",
            "run_id": run_id
        }
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


# ============================================================================
# SAVED CONFIGURATIONS ENDPOINTS
# ============================================================================

@router.post("/configs/save", response_model=SavedConfigurationResponse)
async def save_configuration(
    config_data: SavedConfigurationCreate,
    user_id: str = Depends(get_current_user)
) -> SavedConfigurationResponse:
    """
    Save an algorithm configuration for reuse.
    
    Args:
        config_data: Configuration details
        user_id: Current authenticated user
        
    Returns:
        Saved configuration with ID
    """
    try:
        return service.save_configuration(user_id, config_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to save configuration: {str(e)}"
        )


@router.get("/configs/my", response_model=List[SavedConfigurationResponse])
async def get_my_configurations(
    limit: int = 50,
    user_id: str = Depends(get_current_user)
) -> List[SavedConfigurationResponse]:
    """
    Retrieve your saved configurations.
    
    Args:
        limit: Maximum results
        user_id: Current authenticated user
        
    Returns:
        List of user's configurations
    """
    return service.get_user_configurations(user_id, limit)


@router.get("/configs/public", response_model=List[SavedConfigurationResponse])
async def get_public_configurations(
    algorithm: Optional[str] = None,
    tags: Optional[List[str]] = None,
    limit: int = 50
) -> List[SavedConfigurationResponse]:
    """
    Discover public configurations shared by the community.
    
    Args:
        algorithm: Filter by algorithm
        tags: Filter by tags
        limit: Maximum results
        
    Returns:
        List of public configurations
    """
    return service.get_public_configurations(algorithm, tags, limit)


@router.delete("/configs/{config_id}")
async def delete_configuration(
    config_id: str,
    user_id: str = Depends(get_current_user)
) -> Dict[str, str]:
    """
    Delete a saved configuration.
    
    Args:
        config_id: UUID of configuration
        user_id: Current authenticated user
        
    Returns:
        Confirmation message
    """
    try:
        service.delete_configuration(config_id, user_id)
        return {"message": "Configuration deleted successfully"}
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


# ============================================================================
# USER STATISTICS ENDPOINTS
# ============================================================================

@router.get("/stats", response_model=UserStatsResponse)
async def get_user_stats(
    user_id: str = Depends(get_current_user)
) -> UserStatsResponse:
    """
    Retrieve your optimization statistics.
    
    Args:
        user_id: Current authenticated user
        
    Returns:
        User statistics (total runs, favorite algorithm, etc.)
    """
    return service.get_user_stats(user_id)