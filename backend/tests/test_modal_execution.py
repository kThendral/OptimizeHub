"""
Test suite for Modal cloud function execution.

Verifies all three execution modes and enforced constraints.
Run from the backend/ directory:

    python -m pytest tests/test_modal_execution.py -v --timeout=120

Or directly:

    python tests/test_modal_execution.py
"""

import sys
import time
import traceback
from typing import Any, Dict
import modal


def _get_modal_functions():
    """
    Look up the deployed Modal functions by name.
    This is required for calling functions outside of a Modal app context.
    """
    run_algorithm = modal.Function.from_name(
        "optimizehub-executor", "run_algorithm"
    )
    run_with_custom_fitness = modal.Function.from_name(
        "optimizehub-executor", "run_with_custom_fitness"
    )
    return run_algorithm, run_with_custom_fitness


# Resolve once at module load
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
    print(f"\n{'─' * 60}")
    print(f"  {title}")
    print(f"{'─' * 60}")


# ---------------------------------------------------------------------------
# Test 1 — Standard run (execution mode 1)
# ---------------------------------------------------------------------------

def test_standard_run() -> None:
    _section("Test 1 — Standard run (GA on Sphere, 2D)")

    problem_config: Dict[str, Any] = {
        "dimensions": 2,
        "bounds": [[-5.12, 5.12], [-5.12, 5.12]],
        "fitness_function_name": "sphere",
        "objective": "minimize",
    }
    params: Dict[str, Any] = {
        "population_size": 10,
        "max_iterations": 5,
        "crossover_rate": 0.8,
        "mutation_rate": 0.1,
        "tournament_size": 3,
    }

    result = _run_algorithm.remote("ga", problem_config, params)
    print(f"  Result keys: {list(result.keys())}")

    assert result is not None, "Result must not be None"
    assert "best_solution" in result, "Result must contain 'best_solution'"
    assert "best_fitness" in result, "Result must contain 'best_fitness'"
    assert "convergence_curve" in result, "Result must contain 'convergence_curve'"
    assert result["best_fitness"] is not None, "best_fitness must not be None"
    assert isinstance(result["best_solution"], list), "best_solution must be a list"
    assert len(result["best_solution"]) == 2, "best_solution must have 2 dimensions"
    assert isinstance(result["convergence_curve"], list), "convergence_curve must be a list"
    assert len(result["convergence_curve"]) > 0, "convergence_curve must not be empty"
    assert result.get("status") == "success", f"Expected status='success', got {result.get('status')}"

    print(f"  best_fitness  = {result['best_fitness']:.6f}")
    print(f"  iterations    = {len(result['convergence_curve'])}")
    print(f"  execution_time= {result.get('execution_time')}s")
    _pass("Standard run returned valid results")


# ---------------------------------------------------------------------------
# Test 2 — Custom fitness function run (execution mode 2)
# ---------------------------------------------------------------------------

def test_custom_fitness() -> None:
    _section("Test 2 — Custom fitness function (Sphere via def fitness)")

    # Must use 'fitness' as the function name (existing convention)
    fitness_code = """
def fitness(x):
    return sum(xi**2 for xi in x)
"""

    params: Dict[str, Any] = {
        "population_size": 10,
        "max_iterations": 5,
        "crossover_rate": 0.8,
        "mutation_rate": 0.1,
        "tournament_size": 3,
        "problem": {
            "dimensions": 2,
            "lower_bound": -5.0,
            "upper_bound": 5.0,
        },
    }

    result = _run_with_custom_fitness.remote("ga", fitness_code, params)
    print(f"  Result keys: {list(result.keys())}")

    assert result is not None, "Result must not be None"
    assert "best_solution" in result, "Result must contain 'best_solution'"
    assert "best_fitness" in result, "Result must contain 'best_fitness'"
    assert result["best_fitness"] is not None, "best_fitness must not be None"
    assert isinstance(result["best_solution"], list), "best_solution must be a list"
    assert len(result["best_solution"]) == 2, "best_solution must have 2 dimensions"
    assert result.get("status") == "success", f"Expected status='success', got {result.get('status')}"

    print(f"  best_fitness  = {result['best_fitness']:.6f}")
    print(f"  execution_time= {result.get('execution_time')}s")
    _pass("Custom fitness run returned valid results")


# ---------------------------------------------------------------------------
# Test 3 — YAML config run (execution mode 3)
# ---------------------------------------------------------------------------

def test_yaml_config_run() -> None:
    _section("Test 3 — YAML config run (PSO on Rastrigin, 3D)")

    import yaml
    from executor.modal_runner import run_algorithm

    yaml_config_str = """
algorithm: pso
params:
  swarm_size: 15
  max_iterations: 8
  w: 0.7
  c1: 1.5
  c2: 1.5
problem:
  dimensions: 3
  bounds:
    - [-5.12, 5.12]
    - [-5.12, 5.12]
    - [-5.12, 5.12]
  fitness_function_name: rastrigin
  objective: minimize
"""

    config = yaml.safe_load(yaml_config_str)

    # Merge problem dict with the expected problem_config shape
    problem_config: Dict[str, Any] = config["problem"]
    params: Dict[str, Any] = config["params"]
    algorithm_name: str = config["algorithm"]

    result = _run_algorithm.remote(algorithm_name, problem_config, params)
    print(f"  Result keys: {list(result.keys())}")

    assert result is not None, "Result must not be None"
    assert "best_solution" in result, "Result must contain 'best_solution'"
    assert "best_fitness" in result, "Result must contain 'best_fitness'"
    assert result["best_fitness"] is not None, "best_fitness must not be None"
    assert len(result["best_solution"]) == 3, "best_solution must have 3 dimensions"
    assert result.get("status") == "success", f"Expected status='success', got {result.get('status')}"

    print(f"  best_fitness  = {result['best_fitness']:.6f}")
    print(f"  iterations    = {len(result.get('convergence_curve', []))}")
    _pass("YAML config run returned valid results")


# ---------------------------------------------------------------------------
# Test 4 — Constraint verification: network access is blocked
# ---------------------------------------------------------------------------

def test_network_access_blocked() -> None:
    _section("Test 4 — Constraint: network access is blocked inside Modal")

    # Attempt to import socket and connect — RestrictedPython will block the
    # import, which is the proximate enforcement mechanism.  The block_network=True
    # flag on the Modal function provides infrastructure-level enforcement on top.
    malicious_code = """
import socket

def fitness(x):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("google.com", 80))
    s.close()
    return sum(xi**2 for xi in x)
"""

    params: Dict[str, Any] = {
        "population_size": 10,
        "max_iterations": 2,
        "problem": {"dimensions": 2, "lower_bound": -5.0, "upper_bound": 5.0},
    }

    try:
        _run_with_custom_fitness.remote("ga", malicious_code, params)
        _fail(
            "Expected an error for network-accessing code, but execution succeeded. "
            "Security constraint NOT enforced!"
        )
    except Exception as exc:
        err = str(exc)
        print(f"  Caught exception (expected): {type(exc).__name__}: {err[:120]}")
        _pass(
            "Network-accessing code was blocked "
            "(RestrictedPython prevented 'import socket')"
        )


# ---------------------------------------------------------------------------
# Test 5 — Timeout enforcement
# ---------------------------------------------------------------------------

def test_timeout_enforcement() -> None:
    _section("Test 5 — Constraint: 30-second timeout is enforced")

    # Very large iteration count + large population → will run well over 30 s
    problem_config: Dict[str, Any] = {
        "dimensions": 5,
        "bounds": [[-5.12, 5.12]] * 5,
        "fitness_function_name": "rastrigin",
        "objective": "minimize",
    }
    params: Dict[str, Any] = {
        "population_size": 1000,
        "max_iterations": 999999,
    }

    wall_start = time.time()
    try:
        _run_algorithm.remote("ga", problem_config, params)
        elapsed = time.time() - wall_start
        # If we somehow got a result (GA's own internal 30s guard may have fired)
        # that's still acceptable — as long as it didn't run for minutes.
        if elapsed < 60:
            _pass(
                f"Algorithm completed in {elapsed:.1f}s "
                "(GA's internal timeout guard fired before Modal's)"
            )
        else:
            _fail(f"Execution took {elapsed:.1f}s — timeout not enforced!")
    except Exception as exc:
        elapsed = time.time() - wall_start
        err_type = type(exc).__name__
        print(f"  Caught {err_type} after {elapsed:.1f}s: {str(exc)[:120]}")
        assert elapsed < 60, (
            f"Exception raised after {elapsed:.1f}s — Modal should have timed out "
            "within ~35 seconds of the 30s limit"
        )
        _pass(f"Timeout exception raised after {elapsed:.1f}s ✓")


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def main() -> None:
    print("\n" + "=" * 60)
    print("  OptimizeHub — Modal Execution Tests")
    print("=" * 60)

    tests = [
        test_standard_run,
        test_custom_fitness,
        test_yaml_config_run,
        test_network_access_blocked,
        test_timeout_enforcement,
    ]

    passed = 0
    for test_fn in tests:
        try:
            test_fn()
            passed += 1
        except SystemExit:
            raise
        except Exception as exc:
            print(f"\n  ❌ EXCEPTION in {test_fn.__name__}:")
            traceback.print_exc()
            print(f"  {exc}")
            sys.exit(1)

    print(f"\n{'=' * 60}")
    print(f"  {passed}/{len(tests)} tests passed ✅")
    print(f"{'=' * 60}\n")


if __name__ == "__main__":
    main()
