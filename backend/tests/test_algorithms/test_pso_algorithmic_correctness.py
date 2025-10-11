"""
Algorithmic correctness tests for PSO under edge conditions.
Tests dimension edge cases, extreme bounds, and degenerate scenarios.
"""

import numpy as np
import sys
from pathlib import Path

# Add backend to path for imports
backend_path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_path))

from app.algorithms.particle_swarm import ParticleSwarmOptimization


# Test Functions
def sphere_function(x):
    """Sphere function: f(x) = sum(x_i^2)"""
    return np.sum(x ** 2)


def rastrigin_function(x):
    """Rastrigin function with many local minima"""
    n = len(x)
    return 10 * n + np.sum(x ** 2 - 10 * np.cos(2 * np.pi * x))


def rosenbrock_function(x):
    """Rosenbrock function - challenging for optimizers"""
    return np.sum(100.0 * (x[1:] - x[:-1]**2)**2 + (1 - x[:-1])**2)


def test_dimension_edge_cases():
    """Test PSO with extreme dimension counts."""
    print("\n" + "="*70)
    print("DIMENSION EDGE CASE TESTS")
    print("="*70)

    passed = 0
    failed = 0

    # Test 1: 1D problem - PSO should still work but degenerates to simpler search
    print("\n[Test 1] 1D optimization problem")
    try:
        problem = {
            'dimensions': 1,
            'bounds': [(-10, 10)],
            'objective': 'minimize',
            'fitness_function': sphere_function,
            'params': {'swarm_size': 20, 'max_iterations': 30}
        }
        pso = ParticleSwarmOptimization(problem, problem['params'])
        pso.initialize()
        pso.optimize()
        results = pso.get_results()

        final_fitness = results['convergence_curve'][-1]
        best_solution = np.array(results['best_solution'])

        # Check convergence
        if final_fitness < 1.0 and abs(best_solution[0]) < 1.0:
            print(f"  ✓ PASS: 1D PSO converged")
            print(f"    Best solution: {best_solution[0]:.6f}")
            print(f"    Final fitness: {final_fitness:.6f}")
            passed += 1
        else:
            print(f"  ✗ FAIL: Poor convergence - fitness: {final_fitness}")
            failed += 1
    except Exception as e:
        print(f"  ✗ FAIL: {e}")
        failed += 1

    # Test 2: Maximum dimensions (50)
    print("\n[Test 2] Maximum dimensions (50D)")
    try:
        problem = {
            'dimensions': 50,
            'bounds': [(-5, 5) for _ in range(50)],
            'objective': 'minimize',
            'fitness_function': sphere_function,
            'params': {'swarm_size': 50, 'max_iterations': 100}
        }
        pso = ParticleSwarmOptimization(problem, problem['params'])
        pso.initialize()
        pso.optimize()
        results = pso.get_results()

        final_fitness = results['convergence_curve'][-1]
        initial_fitness = results['convergence_curve'][0]
        improvement_ratio = initial_fitness / max(final_fitness, 1e-10)

        # In 50D, we expect significant improvement even if not perfect convergence
        if improvement_ratio > 10:  # At least 10x improvement
            print(f"  ✓ PASS: 50D PSO showed significant improvement")
            print(f"    Initial fitness: {initial_fitness:.2e}")
            print(f"    Final fitness: {final_fitness:.2e}")
            print(f"    Improvement ratio: {improvement_ratio:.2f}x")
            passed += 1
        else:
            print(f"  ✗ FAIL: Insufficient improvement - ratio: {improvement_ratio:.2f}x")
            failed += 1
    except Exception as e:
        print(f"  ✗ FAIL: {e}")
        failed += 1

    # Test 3: 2D problem (sanity check for standard case)
    print("\n[Test 3] Standard 2D problem")
    try:
        problem = {
            'dimensions': 2,
            'bounds': [(-10, 10), (-10, 10)],
            'objective': 'minimize',
            'fitness_function': sphere_function,
            'params': {'swarm_size': 20, 'max_iterations': 30}
        }
        pso = ParticleSwarmOptimization(problem, problem['params'])
        pso.initialize()
        pso.optimize()
        results = pso.get_results()

        final_fitness = results['convergence_curve'][-1]
        best_solution = np.array(results['best_solution'])

        if final_fitness < 0.1 and np.linalg.norm(best_solution) < 1.0:
            print(f"  ✓ PASS: 2D PSO converged well")
            print(f"    Final fitness: {final_fitness:.6f}")
            passed += 1
        else:
            print(f"  ✗ FAIL: Poor convergence")
            failed += 1
    except Exception as e:
        print(f"  ✗ FAIL: {e}")
        failed += 1

    # Test 4: 10D Rastrigin (more challenging)
    print("\n[Test 4] 10D Rastrigin function (many local minima)")
    try:
        problem = {
            'dimensions': 10,
            'bounds': [(-5.12, 5.12) for _ in range(10)],
            'objective': 'minimize',
            'fitness_function': rastrigin_function,
            'params': {'swarm_size': 40, 'max_iterations': 100}
        }
        pso = ParticleSwarmOptimization(problem, problem['params'])
        pso.initialize()
        pso.optimize()
        results = pso.get_results()

        initial_fitness = results['convergence_curve'][0]
        final_fitness = results['convergence_curve'][-1]
        improvement = initial_fitness - final_fitness

        # For Rastrigin, just check for improvement (global optimum is hard)
        if improvement > 0 and final_fitness < initial_fitness * 0.5:
            print(f"  ✓ PASS: PSO improved on challenging function")
            print(f"    Initial: {initial_fitness:.2f}, Final: {final_fitness:.2f}")
            print(f"    Improvement: {improvement:.2f}")
            passed += 1
        else:
            print(f"  ✗ FAIL: Insufficient improvement")
            failed += 1
    except Exception as e:
        print(f"  ✗ FAIL: {e}")
        failed += 1

    print("\n" + "="*70)
    print(f"Dimension Edge Case Tests: {passed}/{passed + failed} passed")
    print("="*70)

    return passed, failed


def test_extreme_bounds():
    """Test PSO with extreme and mixed-scale bounds."""
    print("\n" + "="*70)
    print("EXTREME BOUNDS TESTS")
    print("="*70)

    passed = 0
    failed = 0

    # Test 1: Vastly different scales
    print("\n[Test 1] Mixed-scale bounds (1e-6 to 1e6)")
    try:
        problem = {
            'dimensions': 5,
            'bounds': [
                (-1e6, 1e6),      # Very large
                (-0.01, 0.01),    # Very small
                (-100, 100),      # Medium
                (-1e-3, 1e-3),    # Tiny
                (-1000, 1000)     # Large
            ],
            'objective': 'minimize',
            'fitness_function': sphere_function,
            'params': {'swarm_size': 30, 'max_iterations': 50}
        }
        pso = ParticleSwarmOptimization(problem, problem['params'])
        pso.initialize()

        # Check initialization stayed within bounds
        for i in range(pso.swarm_size):
            for d in range(pso.dimensions):
                lower, upper = pso.bounds[d]
                if not (lower <= pso.positions[i, d] <= upper):
                    raise ValueError(f"Initialization violated bounds at particle {i}, dim {d}")

        pso.optimize()
        results = pso.get_results()

        # Check final positions stay within bounds
        final_position = np.array(results['best_solution'])
        for d in range(pso.dimensions):
            lower, upper = pso.bounds[d]
            if not (lower <= final_position[d] <= upper):
                raise ValueError(f"Final solution violated bounds at dim {d}")

        # Check for improvement
        initial_fitness = results['convergence_curve'][0]
        final_fitness = results['convergence_curve'][-1]

        if final_fitness < initial_fitness:
            print(f"  ✓ PASS: Handled mixed scales correctly")
            print(f"    All bounds respected")
            print(f"    Improved from {initial_fitness:.2e} to {final_fitness:.2e}")
            passed += 1
        else:
            print(f"  ✗ FAIL: No improvement observed")
            failed += 1
    except Exception as e:
        print(f"  ✗ FAIL: {e}")
        failed += 1

    # Test 2: All very large bounds
    print("\n[Test 2] All very large bounds (±1e9)")
    try:
        problem = {
            'dimensions': 3,
            'bounds': [(-1e9, 1e9) for _ in range(3)],
            'objective': 'minimize',
            'fitness_function': sphere_function,
            'params': {'swarm_size': 25, 'max_iterations': 40}
        }
        pso = ParticleSwarmOptimization(problem, problem['params'])
        pso.initialize()
        pso.optimize()
        results = pso.get_results()

        # Just check it completes and improves
        if results['convergence_curve'][-1] < results['convergence_curve'][0]:
            print(f"  ✓ PASS: Handled very large bounds")
            print(f"    Final fitness: {results['convergence_curve'][-1]:.2e}")
            passed += 1
        else:
            print(f"  ✗ FAIL: No improvement")
            failed += 1
    except Exception as e:
        print(f"  ✗ FAIL: {e}")
        failed += 1

    # Test 3: All very small bounds
    print("\n[Test 3] All very small bounds (±0.001)")
    try:
        problem = {
            'dimensions': 4,
            'bounds': [(-0.001, 0.001) for _ in range(4)],
            'objective': 'minimize',
            'fitness_function': sphere_function,
            'params': {'swarm_size': 20, 'max_iterations': 30}
        }
        pso = ParticleSwarmOptimization(problem, problem['params'])
        pso.initialize()
        pso.optimize()
        results = pso.get_results()

        final_fitness = results['convergence_curve'][-1]
        # In such tiny bounds, should converge very close to 0
        if final_fitness < 1e-6:
            print(f"  ✓ PASS: Handled very small bounds")
            print(f"    Final fitness: {final_fitness:.2e}")
            passed += 1
        else:
            print(f"  ✗ FAIL: Poor convergence in small bounds")
            failed += 1
    except Exception as e:
        print(f"  ✗ FAIL: {e}")
        failed += 1

    # Test 4: Asymmetric bounds (all positive or all negative)
    print("\n[Test 4] Asymmetric bounds (optimum at boundary)")
    try:
        # Bounds don't contain origin - optimum is at boundary
        problem = {
            'dimensions': 3,
            'bounds': [(10, 20), (5, 15), (8, 12)],
            'objective': 'minimize',
            'fitness_function': sphere_function,
            'params': {'swarm_size': 25, 'max_iterations': 40}
        }
        pso = ParticleSwarmOptimization(problem, problem['params'])
        pso.initialize()
        pso.optimize()
        results = pso.get_results()

        best_solution = np.array(results['best_solution'])
        # Should converge to lower bounds (closest to 0)
        expected = [10, 5, 8]
        distance_to_lower_bounds = np.linalg.norm(best_solution - expected)

        if distance_to_lower_bounds < 2.0:  # Close to lower bounds
            print(f"  ✓ PASS: Converged to boundary as expected")
            print(f"    Best solution: {best_solution}")
            print(f"    Expected: {expected}")
            passed += 1
        else:
            print(f"  ✗ FAIL: Did not converge to optimal boundary")
            print(f"    Best solution: {best_solution}")
            failed += 1
    except Exception as e:
        print(f"  ✗ FAIL: {e}")
        failed += 1

    print("\n" + "="*70)
    print(f"Extreme Bounds Tests: {passed}/{passed + failed} passed")
    print("="*70)

    return passed, failed


def test_degenerate_cases():
    """Test PSO recovery from degenerate initial conditions."""
    print("\n" + "="*70)
    print("DEGENERATE CASE TESTS")
    print("="*70)

    passed = 0
    failed = 0

    # Test 1: All particles start at same position (no initial diversity)
    print("\n[Test 1] Zero initial diversity (all particles at same point)")
    try:
        problem = {
            'dimensions': 3,
            'bounds': [(-10, 10), (-10, 10), (-10, 10)],
            'objective': 'minimize',
            'fitness_function': sphere_function,
            'params': {'swarm_size': 20, 'max_iterations': 50}
        }
        pso = ParticleSwarmOptimization(problem, problem['params'])
        pso.initialize()

        # Force all particles to same position
        same_position = np.array([5.0, 5.0, 5.0])
        pso.positions[:] = same_position
        pso.personal_best_positions[:] = same_position
        pso.personal_best_scores[:] = sphere_function(same_position)
        pso.global_best_position = same_position.copy()
        pso.global_best_score = sphere_function(same_position)
        pso.best_solution = same_position.tolist()
        pso.convergence_curve = [pso.global_best_score]

        # Velocities still have some randomness from initialization
        # Run optimization
        pso.optimize()
        results = pso.get_results()

        final_fitness = results['convergence_curve'][-1]
        initial_fitness = results['convergence_curve'][0]

        # PSO should still improve due to velocity diversity
        if final_fitness < initial_fitness * 0.9:  # At least 10% improvement
            print(f"  ✓ PASS: PSO recovered from zero position diversity")
            print(f"    Initial: {initial_fitness:.6f}, Final: {final_fitness:.6f}")
            passed += 1
        else:
            print(f"  ✗ FAIL: Failed to recover from degenerate start")
            print(f"    Initial: {initial_fitness:.6f}, Final: {final_fitness:.6f}")
            failed += 1
    except Exception as e:
        print(f"  ✗ FAIL: {e}")
        failed += 1

    # Test 2: Particles start at boundary
    print("\n[Test 2] All particles initialized at boundary")
    try:
        problem = {
            'dimensions': 3,
            'bounds': [(-10, 10), (-10, 10), (-10, 10)],
            'objective': 'minimize',
            'fitness_function': sphere_function,
            'params': {'swarm_size': 20, 'max_iterations': 40}
        }
        pso = ParticleSwarmOptimization(problem, problem['params'])
        pso.initialize()

        # Force all particles to upper boundary
        boundary_position = np.array([10.0, 10.0, 10.0])
        pso.positions[:] = boundary_position
        pso.personal_best_positions[:] = boundary_position
        pso.personal_best_scores[:] = sphere_function(boundary_position)
        pso.global_best_position = boundary_position.copy()
        pso.global_best_score = sphere_function(boundary_position)
        pso.best_solution = boundary_position.tolist()
        pso.convergence_curve = [pso.global_best_score]

        pso.optimize()
        results = pso.get_results()

        final_fitness = results['convergence_curve'][-1]
        initial_fitness = results['convergence_curve'][0]

        # Should move away from boundary toward optimum
        if final_fitness < initial_fitness * 0.5:
            print(f"  ✓ PASS: PSO moved from boundary toward optimum")
            print(f"    Initial: {initial_fitness:.6f}, Final: {final_fitness:.6f}")
            passed += 1
        else:
            print(f"  ✗ FAIL: Stuck at boundary")
            failed += 1
    except Exception as e:
        print(f"  ✗ FAIL: {e}")
        failed += 1

    # Test 3: Very poor initial fitness (far from optimum)
    print("\n[Test 3] Very poor initial positions (far from optimum)")
    try:
        problem = {
            'dimensions': 5,
            'bounds': [(-100, 100) for _ in range(5)],
            'objective': 'minimize',
            'fitness_function': sphere_function,
            'params': {'swarm_size': 40, 'max_iterations': 100}  # More resources for hard case
        }
        pso = ParticleSwarmOptimization(problem, problem['params'])
        pso.initialize()

        # Force particles to far corners of search space, but with some variation
        for i in range(pso.swarm_size):
            # Add some randomness so particles aren't all identical
            offset = np.random.uniform(-5, 5, 5)
            pso.positions[i] = np.array([85, -85, 85, -85, 85]) + offset

        # Re-evaluate
        pso.personal_best_positions = pso.positions.copy()
        pso.personal_best_scores = np.array([pso._evaluate(p) for p in pso.positions])
        best_idx = np.argmin(pso.personal_best_scores)
        pso.global_best_position = pso.personal_best_positions[best_idx].copy()
        pso.global_best_score = pso.personal_best_scores[best_idx]
        pso.best_solution = pso.global_best_position.tolist()
        pso.convergence_curve = [pso.global_best_score]

        pso.optimize()
        results = pso.get_results()

        initial_fitness = results['convergence_curve'][0]
        final_fitness = results['convergence_curve'][-1]
        improvement_ratio = initial_fitness / max(final_fitness, 1e-10)

        # Lower expectation - starting very far away is challenging
        # Just need to show meaningful improvement (2x is reasonable)
        if improvement_ratio > 2.0:  # At least 2x improvement from poor start
            print(f"  ✓ PASS: PSO recovered from poor initialization")
            print(f"    Initial: {initial_fitness:.2e}, Final: {final_fitness:.2e}")
            print(f"    Improvement: {improvement_ratio:.2f}x")
            passed += 1
        else:
            print(f"  ✗ FAIL: Poor recovery from bad start")
            print(f"    Initial: {initial_fitness:.2e}, Final: {final_fitness:.2e}")
            print(f"    Improvement: {improvement_ratio:.2f}x (need > 2.0x)")
            failed += 1
    except Exception as e:
        print(f"  ✗ FAIL: {e}")
        failed += 1

    # Test 4: Flat fitness landscape (all same fitness)
    print("\n[Test 4] Flat fitness landscape (constant function)")
    try:
        def constant_function(x):
            return 5.0  # Always returns same value

        problem = {
            'dimensions': 3,
            'bounds': [(-10, 10), (-10, 10), (-10, 10)],
            'objective': 'minimize',
            'fitness_function': constant_function,
            'params': {'swarm_size': 15, 'max_iterations': 20}
        }
        pso = ParticleSwarmOptimization(problem, problem['params'])
        pso.initialize()
        pso.optimize()
        results = pso.get_results()

        # In flat landscape, fitness should remain constant
        initial_fitness = results['convergence_curve'][0]
        final_fitness = results['convergence_curve'][-1]

        if abs(initial_fitness - final_fitness) < 1e-10:
            print(f"  ✓ PASS: PSO handled flat landscape correctly")
            print(f"    Fitness remained constant: {final_fitness:.6f}")
            passed += 1
        else:
            print(f"  ✗ FAIL: Unexpected fitness change in flat landscape")
            failed += 1
    except Exception as e:
        print(f"  ✗ FAIL: {e}")
        failed += 1

    print("\n" + "="*70)
    print(f"Degenerate Case Tests: {passed}/{passed + failed} passed")
    print("="*70)

    return passed, failed


def main():
    """Run all algorithmic correctness tests."""
    print("\n" + "="*70)
    print("PSO ALGORITHMIC CORRECTNESS TEST SUITE")
    print("="*70)

    total_passed = 0
    total_failed = 0

    # Run test suites
    p, f = test_dimension_edge_cases()
    total_passed += p
    total_failed += f

    p, f = test_extreme_bounds()
    total_passed += p
    total_failed += f

    p, f = test_degenerate_cases()
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
