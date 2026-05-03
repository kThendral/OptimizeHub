"""
FastAPI application entry point for OptimizeHub.
"""
# Standard library — no app imports yet
import logging
import os
import threading
from contextlib import asynccontextmanager
from app.api.persistence_routes import router as persistence_router

# Load .env FIRST so that REDIS_URL and other vars are in os.environ
# before any app module (celery_app, config, etc.) is imported.
# celery_app.py reads REDIS_URL at module level — if dotenv runs after
# that import, Celery gets REDIS_URL=None and falls back to AMQP.
from dotenv import load_dotenv
load_dotenv()

# App imports — safe to do after load_dotenv()
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.api.async_tasks import router as async_router
from app.api.routes import router
from app.api.sse import router as sse_router
from app.api.auth import router as auth_router
from app.config import get_available_algorithms, ALGORITHM_REGISTRY

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def run_celery_worker():
    """Run Celery worker in a background thread alongside FastAPI."""
    try:
        from app.celery_app import celery
        celery.worker_main([
            "worker",
            "--loglevel=info",
            "--concurrency=2",       # 2 concurrent task slots
            "--without-gossip",      # reduces Redis chatter
            "--without-mingle",      # skips worker sync on startup
            "--without-heartbeat",   # reduces Redis chatter further
            "-Q", "celery"           # listen on default queue
        ])
    except Exception:
        import traceback
        print(f"[celery-thread-error] {traceback.format_exc()}", flush=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    """
    # Startup
    logger.info("Starting OptimizeHub API...")

    # Start Celery worker as daemon thread so it runs alongside FastAPI
    worker_thread = threading.Thread(
        target=run_celery_worker,
        daemon=True,  # thread dies when main process exits
        name="celery-worker"
    )
    worker_thread.start()
    logger.info(f"[startup] Celery worker thread started: {worker_thread.name}")

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

    # Shutdown — daemon=True means the thread stops with the main process
    logger.info("[shutdown] Celery worker thread will stop with main process")
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
_default_origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:8080",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:8080",
]
_extra_origins = [
    o.strip()
    for o in os.environ.get("ALLOWED_ORIGINS", "").split(",")
    if o.strip()
]
_allowed_origins = _default_origins + _extra_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins,
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
app.include_router(sse_router, prefix="/api", tags=["SSE"])
app.include_router(auth_router, prefix="/api", tags=["auth"])
app.include_router(persistence_router, tags=["Persistence"])

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
