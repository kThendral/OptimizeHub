"""
Edge case and validation tests for Particle Swarm Optimization.
Tests input validation, boundary handling, and parameter sensitivity.
"""

import numpy as np
import sys
from pathlib import Path

# Add backend to path for imports
backend_path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_path))

from app.algorithms.particle_swarm import ParticleSwarmOptimization


def sphere_function(x):
    """Simple sphere function for testing."""
    return np.sum(x ** 2)


def test_edge_cases():
    """Test edge cases and validation."""
    print("\n" + "="*70)
    print("PSO EDGE CASE TESTS")
    print("="*70)

    passed = 0
    failed = 0

    # Test 1: Missing required fields
    print("\n[Test 1] Missing 'dimensions' field")
    try:
        problem = {
            'bounds': [(0, 1)],
            'fitness_function': sphere_function
        }
        pso = ParticleSwarmOptimization(problem, {})
        print("  ✗ FAIL: Should have raised ValueError")
        failed += 1
    except ValueError as e:
        print(f"  ✓ PASS: Caught expected error - {e}")
        passed += 1

    # Test 2: Invalid dimensions (zero)
    print("\n[Test 2] Invalid dimensions (0)")
    try:
        problem = {
            'dimensions': 0,
            'bounds': [],
            'fitness_function': sphere_function
        }
        pso = ParticleSwarmOptimization(problem, {})
        print("  ✗ FAIL: Should have raised ValueError")
        failed += 1
    except ValueError as e:
        print(f"  ✓ PASS: Caught expected error - {e}")
        passed += 1

    # Test 3: Bounds length mismatch
    print("\n[Test 3] Bounds length doesn't match dimensions")
    try:
        problem = {
            'dimensions': 5,
            'bounds': [(0, 1), (0, 1)],  # Only 2 bounds for 5 dimensions
            'fitness_function': sphere_function
        }
        pso = ParticleSwarmOptimization(problem, {})
        print("  ✗ FAIL: Should have raised ValueError")
        failed += 1
    except ValueError as e:
        print(f"  ✓ PASS: Caught expected error - {e}")
        passed += 1

    # Test 4: Invalid bounds (lower >= upper)
    print("\n[Test 4] Invalid bounds (lower >= upper)")
    try:
        problem = {
            'dimensions': 2,
            'bounds': [(0, 1), (5, 2)],  # Second bound is invalid
            'fitness_function': sphere_function
        }
        pso = ParticleSwarmOptimization(problem, {})
        print("  ✗ FAIL: Should have raised ValueError")
        failed += 1
    except ValueError as e:
        print(f"  ✓ PASS: Caught expected error - {e}")
        passed += 1

    # Test 5: Non-callable fitness function
    print("\n[Test 5] Non-callable fitness function")
    try:
        problem = {
            'dimensions': 2,
            'bounds': [(0, 1), (0, 1)],
            'fitness_function': "not a function"
        }
        pso = ParticleSwarmOptimization(problem, {})
        print("  ✗ FAIL: Should have raised ValueError")
        failed += 1
    except ValueError as e:
        print(f"  ✓ PASS: Caught expected error - {e}")
        passed += 1

    # Test 6: Invalid objective
    print("\n[Test 6] Invalid objective")
    try:
        problem = {
            'dimensions': 2,
            'bounds': [(0, 1), (0, 1)],
            'fitness_function': sphere_function,
            'objective': 'invalid'
        }
        pso = ParticleSwarmOptimization(problem, {})
        print("  ✗ FAIL: Should have raised ValueError")
        failed += 1
    except ValueError as e:
        print(f"  ✓ PASS: Caught expected error - {e}")
        passed += 1

    # Test 7: Invalid swarm size (< 10)
    print("\n[Test 7] Invalid swarm size (< 10)")
    try:
        problem = {
            'dimensions': 2,
            'bounds': [(0, 1), (0, 1)],
            'fitness_function': sphere_function
        }
        pso = ParticleSwarmOptimization(problem, {'swarm_size': 5})
        print("  ✗ FAIL: Should have raised ValueError")
        failed += 1
    except ValueError as e:
        print(f"  ✓ PASS: Caught expected error - {e}")
        passed += 1

    # Test 8: Zero swarm size (should raise error)
    print("\n[Test 8] Zero swarm size (raises error)")
    try:
        problem = {
            'dimensions': 2,
            'bounds': [(0, 1), (0, 1)],
            'fitness_function': sphere_function
        }
        pso = ParticleSwarmOptimization(problem, {'swarm_size': 0})
        print("  ✗ FAIL: Should have raised ValueError")
        failed += 1
    except ValueError as e:
        print(f"  ✓ PASS: Caught expected error - {e}")
        passed += 1

    # Test 9: Negative swarm size (should raise error)
    print("\n[Test 9] Negative swarm size (raises error)")
    try:
        problem = {
            'dimensions': 2,
            'bounds': [(0, 1), (0, 1)],
            'fitness_function': sphere_function
        }
        pso = ParticleSwarmOptimization(problem, {'swarm_size': -10})
        print("  ✗ FAIL: Should have raised ValueError")
        failed += 1
    except ValueError as e:
        print(f"  ✓ PASS: Caught expected error - {e}")
        passed += 1

    # Test 10: Excessive iterations (should raise error with helpful message)
    print("\n[Test 10] Excessive iterations (raises error)")
    try:
        problem = {
            'dimensions': 2,
            'bounds': [(0, 1), (0, 1)],
            'fitness_function': sphere_function
        }
        pso = ParticleSwarmOptimization(problem, {'max_iterations': 500})
        print("  ✗ FAIL: Should have raised ValueError")
        failed += 1
    except ValueError as e:
        if "platform constraint" in str(e):
            print(f"  ✓ PASS: Caught expected error with helpful message - {e}")
            passed += 1
        else:
            print(f"  ✗ FAIL: Error message should mention platform constraint")
            failed += 1

    # Test 11: Both c1 and c2 zero (invalid - no movement)
    print("\n[Test 11] Both c1=0 and c2=0 (invalid)")
    try:
        problem = {
            'dimensions': 2,
            'bounds': [(0, 1), (0, 1)],
            'fitness_function': sphere_function
        }
        pso = ParticleSwarmOptimization(problem, {'c1': 0, 'c2': 0})
        print("  ✗ FAIL: Should have raised ValueError")
        failed += 1
    except ValueError as e:
        print(f"  ✓ PASS: Caught expected error - {e}")
        passed += 1

    # Test 12: Negative inertia weight (allowed for research)
    print("\n[Test 12] Negative inertia weight (allowed for research)")
    try:
        problem = {
            'dimensions': 2,
            'bounds': [(0, 1), (0, 1)],
            'fitness_function': sphere_function
        }
        pso = ParticleSwarmOptimization(problem, {'swarm_size': 10, 'w': -0.5})
        print(f"  ✓ PASS: Negative w allowed (research flexibility)")
        passed += 1
    except Exception as e:
        print(f"  ✗ FAIL: Unexpected error - {e}")
        failed += 1

    # Test 13: Social-only PSO (c1=0, c2>0)
    print("\n[Test 13] Social-only PSO (c1=0, c2>0)")
    try:
        problem = {
            'dimensions': 2,
            'bounds': [(0, 1), (0, 1)],
            'fitness_function': sphere_function
        }
        pso = ParticleSwarmOptimization(problem, {'swarm_size': 10, 'c1': 0, 'c2': 2.0})
        print(f"  ✓ PASS: Social-only variant allowed")
        passed += 1
    except Exception as e:
        print(f"  ✗ FAIL: Unexpected error - {e}")
        failed += 1

    # Test 14: Cognition-only PSO (c1>0, c2=0)
    print("\n[Test 14] Cognition-only PSO (c1>0, c2=0)")
    try:
        problem = {
            'dimensions': 2,
            'bounds': [(0, 1), (0, 1)],
            'fitness_function': sphere_function
        }
        pso = ParticleSwarmOptimization(problem, {'swarm_size': 10, 'c1': 2.0, 'c2': 0})
        print(f"  ✓ PASS: Cognition-only variant allowed")
        passed += 1
    except Exception as e:
        print(f"  ✗ FAIL: Unexpected error - {e}")
        failed += 1

    print("\n" + "="*70)
    print(f"Edge Case Tests: {passed}/{passed + failed} passed")
    print("="*70)

    return passed, failed


def test_parameter_sensitivity():
    """Test PSO with different parameter configurations."""
    print("\n" + "="*70)
    print("PSO PARAMETER SENSITIVITY TESTS")
    print("="*70)

    base_problem = {
        'dimensions': 5,
        'bounds': [(-10, 10) for _ in range(5)],
        'objective': 'minimize',
        'fitness_function': sphere_function
    }

    configs = [
        {'name': 'Minimum swarm (10 particles)', 'params': {'swarm_size': 10, 'max_iterations': 20}},
        {'name': 'Small swarm (15 particles)', 'params': {'swarm_size': 15, 'max_iterations': 20}},
        {'name': 'Large swarm (100 particles)', 'params': {'swarm_size': 100, 'max_iterations': 10}},
        {'name': 'Few iterations (5)', 'params': {'swarm_size': 20, 'max_iterations': 5}},
        {'name': 'Maximum iterations (100)', 'params': {'swarm_size': 20, 'max_iterations': 100}},
        {'name': 'High inertia (w=0.95)', 'params': {'swarm_size': 20, 'max_iterations': 20, 'w': 0.95}},
        {'name': 'Low inertia (w=0.2)', 'params': {'swarm_size': 20, 'max_iterations': 20, 'w': 0.2}},
        {'name': 'Negative inertia (w=-0.3)', 'params': {'swarm_size': 20, 'max_iterations': 20, 'w': -0.3}},
        {'name': 'High cognitive (c1=3)', 'params': {'swarm_size': 20, 'max_iterations': 20, 'c1': 3.0}},
        {'name': 'High social (c2=3)', 'params': {'swarm_size': 20, 'max_iterations': 20, 'c2': 3.0}},
        {'name': 'Social-only (c1=0)', 'params': {'swarm_size': 20, 'max_iterations': 20, 'c1': 0, 'c2': 2.0}},
        {'name': 'Cognition-only (c2=0)', 'params': {'swarm_size': 20, 'max_iterations': 20, 'c1': 2.0, 'c2': 0}},
    ]

    passed = 0
    failed = 0

    for config in configs:
        print(f"\n[Test] {config['name']}")
        try:
            pso = ParticleSwarmOptimization(base_problem, config['params'])
            pso.initialize()
            pso.optimize()
            results = pso.get_results()

            final_fitness = results['convergence_curve'][-1]
            print(f"  ✓ PASS: Completed successfully")
            print(f"    Final fitness: {final_fitness:.6f}")
            print(f"    Iterations: {len(results['convergence_curve']) - 1}")
            passed += 1
        except Exception as e:
            print(f"  ✗ FAIL: {e}")
            failed += 1

    print("\n" + "="*70)
    print(f"Parameter Sensitivity Tests: {passed}/{passed + failed} passed")
    print("="*70)

    return passed, failed


def test_boundary_handling():
    """Test PSO with tight and extreme boundary conditions."""
    print("\n" + "="*70)
    print("PSO BOUNDARY HANDLING TESTS")
    print("="*70)

    passed = 0
    failed = 0

    # Test 1: Very tight bounds
    print("\n[Test 1] Very tight bounds (0.01 range)")
    try:
        problem = {
            'dimensions': 3,
            'bounds': [(0.0, 0.01), (-0.005, 0.005), (0.99, 1.0)],
            'objective': 'minimize',
            'fitness_function': sphere_function,
            'params': {'swarm_size': 20, 'max_iterations': 30}
        }
        pso = ParticleSwarmOptimization(problem, problem['params'])
        pso.initialize()
        pso.optimize()

        # Check all particles stayed within bounds
        for i in range(pso.swarm_size):
            for d in range(pso.dimensions):
                lower, upper = pso.bounds[d]
                if not (lower <= pso.positions[i, d] <= upper):
                    raise ValueError(f"Particle {i} violated bounds at dimension {d}")

        print("  ✓ PASS: All particles stayed within tight bounds")
        passed += 1
    except Exception as e:
        print(f"  ✗ FAIL: {e}")
        failed += 1

    # Test 2: Single point bound (lower == upper after rounding)
    print("\n[Test 2] Near-zero width bounds")
    try:
        problem = {
            'dimensions': 2,
            'bounds': [(0.0, 0.000001), (0.0, 0.000001)],
            'objective': 'minimize',
            'fitness_function': sphere_function,
            'params': {'swarm_size': 10, 'max_iterations': 10}
        }
        pso = ParticleSwarmOptimization(problem, problem['params'])
        pso.initialize()
        pso.optimize()
        print("  ✓ PASS: Handled near-zero width bounds")
        passed += 1
    except Exception as e:
        print(f"  ✗ FAIL: {e}")
        failed += 1

    # Test 3: Asymmetric bounds
    print("\n[Test 3] Asymmetric bounds")
    try:
        problem = {
            'dimensions': 4,
            'bounds': [(-1000, 1), (-1, 1000), (0, 100), (-50, -40)],
            'objective': 'minimize',
            'fitness_function': sphere_function,
            'params': {'swarm_size': 25, 'max_iterations': 25}
        }
        pso = ParticleSwarmOptimization(problem, problem['params'])
        pso.initialize()
        pso.optimize()
        results = pso.get_results()
        print(f"  ✓ PASS: Handled asymmetric bounds")
        print(f"    Final fitness: {results['convergence_curve'][-1]:.6f}")
        passed += 1
    except Exception as e:
        print(f"  ✗ FAIL: {e}")
        failed += 1

    # Test 4: Large bounds
    print("\n[Test 4] Very large bounds")
    try:
        problem = {
            'dimensions': 3,
            'bounds': [(-1e6, 1e6), (-1e6, 1e6), (-1e6, 1e6)],
            'objective': 'minimize',
            'fitness_function': sphere_function,
            'params': {'swarm_size': 30, 'max_iterations': 20}
        }
        pso = ParticleSwarmOptimization(problem, problem['params'])
        pso.initialize()
        pso.optimize()
        results = pso.get_results()
        print(f"  ✓ PASS: Handled large bounds")
        print(f"    Final fitness: {results['convergence_curve'][-1]:.2e}")
        passed += 1
    except Exception as e:
        print(f"  ✗ FAIL: {e}")
        failed += 1

    print("\n" + "="*70)
    print(f"Boundary Handling Tests: {passed}/{passed + failed} passed")
    print("="*70)

    return passed, failed


def main():
    """Run all edge case and validation tests."""
    print("\n" + "="*70)
    print("PSO COMPREHENSIVE EDGE CASE AND VALIDATION TEST SUITE")
    print("="*70)

    total_passed = 0
    total_failed = 0

    # Run test suites
    p, f = test_edge_cases()
    total_passed += p
    total_failed += f

    p, f = test_parameter_sensitivity()
    total_passed += p
    total_failed += f

    p, f = test_boundary_handling()
    total_passed += p
    total_failed += f

    # Final summary
    print("\n" + "="*70)
    print("FINAL SUMMARY")
    print("="*70)
    print(f"Total Tests: {total_passed + total_failed}")
    print(f"Passed: {total_passed}")
    print(f"Failed: {total_failed}")
    print(f"Success Rate: {100 * total_passed / (total_passed + total_failed):.1f}%")
    print("="*70 + "\n")

    return total_failed == 0


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
