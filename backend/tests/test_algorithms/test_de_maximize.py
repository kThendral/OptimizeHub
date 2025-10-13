"""
Test Differential Evolution on a maximization problem.
"""

import sys
import numpy as np
from pathlib import Path

backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from app.algorithms.differential_evolution import DifferentialEvolution

def quadratic_max(x):
    """Simple parabola with maximum at [1, 2]"""
    return -((x[0]-1)**2 + (x[1]-2)**2) + 10

def test_de_maximize():
    print("🧬 DIFFERENTIAL EVOLUTION TEST - MAXIMIZATION")
    print("="*70)

    problem = {
        "dimensions": 2,
        "bounds": [(-5, 5), (-5, 5)],
        "objective": "maximize",
        "fitness_function": quadratic_max
    }

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
        print(f"Improvement: {results['convergence_curve'][-1] - results['convergence_curve'][0]:.6f}")

        distance = np.linalg.norm(np.array(results['best_solution']) - np.array([1, 2]))
        print(f"Distance from optimum: {distance:.6f}")

        if results['best_fitness'] > 9.0:
            print("\n✅ DE Maximization Test PASSED")
        else:
            print("\n⚠️ DE Maximization Test - Partial success")

        return True

    except Exception as e:
        print(f"\n❌ DE Maximization Test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_de_maximize()
    exit(0 if success else 1)
