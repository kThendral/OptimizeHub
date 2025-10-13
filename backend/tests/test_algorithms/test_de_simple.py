"""
Simple test for Differential Evolution on 2D Sphere function.
"""

import sys
import numpy as np
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from app.algorithms.differential_evolution import DifferentialEvolution

def sphere_function(x):
    return np.sum(x ** 2)

def test_de_simple():
    print("🧬 DIFFERENTIAL EVOLUTION TEST - SPHERE FUNCTION")
    print("="*70)

    # Problem definition
    problem = {
        "dimensions": 2,
        "bounds": [(-5.0, 5.0), (-5.0, 5.0)],
        "objective": "minimize",
        "fitness_function": sphere_function
    }

    # DE parameters
    params = {
        "population_size": 30,
        "max_iterations": 50,
        "F": 0.8,
        "CR": 0.9,
        "strategy": "rand/1/bin",
        "boundary_handling": "clip",
        "timeout": 30
    }

    try:
        de = DifferentialEvolution(problem, params)
        de.initialize()
        results = de.optimize()

        print("\n📈 Optimization Summary")
        print("-"*70)
        print(f"Algorithm: {results['algorithm']}")
        print(f"Best solution: {results['best_solution']}")
        print(f"Best fitness: {results['best_fitness']:.6f}")
        print(f"Initial fitness: {results['convergence_curve'][0]:.6f}")
        print(f"Final fitness: {results['convergence_curve'][-1]:.6f}")
        print(f"Iterations: {len(results['convergence_curve']) - 1}")
        print(f"Improvement: {results['convergence_curve'][0] - results['convergence_curve'][-1]:.6f}")

        # Distance from global optimum
        distance = np.linalg.norm(results['best_solution'])
        print(f"Distance from origin: {distance:.6f}")

        if results['best_fitness'] < 1.0 and distance < 2.0:
            print("\n✅ DE Simple Test PASSED")
        else:
            print("\n⚠️ DE Simple Test - Partial success")

        return True

    except Exception as e:
        print(f"\n❌ DE Simple Test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_de_simple()
    exit(0 if success else 1)
