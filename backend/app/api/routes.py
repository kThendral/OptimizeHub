"""
FastAPI routes for OptimizeHub API.
"""
from fastapi import APIRouter, HTTPException, status, UploadFile, File
from typing import Dict, Any
import yaml
from app.models.problem import OptimizationRequest, ProblemInput
from app.models.result import (
    OptimizationResult,
    ValidationResult,
    AlgorithmListResponse,
    AlgorithmInfo,
    HealthResponse
)
from app.services.executor import AlgorithmExecutor
from app.services.docker_executor import get_docker_executor
from app.validators.code_validator import validate_fitness_code
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


@router.post("/optimize/custom", response_model=OptimizationResult, status_code=status.HTTP_200_OK)
async def run_optimization_custom(
    fitness_file: UploadFile = File(..., description="Python file containing fitness function"),
    config_file: UploadFile = File(..., description="YAML configuration file")
) -> OptimizationResult:
    """
    Run an optimization algorithm with a custom fitness function.

    This endpoint allows users to upload their own fitness function and execute
    it in an isolated Docker container for security.

    Args:
        fitness_file: Python file (.py) containing a 'fitness' function
        config_file: YAML file with algorithm configuration

    Returns:
        Optimization results with status, solution, and convergence data

    Raises:
        HTTPException: If validation fails or execution encounters an error
    """
    # Validate file types
    if not fitness_file.filename.endswith('.py'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Fitness file must be a Python file (.py)"
        )

    if not config_file.filename.endswith(('.yaml', '.yml')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Config file must be a YAML file (.yaml or .yml)"
        )

    # Read files
    try:
        fitness_code = (await fitness_file.read()).decode('utf-8')
        config_content = (await config_file.read()).decode('utf-8')
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Files must be valid UTF-8 text files"
        )

    # Check file sizes (max 1MB each)
    if len(fitness_code) > 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Fitness file too large (max 1MB)"
        )

    if len(config_content) > 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Config file too large (max 1MB)"
        )

    # Validate fitness function code
    is_valid, error_message = validate_fitness_code(fitness_code)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "Security validation failed",
                "message": error_message
            }
        )

    # Parse YAML configuration
    try:
        config = yaml.safe_load(config_content)
    except yaml.YAMLError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid YAML configuration: {str(e)}"
        )

    # Validate configuration structure
    if not isinstance(config, dict):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Configuration must be a YAML dictionary"
        )

    required_fields = ['algorithm', 'parameters', 'problem']
    missing_fields = [field for field in required_fields if field not in config]
    if missing_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Missing required fields in configuration: {', '.join(missing_fields)}"
        )

    # Validate algorithm name
    allowed_algorithms = ['PSO', 'GA', 'DE', 'SA', 'ACOR']
    if config['algorithm'] not in allowed_algorithms:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Algorithm must be one of: {', '.join(allowed_algorithms)}"
        )

    # Execute in Docker sandbox
    try:
        docker_executor = get_docker_executor()
        result = docker_executor.execute_custom_fitness(fitness_code, config)

        # Check if execution was successful
        if not result.get('success', False):
            error_type = result.get('error_type', 'unknown')
            error_message = result.get('error', 'Unknown error occurred')

            # Provide user-friendly error messages
            if error_type == 'timeout':
                friendly_message = f"Optimization exceeded 30 seconds timeout. Try reducing iterations or problem complexity. Details: {error_message}"
            elif error_type == 'validation_error':
                friendly_message = f"Code validation error: {error_message}"
            elif error_type == 'container_error':
                friendly_message = f"Execution error: {error_message}"
            else:
                friendly_message = error_message

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "error": "Execution failed",
                    "error_type": error_type,
                    "message": friendly_message
                }
            )

        # Return successful result
        return OptimizationResult(
            status="success",
            algorithm=config['algorithm'],
            best_solution=result['best_solution'],
            best_fitness=result['best_fitness'],
            iterations_completed=result['iterations'],
            convergence_curve=result['convergence_history'],
            execution_time=result.get('execution_time', 0)
        )

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Catch any unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Unexpected error during execution",
                "message": str(e)
            }
        )


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
            "POST /api/optimize/custom": "Run optimization with custom fitness function (Docker sandbox)",
            "GET /api/algorithms": "List all algorithms",
            "GET /api/algorithms/{name}": "Get algorithm details",
            "POST /api/validate": "Validate problem definition",
            "GET /api/health": "Health check"
        }
    }
