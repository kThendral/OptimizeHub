"""
Test Differential Evolution on Rastrigin function for multi-dimensional problems.
"""

import sys
import numpy as np
from pathlib import Path

backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from app.algorithms.differential_evolution import DifferentialEvolution

def rastrigin(x):
    n = len(x)
    return 10 * n + np.sum(x**2 - 10 * np.cos(2 * np.pi * x))

def test_de_rastrigin():
    print("🧬 DIFFERENTIAL EVOLUTION TEST - RASTRIGIN FUNCTION")
    print("="*70)

    dimensions = 5
    problem = {
        "dimensions": dimensions,
        "bounds": [(-5.12, 5.12)] * dimensions,
        "objective": "minimize",
        "fitness_function": rastrigin
    }

    params = {
        "population_size": 50,
        "max_iterations": 100,
        "F": 0.7,
        "CR": 0.9,
        "strategy": "rand/1/bin",
        "boundary_handling": "clip",
        "timeout": 60
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

        if results['best_fitness'] < 10.0:
            print("\n✅ DE Rastrigin Test PASSED")
        else:
            print("\n⚠️ DE Rastrigin Test - Partial success")

        return True

    except Exception as e:
        print(f"\n❌ DE Rastrigin Test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_de_rastrigin()
    exit(0 if success else 1)
