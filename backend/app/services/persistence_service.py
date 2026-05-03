"""
Service for handling user persistence operations.
Saves and retrieves optimization runs, configurations, and user data.
"""
from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime
from ..supabase_client import get_supabase_admin
from ..models.persistence import (
    OptimizationRunCreate,
    OptimizationRunResponse,
    SavedConfigurationCreate,
    SavedConfigurationResponse,
    UserStatsResponse
)


class PersistenceService:
    """Handles all database operations for user data."""
    
    def __init__(self):
        self.supabase = get_supabase_admin()
    
    # ========================================================================
    # OPTIMIZATION RUNS
    # ========================================================================
    
    def save_optimization_run(
        self,
        user_id: str,
        run_data: OptimizationRunCreate
    ) -> OptimizationRunResponse:
        """
        Save an optimization run to the database.
        
        Args:
            user_id: UUID of the user performing the optimization
            run_data: Optimization run details
            
        Returns:
            Saved run with ID and timestamps
        """
        payload = {
            "user_id": user_id,
            **run_data.model_dump()
        }
        
        response = self.supabase.table("optimization_runs").insert(payload).execute()
        
        if response.data and len(response.data) > 0:
            return OptimizationRunResponse(**response.data[0])
        
        raise ValueError("Failed to save optimization run")
    
    def get_user_run_history(
        self,
        user_id: str,
        limit: int = 50,
        offset: int = 0
    ) -> List[OptimizationRunResponse]:
        """
        Retrieve a user's optimization run history.
        
        Args:
            user_id: User's UUID
            limit: Maximum number of runs to return
            offset: Pagination offset
            
        Returns:
            List of optimization runs
        """
        response = (
            self.supabase.table("optimization_runs")
            .select("*")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .range(offset, offset + limit - 1)
            .execute()
        )
        
        return [OptimizationRunResponse(**run) for run in response.data]
    
    def get_run_by_id(
        self,
        run_id: str,
        user_id: str
    ) -> Optional[OptimizationRunResponse]:
        """
        Get a specific run (only if user owns it or it's shared).
        
        Args:
            run_id: UUID of the run
            user_id: User making the request
            
        Returns:
            Run data or None if not found/unauthorized
        """
        response = (
            self.supabase.table("optimization_runs")
            .select("*")
            .eq("id", run_id)
            .execute()
        )
        
        if not response.data:
            return None
        
        run = response.data[0]
        # Check permissions: owner or shared publicly
        if run["user_id"] == user_id or run["shared"]:
            return OptimizationRunResponse(**run)
        
        return None
    
    def share_run(
        self,
        run_id: str,
        user_id: str,
        shared_by: Optional[str] = None
    ) -> bool:
        """
        Make an optimization run public/shareable.
        
        Args:
            run_id: UUID of the run to share
            user_id: User making the run public
            shared_by: Username for attribution
            
        Returns:
            True if successful
        """
        # Verify ownership
        response = (
            self.supabase.table("optimization_runs")
            .select("user_id")
            .eq("id", run_id)
            .execute()
        )
        
        if not response.data or response.data[0]["user_id"] != user_id:
            raise PermissionError("Cannot share run you don't own")
        
        # Update sharing status
        self.supabase.table("optimization_runs").update({
            "shared": True,
            "shared_by": shared_by
        }).eq("id", run_id).execute()
        
        return True
    
    def get_public_runs(
        self,
        algorithm: Optional[str] = None,
        limit: int = 50
    ) -> List[OptimizationRunResponse]:
        """
        Retrieve public optimization runs for community browsing.
        
        Args:
            algorithm: Filter by algorithm name (optional)
            limit: Maximum results
            
        Returns:
            List of public runs
        """
        query = self.supabase.table("optimization_runs").select("*").eq("shared", True)
        
        if algorithm:
            query = query.eq("algorithm", algorithm)
        
        response = query.order("created_at", desc=True).limit(limit).execute()
        
        return [OptimizationRunResponse(**run) for run in response.data]
    
    # ========================================================================
    # SAVED CONFIGURATIONS
    # ========================================================================
    
    def save_configuration(
        self,
        user_id: str,
        config_data: SavedConfigurationCreate
    ) -> SavedConfigurationResponse:
        """
        Save an algorithm configuration for reuse.
        
        Args:
            user_id: UUID of the user
            config_data: Configuration details
            
        Returns:
            Saved configuration with ID
        """
        payload = {
            "user_id": user_id,
            **config_data.model_dump()
        }
        
        response = self.supabase.table("saved_configurations").insert(payload).execute()
        
        if response.data and len(response.data) > 0:
            return SavedConfigurationResponse(**response.data[0])
        
        raise ValueError("Failed to save configuration")
    
    def get_user_configurations(
        self,
        user_id: str,
        limit: int = 50
    ) -> List[SavedConfigurationResponse]:
        """
        Retrieve user's saved configurations.
        
        Args:
            user_id: User's UUID
            limit: Maximum results
            
        Returns:
            List of configurations
        """
        response = (
            self.supabase.table("saved_configurations")
            .select("*")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .limit(limit)
            .execute()
        )
        
        return [SavedConfigurationResponse(**config) for config in response.data]
    
    def get_public_configurations(
        self,
        algorithm: Optional[str] = None,
        tags: Optional[List[str]] = None,
        limit: int = 50
    ) -> List[SavedConfigurationResponse]:
        """
        Get public configurations for community discovery.
        
        Args:
            algorithm: Filter by algorithm
            tags: Filter by tags
            limit: Maximum results
            
        Returns:
            List of public configurations
        """
        query = self.supabase.table("saved_configurations").select("*").eq("is_public", True)
        
        if algorithm:
            query = query.eq("algorithm", algorithm)
        
        response = query.order("created_at", desc=True).limit(limit).execute()
        
        configs = [SavedConfigurationResponse(**config) for config in response.data]
        
        # Filter by tags if specified
        if tags:
            configs = [
                c for c in configs
                if any(tag in c.tags for tag in tags)
            ]
        
        return configs[:limit]
    
    def delete_configuration(
        self,
        config_id: str,
        user_id: str
    ) -> bool:
        """
        Delete a saved configuration.
        
        Args:
            config_id: UUID of configuration
            user_id: User making the request
            
        Returns:
            True if successful
        """
        # Verify ownership
        response = (
            self.supabase.table("saved_configurations")
            .select("user_id")
            .eq("id", config_id)
            .execute()
        )
        
        if not response.data or response.data[0]["user_id"] != user_id:
            raise PermissionError("Cannot delete configuration you don't own")
        
        self.supabase.table("saved_configurations").delete().eq("id", config_id).execute()
        
        return True
    
    # ========================================================================
    # USER STATISTICS
    # ========================================================================
    
    def update_user_stats(
        self,
        user_id: str,
        algorithm: str
    ) -> None:
        """
        Update user statistics after a run.
        
        Args:
            user_id: User's UUID
            algorithm: Algorithm used
        """
        # Get current stats
        response = (
            self.supabase.table("user_stats")
            .select("*")
            .eq("user_id", user_id)
            .execute()
        )
        
        if response.data:
            # Update existing stats
            stats = response.data[0]
            self.supabase.table("user_stats").update({
                "total_runs": stats["total_runs"] + 1,
                "last_run_at": datetime.utcnow().isoformat(),
                "favorite_algorithm": algorithm,  # Latest algorithm used
                "updated_at": datetime.utcnow().isoformat()
            }).eq("user_id", user_id).execute()
        else:
            # Create new stats
            self.supabase.table("user_stats").insert({
                "user_id": user_id,
                "total_runs": 1,
                "last_run_at": datetime.utcnow().isoformat(),
                "favorite_algorithm": algorithm
            }).execute()
    
    def get_user_stats(self, user_id: str) -> UserStatsResponse:
        """
        Retrieve user statistics.
        
        Args:
            user_id: User's UUID
            
        Returns:
            User statistics
        """
        response = (
            self.supabase.table("user_stats")
            .select("*")
            .eq("user_id", user_id)
            .execute()
        )
        
        if response.data:
            return UserStatsResponse(**response.data[0])
        
        # Return defaults if no stats exist
        return UserStatsResponse(
            total_runs=0,
            total_configurations=0,
            last_run_at=None,
            favorite_algorithm=None
        )