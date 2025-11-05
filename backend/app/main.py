"""
FastAPI application entry point for OptimizeHub.
"""
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
from app.api.async_tasks import router as async_router
import logging

from app.api.routes import router
from app.config import get_available_algorithms, ALGORITHM_REGISTRY

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    """
    # Startup
    logger.info("Starting OptimizeHub API...")

    # Check available algorithms
    available = get_available_algorithms()
    logger.info(f"Available algorithms: {', '.join(available) if available else 'None'}")

    # Log all registered algorithms
    logger.info(f"Total registered algorithms: {len(ALGORITHM_REGISTRY)}")
    for name, info in ALGORITHM_REGISTRY.items():
        status_indicator = "[OK]" if info['status'] == 'available' else "[PENDING]"
        logger.info(f"  {status_indicator} {info['display_name']} ({name}): {info['status']}")

    logger.info("OptimizeHub API started successfully")

    yield

    # Shutdown
    logger.info("Shutting down OptimizeHub API...")


# Create FastAPI application
app = FastAPI(
    title="OptimizeHub API",
    description=(
        "RESTful API for running optimization algorithms including "
        "Particle Swarm Optimization, Genetic Algorithm, Differential Evolution, "
        "Simulated Annealing, and Ant Colony Optimization."
    ),
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)


# ==============================================================================
# CORS Configuration
# ==============================================================================

# Configure CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React default
        "http://localhost:5173",  # Vite default
        "http://localhost:8080",  # Alternative frontend port
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==============================================================================
# Exception Handlers
# ==============================================================================

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handle Pydantic validation errors with detailed error messages.
    """
    errors = []
    for error in exc.errors():
        field = " -> ".join(str(loc) for loc in error['loc'])
        message = error['msg']
        errors.append(f"{field}: {message}")

    logger.warning(f"Validation error on {request.url.path}: {errors}")

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation Error",
            "detail": "Request data validation failed",
            "validation_errors": errors
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """
    Handle unexpected exceptions gracefully.
    """
    logger.error(f"Unhandled exception on {request.url.path}: {str(exc)}", exc_info=True)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "detail": "An unexpected error occurred while processing your request",
            "message": str(exc)
        }
    )


# ==============================================================================
# Include Routers
# ==============================================================================

# Mount API routes under /api prefix
app.include_router(router, prefix="/api", tags=["Optimization"])
app.include_router(async_router)

# ==============================================================================
# Root Endpoint
# ==============================================================================

@app.get("/")
async def root():
    """
    Root endpoint - API information.
    """
    return {
        "message": "Welcome to OptimizeHub API",
        "version": "1.0.0",
        "status": "operational",
        "documentation": {
            "interactive": "/docs",
            "redoc": "/redoc"
        },
        "endpoints": {
            "health": "/api/health",
            "algorithms": "/api/algorithms",
            "optimize": "/api/optimize",
            "validate": "/api/validate"
        }
    }


# ==============================================================================
# Development Server
# ==============================================================================

if __name__ == "__main__":
    import uvicorn

    logger.info("Starting development server...")

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
