"""
Standalone Differential Evolution (DE) Test Suite

This script validates the Differential Evolution algorithm in OptimizeHub.
It runs three benchmark problems: Sphere, Rastrigin, and Negative Sphere.
Run directly:  python backend/tests/test_algorithms/test_de.py
"""

import os
import sys
import time
import numpy as np

# ---------------------------------------------------------------------
# Ensure 'app' package is importable regardless of working directory
# ---------------------------------------------------------------------
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../../.."))
if BACKEND_DIR not in sys.path:
    sys.path.append(BACKEND_DIR)

from app.algorithms.differential_evolution import DifferentialEvolution


# ---------------------------------------------------------------------
# Benchmark functions
# ---------------------------------------------------------------------
def sphere_function(x):
    """Sphere function: global minimum at 0."""
    return np.sum(x ** 2)


def rastrigin_function(x):
    """Rastrigin function: highly multimodal benchmark."""
    A = 10
    return A * len(x) + np.sum(x ** 2 - A * np.cos(2 * np.pi * x))


def negative_sphere_function(x):
    """Maximization test: inverted sphere."""
    return -np.sum(x ** 2)


# ---------------------------------------------------------------------
# Utility function to run a single test
# ---------------------------------------------------------------------
def run_test(test_name, problem, expected_optimum=0.0, tolerance=10.0):
    print(f"\n{'-'*70}")
    print(f"Running Test: {test_name}")
    print(f"{'-'*70}")

    start_time = time.time()
    de = DifferentialEvolution(problem, problem['params'])
    result = de.optimize()
    end_time = time.time()

    runtime = end_time - start_time
    final_fitness = result["best_fitness"]

    if problem["objective"] == "minimize":
        passed = final_fitness <= expected_optimum + tolerance
    else:
        passed = final_fitness >= expected_optimum - tolerance

    print(f"Result: Final Fitness = {final_fitness:.6f}, Time = {runtime:.3f}s")
    print(f"Status: {'✓ PASS' if passed else '✗ FAIL'}")

    return {
        "test_name": test_name,
        "final_fitness": final_fitness,
        "runtime": runtime,
        "all_passed": passed,
    }


# ---------------------------------------------------------------------
# Main test suite
# ---------------------------------------------------------------------
def main():
    """Run all Differential Evolution tests."""
    print("\n" + "=" * 70)
    print("DIFFERENTIAL EVOLUTION - STANDALONE TEST SUITE")
    print("=" * 70)

    dimensions = 5
    results = []

    # 1️⃣ Sphere Function (Minimize)
    problem_sphere = {
        "name": "Sphere Function",
        "dimensions": dimensions,
        "bounds": [(-100, 100) for _ in range(dimensions)],
        "objective": "minimize",
        "fitness_function": sphere_function,
        "constraints": None,
        "params": {
            "population_size": 30,
            "max_iterations": 50,
            "F": 0.8,
            "CR": 0.9,
        },
    }
    results.append(
        run_test("Sphere Function (Minimize)", problem_sphere, expected_optimum=0.0, tolerance=10.0)
    )

    # 2️⃣ Rastrigin Function (Minimize)
    problem_rastrigin = {
        "name": "Rastrigin Function",
        "dimensions": dimensions,
        "bounds": [(-5.12, 5.12) for _ in range(dimensions)],
        "objective": "minimize",
        "fitness_function": rastrigin_function,
        "constraints": None,
        "params": {
            "population_size": 40,
            "max_iterations": 100,
            "F": 0.8,
            "CR": 0.9,
        },
    }
    results.append(
        run_test("Rastrigin Function (Minimize)", problem_rastrigin, expected_optimum=0.0, tolerance=50.0)
    )

    # 3️⃣ Negative Sphere Function (Maximize)
    problem_neg_sphere = {
        "name": "Negative Sphere Function",
        "dimensions": dimensions,
        "bounds": [(-100, 100) for _ in range(dimensions)],
        "objective": "maximize",
        "fitness_function": negative_sphere_function,
        "constraints": None,
        "params": {
            "population_size": 30,
            "max_iterations": 50,
            "F": 0.8,
            "CR": 0.9,
        },
    }
    results.append(
        run_test("Negative Sphere Function (Maximize)", problem_neg_sphere, expected_optimum=0.0, tolerance=10.0)
    )

    # -----------------------------------------------------------------
    # Summary
    # -----------------------------------------------------------------
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)

    total = len(results)
    passed = sum(1 for r in results if r["all_passed"])

    for r in results:
        status = "✓ PASS" if r["all_passed"] else "✗ FAIL"
        print(f"{status}: {r['test_name']}")
        print(f"       Runtime: {r['runtime']:.3f}s, Final Fitness: {r['final_fitness']:.6f}")

    print("\n" + "=" * 70)
    print(f"Total: {passed}/{total} tests passed")
    print("=" * 70 + "\n")

    return all(r["all_passed"] for r in results)


# ---------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------
if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
