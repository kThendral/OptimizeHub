"""
Celery task definitions for OptimizeHub.

Algorithm execution is delegated to Modal cloud functions.
asyncio.run() is used to call async Modal functions from synchronous Celery tasks,
as per Modal best-practices for non-async callers.
"""

import asyncio
import traceback
from typing import Any, Dict, Optional

from .celery_app import celery

# Import validation for parameter warnings (unchanged)
from .core.validation import validate_algorithm_params


# Do NOT retry ValueError — these are validation errors (bad algorithm name,
# missing fitness function) that will fail again on every retry.
# Only retry transient infrastructure errors (Modal cold-start failures, etc.).
_TRANSIENT_ERRORS = (RuntimeError, ConnectionError, OSError)


@celery.task(
    bind=True,
    acks_late=True,
    autoretry_for=_TRANSIENT_ERRORS,
    retry_backoff=True,
    retry_kwargs={"max_retries": 2},
)
def run_algorithm(
    self,
    algo_key: str,
    problem_payload: Dict[str, Any],
    params: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Celery task: run an optimization algorithm via Modal.

    Signature is unchanged from the previous implementation so that
    ``app/api/async_tasks.py`` requires no modification.

    Args:
        algo_key:        Friendly algorithm name (``"genetic"``, ``"pso"``, etc.)
        problem_payload: JSON-serializable problem dict.  ``fitness_function``
                         must be a string name (e.g. ``"sphere"``), NOT a callable
                         — Modal resolves it inside the cloud function.
        params:          Optional algorithm-specific parameter overrides.

    Returns:
        ``{"algo": algo_key, "status": "SUCCESS", "result": {...}}``
    """
    try:
        params = params or {}

        # Validate parameters and collect educational warnings
        _, _, param_warnings = validate_algorithm_params(algo_key, params)

        # Call Modal asynchronously from this synchronous Celery task.
        # asyncio.run() is safe here because Celery workers do not run an
        # event loop by default.
        from executor.modal_runner import run_algorithm as _modal_run

        result: dict = asyncio.run(
            _modal_run.remote.aio(algo_key, problem_payload, params)
        )

        # Normalise result keys for frontend (same as original task)
        if isinstance(result, dict):
            result.setdefault("elapsed_time", result.get("execution_time"))
            conv = result.get("convergence_curve") or result.get("history") or []
            try:
                result["iterations"] = (
                    len(conv)
                    if isinstance(conv, (list, tuple)) and len(conv) > 0
                    else None
                )
            except Exception:
                result["iterations"] = None
            result.setdefault("iterations_completed", result.get("iterations"))
            if param_warnings:
                result["warnings"] = param_warnings

        return {"algo": algo_key, "status": "SUCCESS", "result": result}

    except ValueError as exc:
        # Validation error — don't retry, fail immediately with clear message
        raise RuntimeError(f"Validation error (will not retry): {exc}") from exc
    except Exception as exc:
        tb = traceback.format_exc()
        raise self.retry(exc=RuntimeError(f"{exc}\n{tb}")) from exc
