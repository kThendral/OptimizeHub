from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from celery import group
from celery.result import AsyncResult

from ..tasks import run_algorithm
from ..celery_app import celery

router = APIRouter(prefix="/async", tags=["async"])

class ProblemRequest(BaseModel):
    problem: Dict[str, Any]
    algorithms: List[str]  # e.g. ["genetic", "simulated_annealing"]

def _format_algorithm_field(algo_str: Any) -> Any:
    """
    Normalize the algorithm field into a small structured object when possible.
    Returns a dict with keys:
      - display: short human string
      - name: base name (e.g. DE)
      - variant: extra descriptor (e.g. rand/1/bin) or None
      - details: params dict (CR, F, ...)
      - raw: original string
    If not parseable, returns the trimmed string.
    """
    if not isinstance(algo_str, str):
        return algo_str
    s = algo_str.strip()
    # parse "MAIN (k=v, ...)" pattern
    if "(" in s and s.endswith(")"):
        main, rest = s.split("(", 1)
        main = main.strip()
        params = rest[:-1].strip()  # drop trailing ')'
        params_dict = {}
        for part in params.split(","):
            part = part.strip()
            if not part:
                continue
            if "=" in part:
                k, v = part.split("=", 1)
                k = k.strip()
                v = v.strip()
                try:
                    # numeric parse
                    v_parsed = float(v) if "." in v else int(v)
                except Exception:
                    v_parsed = v
                params_dict[k] = v_parsed
            else:
                params_dict[part] = True
        # try to split main into name / variant like "DE/rand/1/bin"
        if "/" in main:
            name, variant = main.split("/", 1)
            name = name.strip()
            variant = variant.strip()
        else:
            name = main
            variant = None
        # Preserve variant with slash in the display so DE/rand/1/bin stays readable
        display = f"{name}/{variant}" if variant else f"{name}"
        
        param_str = ""
        if params_dict:
            parts = [f"{k}={v}" for k, v in params_dict.items()]
            param_str = " (" + ", ".join(parts) + ")"
        display = f"{name}/{variant}" if variant else f"{name}"
        display = f"{display}{param_str}"
        return {"display": display, "name": name, "variant": variant, "details": params_dict, "raw": algo_str}
    
    # fallback: try to split "NAME/variant" without params
    if "/" in s:
        name, variant = s.split("/", 1)
        name = name.strip()
        variant = variant.strip()
        display = f"{name}/{variant}"
        return {"display": display, "name": name, "variant": variant, "details": {}, "raw": algo_str}
    return s

def _normalize_result_payload(res: Any) -> Any:
    """
    Ensure result payload contains normalized fields to display:
      - algorithm: formatted via _format_algorithm_field
      - iterations: attempt to infer (params.max_iterations / max_generations / len(convergence_curve))
      - execution_time: pass-through if present
      - best_fitness: try best_fitness OR last value of convergence_curve
    Mutates and returns a copy-friendly structure.
    """
    if not isinstance(res, dict):
        return res

    # many tasks return {'algo':..., 'status':..., 'result': {...}}
    payload = dict(res)  # shallow copy
    inner = payload.get("result") if isinstance(payload.get("result"), dict) else payload
    # Ensure inner is a dict to avoid None or non-dict types for static analysis and runtime
    if inner is None:
        inner = {}
    elif not isinstance(inner, dict):
        try:
            inner = dict(inner)
        except Exception:
            inner = {}

    # If algorithm present, normalize it and expose a display string
    algo_val = None
    if isinstance(inner, dict) and "algorithm" in inner:
        algo_val = inner.get("algorithm")
        formatted = _format_algorithm_field(algo_val)
        # formatted may be a dict with 'display' or a plain string
        if isinstance(formatted, dict):
            inner["algorithm_display"] = formatted.get("display") or formatted.get("name")
            # Use the human-friendly display string as the main `algorithm` value
            inner["algorithm"] = inner["algorithm_display"]
        else:
            inner["algorithm_display"] = str(formatted)
            inner["algorithm"] = str(formatted)

    # iterations heuristics
    iterations = inner.get("iterations")
    if iterations is None:
        params = inner.get("params", {}) or {}
        iterations = params.get("max_iterations") or params.get("max_generations")
    if iterations is None:
        conv = inner.get("convergence_curve") or inner.get("history") or []
        try:
            iterations = len(conv) if isinstance(conv, (list, tuple)) and len(conv) > 0 else None
        except Exception:
            iterations = None
    if iterations is not None:
        inner["iterations"] = int(iterations)
    else:
        inner.setdefault("iterations", None)
    # Provide frontend-friendly key
    inner["iterations_completed"] = inner.get("iterations")

    # execution_time pass-through if present; otherwise try common keys like 'elapsed_time' or 'runtime'
    exec_time = (
        inner.get("execution_time")
        or inner.get("runtime")
        or inner.get("elapsed_time")
        or inner.get("time")
        or None
    )
    inner["execution_time"] = exec_time

    # best_fitness heuristics
    best = inner.get("best_fitness")
    if best is None:
        conv = inner.get("convergence_curve") or inner.get("history") or []
        if isinstance(conv, (list, tuple)) and len(conv) > 0:
            try:
                best = conv[-1]
            except Exception:
                best = None
    inner["best_fitness"] = best

    # Ensure status field exists for ResultsDisplay
    if "status" not in inner and "status" in payload:
        inner["status"] = payload.get("status")

    # place normalized inner back into payload in same shape
    # Return the flattened inner dict that frontend `ResultsDisplay` expects
    return inner

@router.post("/optimize")
def optimize(problem_req: ProblemRequest):
    """
    Submit a group of algorithm tasks to Celery (runs in parallel).
    Returns the group id and the child task ids to poll for results.
    """
    if not problem_req.algorithms:
        raise HTTPException(status_code=400, detail="No algorithms specified")

    # Transform problem to match Celery task expectations
    problem_payload = dict(problem_req.problem)

    # Rename fitness_function_name to fitness_function if present
    if "fitness_function_name" in problem_payload:
        problem_payload["fitness_function"] = problem_payload.pop("fitness_function_name")

    # Create a group of signatures using the registered Celery task helper
    sigs = [run_algorithm.s(algo, problem_payload) for algo in problem_req.algorithms]
    job = group(sigs)
    group_result = job.apply_async()
    child_ids = [res.id for res in group_result.results]

    return {"group_id": group_result.id, "task_ids": child_ids}

@router.get("/tasks/{task_id}")
def get_task_status(task_id: str):
    async_res = AsyncResult(task_id, app=celery)
    state = async_res.state
    response = {"task_id": task_id, "state": state}
    if async_res.ready():
        res = async_res.result
        # Normalize the payload (algorithm display, iterations, execution_time, etc.)
        try:
            if isinstance(res, dict):
                res = _normalize_result_payload(res)
        except Exception:
            # Fall back to the raw result if normalization fails
            pass
        response["result"] = res
    elif state == "FAILURE":
        response["result"] = async_res.info  # Error details
    return response