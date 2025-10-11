"""
FastAPI routes for OptimizeHub API.
"""
from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any
from app.models.problem import OptimizationRequest, ProblemInput
from app.models.result import (
    OptimizationResult,
    ValidationResult,
    AlgorithmListResponse,
    AlgorithmInfo,
    HealthResponse
)
from app.services.executor import AlgorithmExecutor
from app.core.validation import validate_problem, validate_algorithm_params
from app.config import MAX_DIMENSIONS, MAX_ITERATIONS, get_available_algorithms

# Initialize router
router = APIRouter()

# Initialize executor
executor = AlgorithmExecutor()


@router.post("/optimize", response_model=OptimizationResult, status_code=status.HTTP_200_OK)
async def run_optimization(request: OptimizationRequest) -> OptimizationResult:
    """
    Run an optimization algorithm on a given problem.

    This endpoint executes the requested algorithm synchronously and returns results.
    If the algorithm is not yet implemented, returns a proper error response.

    Args:
        request: Optimization request with algorithm, problem, and parameters

    Returns:
        Optimization results with status, solution, and convergence data

    Raises:
        HTTPException: If validation fails
    """
    # Validate problem
    problem_dict = request.problem.model_dump()
    is_valid, errors, warnings = validate_problem(problem_dict)

    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "Invalid problem definition",
                "validation_errors": errors,
                "warnings": warnings
            }
        )

    # Validate algorithm parameters
    is_valid, errors, warnings = validate_algorithm_params(request.algorithm, request.params)

    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "Invalid algorithm parameters",
                "validation_errors": errors,
                "warnings": warnings
            }
        )

    # Execute algorithm
    result = executor.run_algorithm(
        algorithm_name=request.algorithm,
        problem=problem_dict,
        params=request.params
    )

    # Handle not_implemented status with proper HTTP response
    # (still returns 200 but with status field indicating not_implemented)
    return OptimizationResult(**result)


@router.get("/algorithms", response_model=AlgorithmListResponse)
async def list_algorithms() -> AlgorithmListResponse:
    """
    Get list of all algorithms with their status and details.

    Returns information about ALL algorithms including:
    - Available algorithms (ready to use)
    - Coming soon algorithms (in development)

    Returns:
        List of algorithms with metadata
    """
    algorithm_list = executor.get_algorithm_list()
    return AlgorithmListResponse(**algorithm_list)


@router.get("/algorithms/{algorithm_name}", response_model=AlgorithmInfo)
async def get_algorithm_info(algorithm_name: str) -> AlgorithmInfo:
    """
    Get detailed information about a specific algorithm.

    Includes:
    - Description and use cases
    - Default parameters
    - Parameter information and recommendations
    - Implementation status

    Args:
        algorithm_name: Name of the algorithm (e.g., 'particle_swarm')

    Returns:
        Detailed algorithm information

    Raises:
        HTTPException: If algorithm not found
    """
    algorithm_details = executor.get_algorithm_details(algorithm_name)

    if algorithm_details is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Algorithm '{algorithm_name}' not found"
        )

    return AlgorithmInfo(**algorithm_details)


@router.post("/validate", response_model=ValidationResult)
async def validate_problem_endpoint(problem: ProblemInput) -> ValidationResult:
    """
    Validate a problem definition without running optimization.

    Useful for frontend form validation before submitting an optimization request.

    Args:
        problem: Problem definition to validate

    Returns:
        Validation result with errors, warnings, and problem summary
    """
    problem_dict = problem.model_dump()
    is_valid, errors, warnings = validate_problem(problem_dict)

    # Create problem summary
    problem_summary = None
    if is_valid or (not errors and warnings):
        bounds = problem_dict.get('bounds', [])
        if bounds:
            # Check if all bounds are the same
            if all(b == bounds[0] for b in bounds):
                bounds_desc = f"{bounds[0]} for all dimensions"
            else:
                bounds_desc = f"{len(bounds)} dimension-specific bounds"
        else:
            bounds_desc = "No bounds specified"

        problem_summary = {
            'dimensions': problem_dict.get('dimensions'),
            'objective': problem_dict.get('objective', 'minimize'),
            'bounds_range': bounds_desc,
            'fitness_function': problem_dict.get('fitness_function_name', 'Not specified')
        }

    return ValidationResult(
        valid=is_valid,
        errors=errors if errors else None,
        warnings=warnings if warnings else None,
        problem_summary=problem_summary
    )


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Health check endpoint.

    Returns service status and configuration information.

    Returns:
        Health status with available algorithm count and platform limits
    """
    available_algorithms = get_available_algorithms()

    return HealthResponse(
        status="healthy",
        available_algorithms=len(available_algorithms),
        max_dimensions=MAX_DIMENSIONS,
        max_iterations=MAX_ITERATIONS
    )


@router.get("/")
async def root() -> Dict[str, Any]:
    """
    API root endpoint.

    Returns:
        Welcome message and API information
    """
    return {
        "message": "Welcome to OptimizeHub API",
        "version": "1.0.0",
        "docs_url": "/docs",
        "health_check_url": "/api/health",
        "endpoints": {
            "POST /api/optimize": "Run optimization algorithm",
            "GET /api/algorithms": "List all algorithms",
            "GET /api/algorithms/{name}": "Get algorithm details",
            "POST /api/validate": "Validate problem definition",
            "GET /api/health": "Health check"
        }
    }
