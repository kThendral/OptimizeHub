"""
Authentication endpoints for OptimizeHub.
"""
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr
from typing import Optional
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from ..supabase_client import get_supabase_public, get_supabase_admin

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()

class SignupRequest(BaseModel):
    username: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(request: SignupRequest):
    """
    Create a new user account.
    
    Args:
        request: Signup request with username, email, and password
        
    Returns:
        User data and access token
        
    Raises:
        HTTPException: If signup fails
    """
    try:
        supabase = get_supabase_public()
        
        # Create auth user
        res = supabase.auth.sign_up({
            "email": request.email,
            "password": request.password,
            "options": {
                "data": {"username": request.username}
            }
        })
        
        if res.user:
            # Create profile in public.profiles table
            supabase_admin = get_supabase_admin()
            profile_data = {
                "id": res.user.id,
                "username": request.username,
                "email": request.email
            }
            
            try:
                supabase_admin.table("profiles").insert(profile_data).execute()
            except Exception as e:
                # If profile creation fails, user is still created in auth
                # Log the error but don't fail the signup
                print(f"Warning: Failed to create profile: {str(e)}")
            
            return {
                "access_token": res.session.access_token if res.session else None,
                "user": {
                    "id": res.user.id,
                    "email": res.user.email,
                    "username": request.username
                }
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create user"
            )
    except Exception as e:
        error_message = str(e)
        if "User already registered" in error_message or "already exists" in error_message.lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists"
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Signup failed: {error_message}"
        )


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(request: LoginRequest):
    """
    Login with email and password.
    
    Args:
        request: Login request with email and password
        
    Returns:
        User data and access token
        
    Raises:
        HTTPException: If login fails
    """
    try:
        supabase = get_supabase_public()
        
        res = supabase.auth.sign_in_with_password({
            "email": request.email,
            "password": request.password
        })
        
        if res.session and res.user:
            # Get username from profile
            username = None
            try:
                profile = supabase.table("profiles").select("username").eq("id", res.user.id).execute()
                if profile.data and len(profile.data) > 0:
                    username = profile.data[0].get("username")
            except Exception:
                # If profile doesn't exist, try to get from user metadata
                username = res.user.user_metadata.get("username")
            
            return {
                "access_token": res.session.access_token,
                "user": {
                    "id": res.user.id,
                    "email": res.user.email,
                    "username": username
                }
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
    except Exception as e:
        error_message = str(e)
        error_lower = error_message.lower()
        
        # Check for specific error types
        if "invalid login credentials" in error_lower or "invalid password" in error_lower:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password. Please check your credentials and try again."
            )
        elif "email not confirmed" in error_lower or "email not verified" in error_lower:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Please verify your email address before logging in."
            )
        elif "user not found" in error_lower or "no user found" in error_lower:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No account found with this email. Please sign up first."
            )
        elif "too many requests" in error_lower or "rate limit" in error_lower:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many login attempts. Please wait a moment and try again."
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Login failed: {error_message}"
            )

async def get_current_user(credentials:HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Dependency to verify JWT token and extract user ID.
    
    Use on endpoints that require authentication.
    
    Example:
        @app.get("/user/profile")
        async def get_profile(user_id: str = Depends(get_current_user)):
            # user_id is now available and verified
    """
    token = credentials.credentials
    
    try:
        supabase = get_supabase_public()
        # Verify the JWT token with Supabase
        user = supabase.auth.get_user(token)
        
        if not user or not user.user.id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )
        
        return user.user.id
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication failed: {str(e)}"
        )