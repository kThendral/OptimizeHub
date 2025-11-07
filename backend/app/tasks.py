from .celery_app import celery
import importlib
import traceback
from typing import Any, Dict
import inspect

# Import the registry of fitness functions
from . import problem_functions

# mapping friendly keys to algorithm module filenames
ALGO_ALIAS = {
    "genetic": "genetic_algorithm",
    "simulated_annealing": "simulated_annealing",
    "particle_swarm": "particle_swarm",
    "differential_evolution": "differential_evolution",
    "ant_colony": "ant_colony",
}

ENTRYPOINT_NAMES = ("solve", "run", "optimize", "execute", "main")

def resolve_fitness_function(func_name_or_callable):
    """
    If the provided value is a string, try to resolve it to a callable
    in app.problem_functions. If it's already callable, return it.
    """
    if callable(func_name_or_callable):
        return func_name_or_callable
    if isinstance(func_name_or_callable, str):
        fn = getattr(problem_functions, func_name_or_callable, None)
        if fn and callable(fn):
            return fn
        raise ValueError(f"Unknown fitness function name: {func_name_or_callable}")
    raise ValueError("fitness_function must be a string name or a callable")

@celery.task(bind=True, acks_late=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 2})
def run_algorithm(self, algo_key: str, problem_payload: Dict[str, Any], params: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    - algo_key: friendly name like 'genetic' or 'genetic_algorithm'
    - problem_payload: JSON-serializable dict describing the problem; must reference a fitness function by name
    - params: optional algorithm-specific params dict
    """
    try:
        params = params or {}

        # Resolve module name
        module_name = ALGO_ALIAS.get(algo_key, algo_key)
        full_module_path = f"app.algorithms.{module_name}"
        module = importlib.import_module(full_module_path)

        # Resolve fitness function if provided as name
        if "fitness_function" in problem_payload:
            problem_payload = dict(problem_payload)  # shallow copy
            problem_payload["fitness_function"] = resolve_fitness_function(problem_payload["fitness_function"])

        # Try to find a class that implements OptimizationAlgorithm
        alg_class = None
        for _, obj in inspect.getmembers(module, inspect.isclass):
            # skip classes imported from other modules
            if obj.__module__ != module.__name__:
                continue
            # Check if class is a subclass of OptimizationAlgorithm (more reliable than name checking)
            # Also keep name-based heuristic as fallback
            try:
                from app.algorithms.base import OptimizationAlgorithm
                if issubclass(obj, OptimizationAlgorithm) and obj is not OptimizationAlgorithm:
                    alg_class = obj
                    break
            except (ImportError, TypeError):
                # Fallback to name-based heuristic
                if obj.__name__.lower().endswith("algorithm") or obj.__name__.lower().endswith("solver") or obj.__name__.lower().endswith("optimization"):
                    alg_class = obj
                    break

        # If no class found try function entrypoints
        func = None
        if alg_class is None:
            for name in ENTRYPOINT_NAMES:
                func = getattr(module, name, None)
                if callable(func):
                    break

        if alg_class:
            # instantiate and run
            instance = alg_class(problem_payload, params)
            if hasattr(instance, "initialize"):
                instance.initialize()
            if hasattr(instance, "optimize"):
                instance.optimize()
            # Use get_results if present, else assemble a default result
            result = instance.get_results() if hasattr(instance, "get_results") else {"best_solution": instance.best_solution}
            return {"algo": algo_key, "status": "SUCCESS", "result": result}

        elif func:
            result = func(problem_payload)
            return {"algo": algo_key, "status": "SUCCESS", "result": result}
        else:
            raise AttributeError(f"No runnable entrypoint found in {full_module_path}")

    except Exception as exc:
        tb = traceback.format_exc()
        # Attach traceback to the exception message for debugging (optional)
        raise self.retry(exc=RuntimeError(f"{exc}\n{tb}")) from exc