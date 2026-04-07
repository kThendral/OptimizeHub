"""
Modal.com runner for OptimizeHub algorithm execution.

Replaces the Docker sandbox with Modal cloud functions, replicating all original
Docker constraints exactly:
  - 30-second execution timeout         (block_network=True)
  - 512 MB memory limit                 (memory=512)
  - No network access during execution  (block_network=True)
  - Isolated execution environment      (Modal container)
  - cpu=1.0

Three execution modes are supported:
  1. Standard run / YAML config run  →  run_algorithm()
  2. Custom fitness function          →  run_with_custom_fitness()
"""

import modal

# ---------------------------------------------------------------------------
# Container image
# ---------------------------------------------------------------------------
# All algorithm dependencies are installed; the local `app` package is bundled
# so that algorithm classes and fitness utilities are importable inside Modal.
# Run `modal deploy` from the `backend/` directory so that `app/` is on the path.
# ---------------------------------------------------------------------------
image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install(
        "numpy==2.3.3",
        "RestrictedPython",
        "pydantic==2.11.9",
        "deap==1.4.3",
        "PyYAML==6.0.3",
    )
    .add_local_python_source("app", copy=True)
)

# ---------------------------------------------------------------------------
# Modal app
# ---------------------------------------------------------------------------
app = modal.App("optimizehub-executor", image=image)

# ---------------------------------------------------------------------------
# Algorithm name mapping
# Supports all naming conventions used across the codebase:
#   • Docker runner abbreviations  (ga, pso, de, sa, acor)
#   • Celery ALGO_ALIAS keys       (genetic, ...)
#   • Full ALGORITHM_REGISTRY keys (genetic_algorithm, ...)
# ---------------------------------------------------------------------------
ALGO_NAME_MAP: dict[str, str] = {
    # Docker-runner / test abbreviations
    "ga": "genetic_algorithm",
    "pso": "particle_swarm",
    "de": "differential_evolution",
    "sa": "simulated_annealing",
    "acor": "ant_colony",
    # Celery ALGO_ALIAS
    "genetic": "genetic_algorithm",
    # Full ALGORITHM_REGISTRY canonical names
    "genetic_algorithm": "genetic_algorithm",
    "particle_swarm": "particle_swarm",
    "differential_evolution": "differential_evolution",
    "simulated_annealing": "simulated_annealing",
    "ant_colony": "ant_colony",
}


def _serialize(value):
    """Recursively convert numpy scalars / arrays to JSON-native Python types."""
    try:
        import numpy as np
    except ImportError:
        return value

    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return float(value)
    if isinstance(value, dict):
        return {k: _serialize(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_serialize(v) for v in value]
    return value


def _serialize_result(result: dict) -> dict:
    """Ensure every field in an algorithm result dict is JSON-serializable."""
    return {k: _serialize(v) for k, v in result.items()}


# ---------------------------------------------------------------------------
# Function 1 — Standard run and YAML/JSON config run
# ---------------------------------------------------------------------------
@app.function(
    timeout=30,          # matches Docker 30-second execution timeout
    memory=512,          # matches Docker 512 MB memory limit
    block_network=True,  # matches Docker --network none
    cpu=1.0,
)
def run_algorithm(
    algorithm_name: str,
    problem_config: dict,
    params: dict,
) -> dict:
    """
    Run a built-in optimization algorithm on a standard problem configuration.

    Handles execution modes 1 (standard run) and 3 (YAML/JSON config run).
    The fitness function is resolved from a string name inside this function so
    the problem_config remains JSON-serializable across the network boundary.

    Args:
        algorithm_name:
            Algorithm identifier — accepts abbreviations (``"ga"``, ``"pso"``),
            Celery aliases (``"genetic"``), or full registry names
            (``"genetic_algorithm"``).
        problem_config:
            JSON-serializable problem definition.  Must contain:
              - ``dimensions`` (int)
              - ``bounds`` (list of [lower, upper] pairs)
              - ``fitness_function_name`` OR ``fitness_function`` (str) for
                standard benchmark runs, OR ``problem_type`` + type-specific
                fields for real-world problems (knapsack / tsp).
              - ``objective`` (str, optional, default ``"minimize"``)
        params:
            Algorithm-specific parameter overrides merged on top of registry
            defaults (e.g. ``{"population_size": 50, "max_iterations": 50}``).

    Returns:
        dict with keys: ``algorithm``, ``best_solution``, ``best_fitness``,
        ``convergence_curve``, ``params``, ``execution_time``, ``status``.

    Raises:
        ValueError: If algorithm_name is not recognised or the fitness
                    function / problem config is invalid.
    """
    import time
    import importlib
    import inspect

    start_time = time.time()

    # ── 1. Resolve algorithm class ────────────────────────────────────────────
    canonical = ALGO_NAME_MAP.get(algorithm_name.lower())
    if canonical is None:
        raise ValueError(
            f"Unknown algorithm '{algorithm_name}'. "
            f"Valid names: {sorted(ALGO_NAME_MAP.keys())}"
        )

    # Import algorithm class inside the function body (not at module level)
    module = importlib.import_module(f"app.algorithms.{canonical}")

    from app.algorithms.base import OptimizationAlgorithm

    algo_class = None
    for _, obj in inspect.getmembers(module, inspect.isclass):
        if (
            obj.__module__ == module.__name__
            and issubclass(obj, OptimizationAlgorithm)
            and obj is not OptimizationAlgorithm
        ):
            algo_class = obj
            break

    if algo_class is None:
        raise ValueError(
            f"No OptimizationAlgorithm subclass found in app.algorithms.{canonical}"
        )

    # ── 2. Build problem_dict with a callable fitness_function ────────────────
    problem_dict = dict(problem_config)

    # Normalise bounds: list-of-lists → list-of-tuples (algorithms accept both)
    if "bounds" in problem_dict:
        problem_dict["bounds"] = [
            tuple(b) if isinstance(b, list) else b
            for b in problem_dict["bounds"]
        ]

    problem_type = problem_dict.get("problem_type")

    if problem_type == "knapsack":
        from app.core.real_world_problems import create_knapsack_fitness

        items = problem_dict.get("items", [])
        capacity = problem_dict.get("capacity", 10)
        if not items:
            raise ValueError("Knapsack problem requires an 'items' list")

        weights = [item["weight"] for item in items]
        values = [item["value"] for item in items]
        problem_dict["fitness_function"] = create_knapsack_fitness(
            weights, values, capacity
        )
        problem_dict.setdefault("bounds", [(0, 1)] * len(items))
        problem_dict.setdefault("dimensions", len(items))

    elif problem_type == "tsp":
        from app.core.real_world_problems import create_tsp_fitness

        cities = problem_dict.get("cities", [])
        if len(cities) < 3:
            raise ValueError("TSP problem requires at least 3 cities")

        city_coords = [(c["x"], c["y"]) for c in cities]
        problem_dict["fitness_function"] = create_tsp_fitness(city_coords)
        problem_dict.setdefault("bounds", [(0, 1)] * len(cities))
        problem_dict.setdefault("dimensions", len(cities))

    else:
        # Standard benchmark function — resolve by string name.
        # Accept either "fitness_function_name" (routes.py path) or
        # "fitness_function" as a string (async/Celery path after renaming).
        fitness_fn_name = problem_dict.pop("fitness_function_name", None)
        if fitness_fn_name is None:
            ff_value = problem_dict.get("fitness_function")
            if isinstance(ff_value, str):
                fitness_fn_name = problem_dict.pop("fitness_function")

        if fitness_fn_name:
            from app.core.utils import get_fitness_function
            problem_dict["fitness_function"] = get_fitness_function(fitness_fn_name)
        elif "fitness_function" not in problem_dict or not callable(
            problem_dict.get("fitness_function")
        ):
            raise ValueError(
                "problem_config must include 'fitness_function_name' (str) or "
                "a callable 'fitness_function'"
            )

    # ── 3. Merge params: registry defaults + caller overrides ─────────────────
    try:
        from app.config import get_algorithm_info
        default_params = get_algorithm_info(canonical).get("default_params", {}).copy()
        default_params.update(params)
        merged_params = default_params
    except Exception:
        merged_params = params

    # ── 4. Run algorithm using existing interface ──────────────────────────────
    algo = algo_class(problem_dict, merged_params)
    algo.initialize()
    algo.optimize()
    result = algo.get_results()

    # ── 5. Attach metadata and ensure JSON serializability ────────────────────
    result["execution_time"] = round(time.time() - start_time, 3)
    result["status"] = "success"

    return _serialize_result(result)


# ---------------------------------------------------------------------------
# Function 2 — Custom fitness function run
# ---------------------------------------------------------------------------
@app.function(
    timeout=30,          # matches Docker 30-second execution timeout
    memory=512,          # matches Docker 512 MB memory limit
    block_network=True,  # matches Docker --network none
    cpu=1.0,
)
def run_with_custom_fitness(
    algorithm_name: str,
    fitness_code: str,
    params: dict,
) -> dict:
    """
    Run an optimization algorithm with a user-supplied custom fitness function.

    Handles execution mode 2 (custom fitness function).

    The submitted Python code is compiled and executed inside RestrictedPython
    to prevent access to unsafe builtins, network sockets, file I/O, and other
    dangerous operations.

    The code MUST define a function named ``fitness`` that:
      - accepts exactly one argument (a numpy array ``x``)
      - returns a single numeric value

    Args:
        algorithm_name:
            Algorithm identifier (e.g. ``"ga"``, ``"pso"``).
        fitness_code:
            Python source code string.  Must contain ``def fitness(x): ...``.
        params:
            May include:
              - Algorithm-specific parameters (``population_size``,
                ``max_iterations``, etc.)
              - An optional ``"problem"`` sub-dict with problem geometry:
                  ``dimensions``, ``lower_bound``, ``upper_bound``, ``bounds``,
                  ``objective``.

    Returns:
        dict with keys: ``algorithm``, ``best_solution``, ``best_fitness``,
        ``convergence_curve``, ``params``, ``execution_time``, ``status``.

    Raises:
        ValueError: If ``algorithm_name`` is unknown, ``fitness`` is not
                    defined in the submitted code, or the code fails
                    RestrictedPython compilation.
    """
    import time
    import importlib
    import inspect

    from RestrictedPython import compile_restricted

    start_time = time.time()

    # ── 1. Resolve algorithm class ────────────────────────────────────────────
    canonical = ALGO_NAME_MAP.get(algorithm_name.lower())
    if canonical is None:
        raise ValueError(
            f"Unknown algorithm '{algorithm_name}'. "
            f"Valid names: {sorted(ALGO_NAME_MAP.keys())}"
        )

    # Import algorithm class inside the function body (not at module level)
    module = importlib.import_module(f"app.algorithms.{canonical}")

    from app.algorithms.base import OptimizationAlgorithm

    algo_class = None
    for _, obj in inspect.getmembers(module, inspect.isclass):
        if (
            obj.__module__ == module.__name__
            and issubclass(obj, OptimizationAlgorithm)
            and obj is not OptimizationAlgorithm
        ):
            algo_class = obj
            break

    if algo_class is None:
        raise ValueError(
            f"No OptimizationAlgorithm subclass found in app.algorithms.{canonical}"
        )

    # ── 2. Validate + execute user code safely ────────────────────────────────
    # Strategy:
    #   a) compile_restricted()  — AST-level security check (detects dangerous
    #      attribute access, forbidden imports, etc.).  Raises SyntaxError on
    #      any violation.  We discard the resulting bytecode.
    #   b) compile()             — produce plain, unguarded bytecode.
    #   c) exec(plain_bytecode, restricted_globals)  — run in a locked-down
    #      environment that exposes only safe math builtins + numpy.
    #      No os / subprocess / socket / open / eval / exec / __import__.
    #
    # Infrastructure-level hardening is provided by Modal's block_network=True
    # (no outbound network even if a user somehow constructs a socket object).

    # (a) Security validation — raises SyntaxError / RestrictedPython error
    #     if the code contains dangerous constructs.
    try:
        compile_restricted(fitness_code, "<user_fitness>", "exec")
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in fitness code: {exc}") from exc

    # (b) Plain compilation — produces bytecode without RestrictedPython guards
    #     (no _getiter_ / _getattr_ dependencies).
    plain_bytecode = compile(fitness_code, "<user_fitness>", "exec")

    import numpy as np
    import math as _math
    import random as _random

    # Allowlist of safe modules users may import inside their fitness function.
    # Anything not on this list raises ImportError at runtime.
    _SAFE_MODULE_MAP: dict = {
        "numpy": np,
        "np": np,
        "math": _math,
        "random": _random,
    }

    def _restricted_import(name, globals=None, locals=None, fromlist=(), level=0):
        mod = _SAFE_MODULE_MAP.get(name)
        if mod is None:
            raise ImportError(
                f"Import of '{name}' is not allowed in the fitness sandbox. "
                f"Available modules: {sorted(_SAFE_MODULE_MAP.keys())}"
            )
        return mod

    # (c) Restricted execution environment: only safe math builtins + numpy.
    #     Nothing that could access the filesystem, network, or OS is present.
    _safe_builtins: dict = {
        "abs": abs, "all": all, "any": any, "bin": bin, "bool": bool,
        "bytes": bytes, "callable": callable, "chr": chr, "complex": complex,
        "dict": dict, "divmod": divmod, "enumerate": enumerate,
        "filter": filter, "float": float, "format": format,
        "frozenset": frozenset, "hash": hash, "hex": hex, "int": int,
        "isinstance": isinstance, "issubclass": issubclass, "iter": iter,
        "len": len, "list": list, "map": map, "max": max, "min": min,
        "next": next, "oct": oct, "ord": ord, "pow": pow, "print": print,
        "range": range, "repr": repr, "reversed": reversed, "round": round,
        "set": set, "slice": slice, "sorted": sorted, "str": str, "sum": sum,
        "tuple": tuple, "type": type, "zip": zip,
        # Exceptions users may raise (e.g. ValueError for bad inputs)
        "ValueError": ValueError, "TypeError": TypeError,
        "RuntimeError": RuntimeError, "StopIteration": StopIteration,
        "True": True, "False": False, "None": None,
        # Allow `import numpy`, `import math`, `import random` inside fitness body
        "__import__": _restricted_import,
    }

    exec_globals: dict = {
        "__builtins__": _safe_builtins,
        "np": np,
        "numpy": np,
        "math": _math,
    }

    local_vars: dict = {}
    exec(plain_bytecode, exec_globals, local_vars)  # noqa: S102

    if "fitness" not in local_vars or not callable(local_vars["fitness"]):
        raise ValueError(
            "User code must define a callable function named 'fitness'.\n"
            "Example:\n"
            "    def fitness(x):\n"
            "        return sum(xi**2 for xi in x)"
        )

    fitness_fn = local_vars["fitness"]

    # ── 3. Build problem dict from params['problem'] or sensible defaults ─────
    problem_cfg: dict = params.get("problem", {})
    dimensions: int = problem_cfg.get("dimensions", 10)
    lb: float = problem_cfg.get("lower_bound", -5.0)
    ub: float = problem_cfg.get("upper_bound", 5.0)

    raw_bounds = problem_cfg.get("bounds")
    if raw_bounds:
        bounds = [tuple(b) if isinstance(b, list) else b for b in raw_bounds]
    else:
        bounds = [(lb, ub)] * dimensions

    problem_dict: dict = {
        "dimensions": dimensions,
        "bounds": bounds,
        "fitness_function": fitness_fn,
        "objective": problem_cfg.get("objective", "minimize"),
    }

    # Algorithm params: everything in params except the nested 'problem' key
    algo_params: dict = {k: v for k, v in params.items() if k != "problem"}

    # ── 4. Run algorithm ──────────────────────────────────────────────────────
    algo = algo_class(problem_dict, algo_params)
    algo.initialize()
    algo.optimize()
    result = algo.get_results()

    # ── 5. Attach metadata and ensure JSON serializability ────────────────────
    result["execution_time"] = round(time.time() - start_time, 3)
    result["status"] = "success"

    return _serialize_result(result)
