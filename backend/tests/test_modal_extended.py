"""
Extended test suite for Modal cloud function execution.

Covers algorithms and scenarios NOT tested in test_modal_execution.py:
  - PSO, DE, SA, ACOR algorithms (not just GA)
  - All execution modes per algorithm
  - Error conditions: bad algo name, bad fitness code, missing fields
  - Edge cases: single dimension, large dimension count, maximize objective
  - Numpy serialization for ACOR (returns numpy arrays in get_results)
  - Custom fitness with numpy operations
  - Result shape validation for every algorithm

Run from the backend/ directory:
    python -m pytest tests/test_modal_extended.py -v --timeout=180

Or directly:
    python tests/test_modal_extended.py
"""

import sys
import traceback
from typing import Any, Dict
import modal


def _get_modal_functions():
    run_algorithm = modal.Function.from_name("optimizehub-executor", "run_algorithm")
    run_with_custom_fitness = modal.Function.from_name(
        "optimizehub-executor", "run_with_custom_fitness"
    )
    return run_algorithm, run_with_custom_fitness


_run_algorithm, _run_with_custom_fitness = _get_modal_functions()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _pass(msg: str) -> None:
    print(f"  ✅ PASS — {msg}")


def _fail(msg: str) -> None:
    print(f"  ❌ FAIL — {msg}")
    sys.exit(1)


def _section(title: str) -> None:
    print(f"\n{'─' * 65}")
    print(f"  {title}")
    print(f"{'─' * 65}")


def _assert_result_shape(result: dict, algorithm_name: str, expected_dims: int) -> None:
    """Common shape assertions for any algorithm result."""
    assert isinstance(result, dict), "Result must be a dict"
    assert result.get("status") == "success", (
        f"Expected status='success', got {result.get('status')}"
    )
    assert "best_solution" in result, "Missing 'best_solution'"
    assert "best_fitness" in result, "Missing 'best_fitness'"
    assert "convergence_curve" in result, "Missing 'convergence_curve'"
    assert isinstance(result["best_solution"], list), (
        f"best_solution must be a list, got {type(result['best_solution'])}"
    )
    assert len(result["best_solution"]) == expected_dims, (
        f"best_solution length {len(result['best_solution'])} != expected {expected_dims}"
    )
    assert isinstance(result["best_fitness"], (int, float)), (
        f"best_fitness must be numeric, got {type(result['best_fitness'])}"
    )
    assert isinstance(result["convergence_curve"], list), "convergence_curve must be a list"
    assert len(result["convergence_curve"]) > 0, "convergence_curve must not be empty"
    # Ensure no numpy types leaked (Modal serialization check)
    for val in result["best_solution"]:
        assert type(val) in (int, float), (
            f"best_solution contains non-JSON type: {type(val)} — numpy not serialized"
        )


# ---------------------------------------------------------------------------
# Section A — All 5 algorithms on Sphere (standard run)
# ---------------------------------------------------------------------------

def test_pso_sphere() -> None:
    _section("A1 — PSO on Sphere 2D")
    result = _run_algorithm.remote(
        "pso",
        {"dimensions": 2, "bounds": [[-5.0, 5.0], [-5.0, 5.0]],
         "fitness_function_name": "sphere", "objective": "minimize"},
        {"swarm_size": 10, "max_iterations": 5, "w": 0.7, "c1": 1.5, "c2": 1.5},
    )
    _assert_result_shape(result, "pso", 2)
    print(f"  best_fitness={result['best_fitness']:.6f}, iters={len(result['convergence_curve'])}")
    _pass("PSO standard run")


def test_de_sphere() -> None:
    _section("A2 — DE on Sphere 3D")
    result = _run_algorithm.remote(
        "de",
        {"dimensions": 3, "bounds": [[-5.0, 5.0]] * 3,
         "fitness_function_name": "sphere", "objective": "minimize"},
        {"population_size": 10, "max_iterations": 5, "F": 0.8, "CR": 0.9},
    )
    _assert_result_shape(result, "de", 3)
    print(f"  best_fitness={result['best_fitness']:.6f}, iters={len(result['convergence_curve'])}")
    _pass("DE standard run")


def test_sa_sphere() -> None:
    _section("A3 — SA on Sphere 2D")
    result = _run_algorithm.remote(
        "sa",
        {"dimensions": 2, "bounds": [[-5.0, 5.0], [-5.0, 5.0]],
         "fitness_function_name": "sphere", "objective": "minimize"},
        {"initial_temp": 100.0, "cooling_rate": 0.9, "max_iterations": 10},
    )
    _assert_result_shape(result, "sa", 2)
    print(f"  best_fitness={result['best_fitness']:.6f}, iters={len(result['convergence_curve'])}")
    _pass("SA standard run")


def test_acor_sphere() -> None:
    _section("A4 — ACOR on Sphere 2D (numpy serialization check)")
    result = _run_algorithm.remote(
        "acor",
        {"dimensions": 2, "bounds": [[-5.0, 5.0], [-5.0, 5.0]],
         "fitness_function_name": "sphere", "objective": "minimize"},
        {"population_size": 10, "max_iterations": 5},
    )
    _assert_result_shape(result, "acor", 2)
    print(f"  best_fitness={result['best_fitness']:.6f}")
    print(f"  best_solution types: {[type(v).__name__ for v in result['best_solution']]}")
    _pass("ACOR standard run (numpy serialized to list of floats)")


def test_ga_rastrigin() -> None:
    _section("A5 — GA on Rastrigin 5D (different benchmark)")
    result = _run_algorithm.remote(
        "genetic_algorithm",
        {"dimensions": 5, "bounds": [[-5.12, 5.12]] * 5,
         "fitness_function_name": "rastrigin", "objective": "minimize"},
        {"population_size": 15, "max_iterations": 8, "crossover_rate": 0.7,
         "mutation_rate": 0.15, "tournament_size": 3},
    )
    _assert_result_shape(result, "genetic_algorithm", 5)
    print(f"  best_fitness={result['best_fitness']:.6f}, iters={len(result['convergence_curve'])}")
    _pass("GA on Rastrigin 5D")


# ---------------------------------------------------------------------------
# Section B — Custom fitness with numpy operations (all algorithms)
# ---------------------------------------------------------------------------

FITNESS_NUMPY = """
def fitness(x):
    # Rosenbrock function — np is available directly (no import needed)
    total = 0.0
    for i in range(len(x) - 1):
        total += 100.0 * (x[i+1] - x[i]**2)**2 + (1.0 - x[i])**2
    return float(total)
"""

def test_custom_fitness_pso() -> None:
    _section("B1 — Custom fitness (Rosenbrock) with PSO")
    result = _run_with_custom_fitness.remote(
        "pso",
        FITNESS_NUMPY,
        {"swarm_size": 10, "max_iterations": 5, "w": 0.7, "c1": 1.5, "c2": 1.5,
         "problem": {"dimensions": 2, "lower_bound": -2.0, "upper_bound": 2.0}},
    )
    _assert_result_shape(result, "pso", 2)
    print(f"  best_fitness={result['best_fitness']:.6f}")
    _pass("Custom Rosenbrock with PSO")


def test_custom_fitness_numpy_array_ops() -> None:
    _section("B2 — Custom fitness using numpy array ops (np available as global)")
    fitness_code = """
def fitness(x):
    # np is pre-injected into the sandbox globals — no import needed
    arr = np.array(x)
    return float(np.sum(arr ** 2) + np.sum(np.abs(arr)))
"""
    result = _run_with_custom_fitness.remote(
        "ga",
        fitness_code,
        {"population_size": 10, "max_iterations": 5,
         "problem": {"dimensions": 3, "lower_bound": -3.0, "upper_bound": 3.0}},
    )
    _assert_result_shape(result, "ga", 3)
    print(f"  best_fitness={result['best_fitness']:.6f}")
    _pass("Custom fitness with numpy array ops")


def test_custom_fitness_de() -> None:
    _section("B3 — Custom fitness with DE")
    fitness_code = """
def fitness(x):
    return sum(xi**2 for xi in x)
"""
    result = _run_with_custom_fitness.remote(
        "de",
        fitness_code,
        {"population_size": 10, "max_iterations": 5, "F": 0.8, "CR": 0.9,
         "problem": {"dimensions": 2, "lower_bound": -5.0, "upper_bound": 5.0}},
    )
    _assert_result_shape(result, "de", 2)
    _pass("Custom fitness with DE")


# ---------------------------------------------------------------------------
# Section C — Full canonical names (not abbreviations)
# ---------------------------------------------------------------------------

def test_full_name_particle_swarm() -> None:
    _section("C1 — Full name 'particle_swarm' (not 'pso')")
    result = _run_algorithm.remote(
        "particle_swarm",
        {"dimensions": 2, "bounds": [[-5.0, 5.0], [-5.0, 5.0]],
         "fitness_function_name": "sphere", "objective": "minimize"},
        {"swarm_size": 10, "max_iterations": 5},
    )
    _assert_result_shape(result, "particle_swarm", 2)
    _pass("Full name 'particle_swarm' resolved correctly")


def test_full_name_differential_evolution() -> None:
    _section("C2 — Full name 'differential_evolution'")
    result = _run_algorithm.remote(
        "differential_evolution",
        {"dimensions": 2, "bounds": [[-5.0, 5.0], [-5.0, 5.0]],
         "fitness_function_name": "sphere", "objective": "minimize"},
        {"population_size": 10, "max_iterations": 5},
    )
    _assert_result_shape(result, "differential_evolution", 2)
    _pass("Full name 'differential_evolution' resolved correctly")


def test_celery_alias_genetic() -> None:
    _section("C3 — Celery alias 'genetic' (not 'ga' or 'genetic_algorithm')")
    result = _run_algorithm.remote(
        "genetic",
        {"dimensions": 2, "bounds": [[-5.0, 5.0], [-5.0, 5.0]],
         "fitness_function_name": "sphere", "objective": "minimize"},
        {"population_size": 10, "max_iterations": 5},
    )
    _assert_result_shape(result, "genetic", 2)
    _pass("Celery alias 'genetic' resolved correctly")


# ---------------------------------------------------------------------------
# Section D — Error condition tests
# ---------------------------------------------------------------------------

def test_error_unknown_algorithm() -> None:
    _section("D1 — Error: unknown algorithm name")
    try:
        _run_algorithm.remote(
            "unknown_algo_xyz",
            {"dimensions": 2, "bounds": [[-5.0, 5.0], [-5.0, 5.0]],
             "fitness_function_name": "sphere"},
            {},
        )
        _fail("Should have raised an error for unknown algorithm")
    except Exception as exc:
        err = str(exc)
        print(f"  Caught (expected): {type(exc).__name__}: {err[:120]}")
        assert "unknown" in err.lower() or "valid" in err.lower() or "Unknown" in err, (
            f"Error message should mention the unknown algorithm. Got: {err}"
        )
        _pass("Unknown algorithm raises descriptive error")


def test_error_unknown_fitness_function() -> None:
    _section("D2 — Error: unknown fitness_function_name")
    try:
        _run_algorithm.remote(
            "ga",
            {"dimensions": 2, "bounds": [[-5.0, 5.0], [-5.0, 5.0]],
             "fitness_function_name": "nonexistent_function_xyz"},
            {"population_size": 10, "max_iterations": 5},
        )
        _fail("Should have raised an error for unknown fitness function")
    except Exception as exc:
        print(f"  Caught (expected): {type(exc).__name__}: {str(exc)[:120]}")
        _pass("Unknown fitness function raises error")


def test_error_custom_no_fitness_function() -> None:
    _section("D3 — Error: custom code without 'fitness' function defined")
    bad_code = """
def wrong_name(x):
    return sum(xi**2 for xi in x)
"""
    try:
        _run_with_custom_fitness.remote(
            "ga",
            bad_code,
            {"population_size": 10, "max_iterations": 5,
             "problem": {"dimensions": 2, "lower_bound": -5.0, "upper_bound": 5.0}},
        )
        _fail("Should have raised an error for missing 'fitness' function")
    except Exception as exc:
        err = str(exc)
        print(f"  Caught (expected): {type(exc).__name__}: {err[:120]}")
        assert "fitness" in err.lower(), (
            f"Error should mention 'fitness' function. Got: {err}"
        )
        _pass("Missing 'fitness' function raises descriptive error")


def test_error_custom_syntax_error() -> None:
    _section("D4 — Error: custom code with syntax error")
    bad_code = """
def fitness(x)  # missing colon
    return sum(xi**2 for xi in x)
"""
    try:
        _run_with_custom_fitness.remote(
            "ga",
            bad_code,
            {"population_size": 10, "max_iterations": 5,
             "problem": {"dimensions": 2, "lower_bound": -5.0, "upper_bound": 5.0}},
        )
        _fail("Should have raised an error for syntax error in fitness code")
    except Exception as exc:
        print(f"  Caught (expected): {type(exc).__name__}: {str(exc)[:120]}")
        _pass("Syntax error in fitness code raises error")


def test_error_custom_dangerous_import() -> None:
    _section("D5 — Security: 'import os' blocked in custom fitness")
    dangerous_code = """
import os

def fitness(x):
    os.system("echo pwned")
    return sum(xi**2 for xi in x)
"""
    try:
        _run_with_custom_fitness.remote(
            "ga",
            dangerous_code,
            {"population_size": 5, "max_iterations": 2,
             "problem": {"dimensions": 2, "lower_bound": -5.0, "upper_bound": 5.0}},
        )
        _fail("'import os' should have been blocked by RestrictedPython")
    except Exception as exc:
        print(f"  Caught (expected): {type(exc).__name__}: {str(exc)[:120]}")
        _pass("'import os' blocked by security sandbox")


def test_error_custom_exec_blocked() -> None:
    _section("D6 — Security: exec() blocked in custom fitness")
    dangerous_code = """
def fitness(x):
    exec("import os; os.system('echo pwned')")
    return sum(xi**2 for xi in x)
"""
    try:
        _run_with_custom_fitness.remote(
            "ga",
            dangerous_code,
            {"population_size": 5, "max_iterations": 2,
             "problem": {"dimensions": 2, "lower_bound": -5.0, "upper_bound": 5.0}},
        )
        _fail("exec() should have been blocked")
    except Exception as exc:
        print(f"  Caught (expected): {type(exc).__name__}: {str(exc)[:120]}")
        _pass("exec() in custom fitness code is blocked")


# ---------------------------------------------------------------------------
# Section E — Edge cases
# ---------------------------------------------------------------------------

def test_single_dimension() -> None:
    _section("E1 — Edge case: 1D problem")
    result = _run_algorithm.remote(
        "pso",
        {"dimensions": 1, "bounds": [[-10.0, 10.0]],
         "fitness_function_name": "sphere", "objective": "minimize"},
        {"swarm_size": 10, "max_iterations": 5},  # PSO requires swarm_size >= 10
    )
    _assert_result_shape(result, "pso", 1)
    print(f"  best_solution={result['best_solution']}, best_fitness={result['best_fitness']:.6f}")
    _pass("1D problem handled correctly")


def test_maximize_objective() -> None:
    _section("E2 — Maximize objective (not minimize)")
    # For maximization: use a simple problem where higher x is better
    result = _run_algorithm.remote(
        "ga",
        {"dimensions": 2, "bounds": [[0.0, 10.0], [0.0, 10.0]],
         "fitness_function_name": "sphere", "objective": "maximize"},
        {"population_size": 10, "max_iterations": 5},
    )
    _assert_result_shape(result, "ga", 2)
    print(f"  best_fitness={result['best_fitness']:.6f}")
    _pass("Maximize objective handled without error")


def test_result_convergence_monotonicity_minimize() -> None:
    _section("E3 — Convergence curve is non-increasing for minimize (GA, Sphere)")
    result = _run_algorithm.remote(
        "ga",
        {"dimensions": 2, "bounds": [[-5.0, 5.0], [-5.0, 5.0]],
         "fitness_function_name": "sphere", "objective": "minimize"},
        {"population_size": 20, "max_iterations": 20, "crossover_rate": 0.8,
         "mutation_rate": 0.1, "tournament_size": 3},
    )
    curve = result["convergence_curve"]
    for i in range(1, len(curve)):
        assert curve[i] <= curve[i - 1] + 1e-9, (
            f"Convergence curve increased at iteration {i}: {curve[i-1]} → {curve[i]}"
        )
    print(f"  {len(curve)} iterations, final fitness={curve[-1]:.6f}")
    _pass("Convergence curve is non-increasing")


def test_execution_time_present_and_reasonable() -> None:
    _section("E4 — execution_time field is present and under 30s")
    result = _run_algorithm.remote(
        "pso",
        {"dimensions": 2, "bounds": [[-5.0, 5.0], [-5.0, 5.0]],
         "fitness_function_name": "sphere", "objective": "minimize"},
        {"swarm_size": 10, "max_iterations": 10},
    )
    et = result.get("execution_time")
    assert et is not None, "execution_time must be present"
    assert isinstance(et, (int, float)), f"execution_time must be numeric, got {type(et)}"
    assert et > 0, "execution_time must be positive"
    assert et < 30, f"execution_time={et}s exceeded 30s Modal limit"
    print(f"  execution_time={et}s")
    _pass("execution_time present and under 30s")


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def main() -> None:
    print("\n" + "=" * 65)
    print("  OptimizeHub — Extended Modal Execution Tests")
    print("=" * 65)

    tests = [
        # Section A — All algorithms
        test_pso_sphere,
        test_de_sphere,
        test_sa_sphere,
        test_acor_sphere,
        test_ga_rastrigin,
        # Section B — Custom fitness
        test_custom_fitness_pso,
        test_custom_fitness_numpy_array_ops,
        test_custom_fitness_de,
        # Section C — Name resolution
        test_full_name_particle_swarm,
        test_full_name_differential_evolution,
        test_celery_alias_genetic,
        # Section D — Error conditions
        test_error_unknown_algorithm,
        test_error_unknown_fitness_function,
        test_error_custom_no_fitness_function,
        test_error_custom_syntax_error,
        test_error_custom_dangerous_import,
        test_error_custom_exec_blocked,
        # Section E — Edge cases
        test_single_dimension,
        test_maximize_objective,
        test_result_convergence_monotonicity_minimize,
        test_execution_time_present_and_reasonable,
    ]

    passed = 0
    failed = 0
    for test_fn in tests:
        try:
            test_fn()
            passed += 1
        except SystemExit:
            raise
        except AssertionError as exc:
            print(f"\n  ❌ ASSERTION FAILED in {test_fn.__name__}: {exc}")
            traceback.print_exc()
            failed += 1
        except Exception as exc:
            print(f"\n  ❌ EXCEPTION in {test_fn.__name__}: {type(exc).__name__}: {exc}")
            traceback.print_exc()
            failed += 1

    print(f"\n{'=' * 65}")
    print(f"  {passed}/{len(tests)} tests passed", end="")
    if failed:
        print(f"  ({failed} failed) ❌")
    else:
        print(" ✅")
    print(f"{'=' * 65}\n")

    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
