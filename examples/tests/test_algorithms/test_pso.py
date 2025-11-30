"""
Standalone test for Particle Swarm Optimization algorithm.
Tests PSO on three benchmark functions:
1. Sphere function (minimize)
2. Rastrigin function (minimize)
3. Negative Sphere function (maximize)
"""

import numpy as np
import time
import sys
from pathlib import Path

# Add backend to path for imports
backend_path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_path))

from app.algorithms.particle_swarm import ParticleSwarmOptimization


# Test Functions
def sphere_function(x):
    """
    Sphere function: f(x) = sum(x_i^2)
    Global minimum: f(0,0,...,0) = 0
    Search domain: [-100, 100]
    """
    return np.sum(x ** 2)


def rastrigin_function(x):
    """
    Rastrigin function: f(x) = 10*n + sum(x_i^2 - 10*cos(2*pi*x_i))
    Global minimum: f(0,0,...,0) = 0
    Search domain: [-5.12, 5.12]
    More challenging due to many local minima
    """
    n = len(x)
    return 10 * n + np.sum(x ** 2 - 10 * np.cos(2 * np.pi * x))


def negative_sphere_function(x):
    """
    Negative Sphere function: f(x) = -sum(x_i^2)
    Global maximum: f(0,0,...,0) = 0
    Search domain: [-100, 100]
    """
    return -np.sum(x ** 2)


def run_test(test_name, problem, expected_optimum=0.0, tolerance=1.0):
    """
    Run PSO test and verify results.

    Args:
        test_name: Name of the test
        problem: Problem dictionary
        expected_optimum: Expected optimal fitness value
        tolerance: Acceptable deviation from optimum

    Returns:
        dict: Test results
    """
    print(f"\n{'='*70}")
    print(f"TEST: {test_name}")
    print(f"{'='*70}")

    # Initialize PSO
    pso = ParticleSwarmOptimization(problem, problem['params'])

    # Run optimization
    start_time = time.time()
    pso.initialize()
    pso.optimize()
    runtime = time.time() - start_time

    # Get results
    results = pso.get_results()
    best_solution = np.array(results['best_solution'])
    convergence_curve = results['convergence_curve']
    final_fitness = convergence_curve[-1]
    initial_fitness = convergence_curve[0]

    # Verification checks
    print(f"\nResults:")
    print(f"  Runtime: {runtime:.3f} seconds")
    print(f"  Best solution: {best_solution}")
    print(f"  Final fitness: {final_fitness:.6f}")
    print(f"  Initial fitness: {initial_fitness:.6f}")
    print(f"  Improvement: {abs(initial_fitness - final_fitness):.6f}")
    print(f"  Distance from origin: {np.linalg.norm(best_solution):.6f}")
    print(f"  Iterations: {len(convergence_curve) - 1}")

    # Checks
    checks = {
        'completes_without_error': True,
        'under_30_seconds': runtime < 30,
        'solution_near_origin': np.linalg.norm(best_solution) < 10.0,
        'fitness_near_optimum': abs(final_fitness - expected_optimum) < tolerance,
        'shows_improvement': abs(final_fitness) < abs(initial_fitness),
        'convergence_curve_valid': len(convergence_curve) > 1
    }

    print(f"\nVerification:")
    for check_name, passed in checks.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {status}: {check_name}")

    all_passed = all(checks.values())
    print(f"\n{'='*70}")
    print(f"Overall: {'✓ ALL CHECKS PASSED' if all_passed else '✗ SOME CHECKS FAILED'}")
    print(f"{'='*70}")

    return {
        'test_name': test_name,
        'runtime': runtime,
        'final_fitness': final_fitness,
        'best_solution': best_solution.tolist(),
        'checks': checks,
        'all_passed': all_passed,
        'convergence_curve': convergence_curve
    }


def main():
    """Run all PSO tests."""
    print("\n" + "="*70)
    print("PARTICLE SWARM OPTIMIZATION - STANDALONE TEST SUITE")
    print("="*70)

    dimensions = 5
    test_results = []

    # Test 1: Sphere Function (Minimize)
    problem_sphere = {
        'name': 'Sphere Function',
        'dimensions': dimensions,
        'bounds': [(-100, 100) for _ in range(dimensions)],
        'objective': 'minimize',
        'fitness_function': sphere_function,
        'constraints': None,
        'params': {
            'swarm_size': 30,
            'max_iterations': 50,
            'w': 0.7,
            'c1': 1.5,
            'c2': 1.5
        }
    }
    result1 = run_test(
        "Sphere Function (Minimize)",
        problem_sphere,
        expected_optimum=0.0,
        tolerance=10.0
    )
    test_results.append(result1)

    # Test 2: Rastrigin Function (Minimize)
    problem_rastrigin = {
        'name': 'Rastrigin Function',
        'dimensions': dimensions,
        'bounds': [(-5.12, 5.12) for _ in range(dimensions)],
        'objective': 'minimize',
        'fitness_function': rastrigin_function,
        'constraints': None,
        'params': {
            'swarm_size': 40,  # More particles for harder problem
            'max_iterations': 100,  # More iterations
            'w': 0.7,
            'c1': 1.5,
            'c2': 1.5
        }
    }
    result2 = run_test(
        "Rastrigin Function (Minimize)",
        problem_rastrigin,
        expected_optimum=0.0,
        tolerance=50.0  # Higher tolerance for harder problem
    )
    test_results.append(result2)

    # Test 3: Negative Sphere Function (Maximize)
    problem_neg_sphere = {
        'name': 'Negative Sphere Function',
        'dimensions': dimensions,
        'bounds': [(-100, 100) for _ in range(dimensions)],
        'objective': 'maximize',
        'fitness_function': negative_sphere_function,
        'constraints': None,
        'params': {
            'swarm_size': 30,
            'max_iterations': 50,
            'w': 0.7,
            'c1': 1.5,
            'c2': 1.5
        }
    }
    result3 = run_test(
        "Negative Sphere Function (Maximize)",
        problem_neg_sphere,
        expected_optimum=0.0,
        tolerance=10.0
    )
    test_results.append(result3)

    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)

    total_tests = len(test_results)
    passed_tests = sum(1 for r in test_results if r['all_passed'])

    for result in test_results:
        status = "✓ PASS" if result['all_passed'] else "✗ FAIL"
        print(f"{status}: {result['test_name']}")
        print(f"       Runtime: {result['runtime']:.3f}s, Final Fitness: {result['final_fitness']:.6f}")

    print(f"\n{'='*70}")
    print(f"Total: {passed_tests}/{total_tests} tests passed")
    print(f"{'='*70}\n")

    return all(r['all_passed'] for r in test_results)


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
