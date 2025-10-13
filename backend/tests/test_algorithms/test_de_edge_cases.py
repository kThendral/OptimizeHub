"""
Compact Edge-Case Test Suite for Differential Evolution
"""

import numpy as np
import sys
from pathlib import Path

# Add backend to path for imports
backend_path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_path))

from app.algorithms.differential_evolution import DifferentialEvolution

# -------------------- Test Functions --------------------
def sphere(x):
    return np.sum(x**2)

def negative_sphere(x):
    return -np.sum(x**2)

# -------------------- Edge Case Tests --------------------
def run_edge_case_tests():
    print("\n" + "="*60)
    print("DIFFERENTIAL EVOLUTION - EDGE CASE TESTS")
    print("="*60)

    tests_passed = 0
    total_tests = 0

    # ---- Test 1: Missing 'dimensions' ----
    total_tests += 1
    try:
        problem = {'bounds': [(0,1)], 'fitness_function': sphere}
        de = DifferentialEvolution(problem, {'population_size': 20, 'max_iterations': 10})
        de.initialize()
        print("[Test 1] ❌ FAIL: Did not raise error for missing dimensions")
    except ValueError as e:
        print(f"[Test 1] ✓ PASS: {e}")
        tests_passed += 1

    # ---- Test 2: Population size < 10 ----
    total_tests += 1
    try:
        problem = {'dimensions': 2, 'bounds': [(0,1),(0,1)], 'fitness_function': sphere}
        de = DifferentialEvolution(problem, {'population_size': 5, 'max_iterations': 10})
        de.initialize()
        print("[Test 2] ❌ FAIL: Did not raise error for small population")
    except ValueError as e:
        print(f"[Test 2] ✓ PASS: {e}")
        tests_passed += 1

    # ---- Test 3: F out of bounds (>2) ----
    total_tests += 1
    try:
        problem = {'dimensions': 2, 'bounds': [(0,1),(0,1)], 'fitness_function': sphere}
        de = DifferentialEvolution(problem, {'population_size': 20, 'max_iterations': 10, 'F': 2.5})
        de.initialize()
        print("[Test 3] ❌ FAIL: Did not raise error for F>2")
    except ValueError as e:
        print(f"[Test 3] ✓ PASS: {e}")
        tests_passed += 1

    # ---- Test 4: CR out of bounds (<0) ----
    total_tests += 1
    try:
        problem = {'dimensions': 2, 'bounds': [(0,1),(0,1)], 'fitness_function': sphere}
        de = DifferentialEvolution(problem, {'population_size': 20, 'max_iterations': 10, 'CR': -0.1})
        de.initialize()
        print("[Test 4] ❌ FAIL: Did not raise error for CR<0")
    except ValueError as e:
        print(f"[Test 4] ✓ PASS: {e}")
        tests_passed += 1

    # ---- Test 5: Degenerate initialization (all population same) ----
    # Only one try/except per test
    total_tests += 1  # Only increment once

    try:
        # Initialize DE for degenerate population
        problem = {'dimensions': 3, 'bounds': [(-1,1)]*3, 'fitness_function': sphere}
        de = DifferentialEvolution(problem, {'population_size': 20, 'max_iterations': 5})
        de.initialize()
        
        # Force all individuals to the same point
        de.population[:] = 0.5
        de.fitness_values = np.array([de._evaluate(ind) for ind in de.population])
        
        print(f"[Test 5] ✓ PASS: Initialized degenerate population")
        print(f"  Sample fitness: {de.fitness_values[0]:.6f}")
        tests_passed += 1

    except Exception as e:
        print(f"[Test 5] ❌ FAIL: {e}")




    # ---- Test 6: Very tight bounds ----
    total_tests += 1
    try:
        problem = {'dimensions': 2, 'bounds': [(0.499,0.501),(0.999,1.001)], 'fitness_function': sphere}
        de = DifferentialEvolution(problem, {'population_size': 20, 'max_iterations': 5})
        de.initialize()  # Use public method
        within_bounds = np.all((de.population >= np.array([0.499,0.999])) & (de.population <= np.array([0.501,1.001])))
        print(f"[Test 6] {'✓ PASS' if within_bounds else '❌ FAIL'}: All individuals within tight bounds")
        if within_bounds:
            print(f"  Sample individual: {de.population[0]}")
            tests_passed += 1
    except Exception as e:
        print(f"[Test 6] ❌ FAIL: {e}")

    # ---- Test 7: Optimization run on negative sphere (maximize) ----
    total_tests += 1
    try:
        problem = {'dimensions': 3, 'bounds': [(-5,5)]*3, 'fitness_function': negative_sphere, 'objective':'maximize'}
        de = DifferentialEvolution(problem, {'population_size': 20, 'max_iterations': 10})
        de.initialize()
        de.optimize()
        print(f"[Test 7] ✓ PASS: Optimization completed")
        print(f"  Best fitness: {de.best_fitness:.6f}")
        print(f"  Best solution: {de.best_solution}")
        print(f"  Convergence length: {len(de.convergence_curve)}")
        tests_passed += 1
    except Exception as e:
        print(f"[Test 7] ❌ FAIL: {e}")

    # ---- Final Summary ----
    print("\n" + "="*60)
    print(f"Edge Case Tests Passed: {tests_passed}/{total_tests}")
    print("="*60)

if __name__ == "__main__":
    run_edge_case_tests()
