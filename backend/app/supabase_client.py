"""
Supabase client configuration for OptimizeHub.
"""
import os
from supabase import create_client, Client
from typing import Optional

# Client for public operations (uses anon key)
supabase_public: Optional[Client] = None

# Client for server-only operations (uses service_role key)
supabase_admin: Optional[Client] = None


def get_supabase_public() -> Client:
    """Get or create the public Supabase client."""
    global supabase_public
    if supabase_public is None:
        url = os.getenv("SUPABASE_URL")
        anon_key = os.getenv("SUPABASE_ANON_KEY")
        
        if not url or not anon_key:
            raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set in environment variables")
        
        supabase_public = create_client(url, anon_key)
    return supabase_public


def get_supabase_admin() -> Client:
    """Get or create the admin Supabase client."""
    global supabase_admin
    if supabase_admin is None:
        url = os.getenv("SUPABASE_URL")
        service_role_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        
        if not url or not service_role_key:
            raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set in environment variables")
        
        supabase_admin = create_client(url, service_role_key)
    return supabase_admin
