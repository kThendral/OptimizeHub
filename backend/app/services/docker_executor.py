"""
Modal-backed executor service for running custom fitness functions.

Replaces the previous Docker subprocess approach with Modal cloud functions,
preserving the same public API so that API routes do not need to change.

Original Docker constraints are now enforced by Modal:
  - No network access  (block_network=True)
  - 512 MB memory      (memory=512)
  - 30 s timeout       (timeout=30)
  - Isolated container (Modal ephemeral VM)
"""

import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class DockerExecutor:
    """
    Executes custom fitness functions via Modal cloud functions.

    Public API is identical to the original DockerExecutor so that
    API routes (``app/api/routes.py``) require no changes.
    """

    def __init__(
        self,
        timeout: int = 30,
        memory_limit: str = "512m",
        cpu_limit: str = "1.0",
        # Legacy Docker parameters accepted but ignored
        image_name: str = "optimizehub-sandbox:latest",
    ):
        self.timeout = timeout
        self.memory_limit = memory_limit
        self.cpu_limit = cpu_limit

    def execute_custom_fitness(
        self,
        fitness_code: str,
        config: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Execute a custom fitness function via Modal.

        Args:
            fitness_code:
                Python source code containing ``def fitness(x): ...``.
            config:
                Configuration dict with keys:
                  ``algorithm`` (str), ``parameters`` (dict), ``problem`` (dict).

        Returns:
            Result dict compatible with the original Docker runner output::

                {
                    "success":            bool,
                    "best_solution":      list,
                    "best_fitness":       float,
                    "iterations":         int,
                    "convergence_history": list,
                    "execution_time":     float,
                }
            On failure::

                {
                    "success":    False,
                    "error":      str,
                    "error_type": str,   # "timeout" | "validation_error" | "execution_error"
                }
        """
        # Extract algorithm name, algo params, and problem geometry from config
        algorithm_name: str = config.get("algorithm", "GA")
        algo_parameters: dict = config.get("parameters", {})
        problem_cfg: dict = config.get("problem", {})

        # Bundle problem geometry inside params so the Modal function can use it
        params: dict = {**algo_parameters, "problem": problem_cfg}

        try:
            from executor.modal_runner import run_with_custom_fitness

            logger.info(
                "Dispatching custom fitness run to Modal "
                "(algorithm=%s, timeout=%ds)",
                algorithm_name,
                self.timeout,
            )

            modal_result: dict = run_with_custom_fitness.remote(
                algorithm_name, fitness_code, params
            )

            logger.info("Modal execution completed successfully")

            # Translate Modal result format → Docker-runner-compatible format
            convergence_curve = modal_result.get("convergence_curve") or []
            return {
                "success": True,
                "best_solution": modal_result.get("best_solution"),
                "best_fitness": modal_result.get("best_fitness"),
                "iterations": len(convergence_curve),
                "convergence_history": convergence_curve,
                "execution_time": modal_result.get("execution_time", 0.0),
            }

        except ValueError as exc:
            # Validation errors from modal_runner (bad algo name, missing fitness fn)
            logger.warning("Validation error in custom fitness execution: %s", exc)
            return {
                "success": False,
                "error": str(exc),
                "error_type": "validation_error",
            }

        except Exception as exc:
            err_str = str(exc)
            logger.error("Modal execution failed: %s", err_str)

            # Classify Modal timeout errors using class name (avoids hard import dependency
            # on modal internals while still catching all known timeout exception names).
            exc_type_name = type(exc).__name__
            is_timeout = exc_type_name in ("FunctionTimeoutError", "TimeoutError") or (
                "timeout" in err_str.lower()
            )
            if is_timeout:
                return {
                    "success": False,
                    "error": (
                        f"Execution exceeded {self.timeout} seconds timeout. "
                        "Try reducing iterations or problem complexity. "
                        f"Details: {err_str}"
                    ),
                    "error_type": "timeout",
                }

            # Container / sandbox execution errors
            if exc_type_name in ("ExecutionError", "UserCodeException", "SandboxTerminatedError"):
                return {
                    "success": False,
                    "error": f"Sandbox execution error: {err_str}",
                    "error_type": "container_error",
                }

            return {
                "success": False,
                "error": err_str,
                "error_type": "execution_error",
            }

    def cleanup_all(self) -> None:
        """No-op: Modal manages container lifecycle automatically."""
        pass


# ---------------------------------------------------------------------------
# Singleton helper — unchanged public API
# ---------------------------------------------------------------------------
_executor_instance: Optional[DockerExecutor] = None


def get_docker_executor() -> DockerExecutor:
    """Return (or create) the singleton DockerExecutor instance."""
    global _executor_instance
    if _executor_instance is None:
        _executor_instance = DockerExecutor()
    return _executor_instance
