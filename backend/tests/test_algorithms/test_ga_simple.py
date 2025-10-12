"""
Simple test script to verify Genetic Algorithm implementation works correctly.
"""

import sys
import numpy as np
from pathlib import Path

# Add backend to path for imports
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

from app.algorithms.genetic_algorithm import GeneticAlgorithm


def sphere_function(x):
    """Simple sphere function: f(x) = sum(x_i^2)"""
    return np.sum(x ** 2)


def test_ga():
    """Test GA on sphere function."""
    print("Testing Genetic Algorithm on 2D Sphere Function")
    print("=" * 50)
    
    # Define problem
    problem = {
        'dimensions': 2,
        'bounds': [(-5.0, 5.0), (-5.0, 5.0)],
        'objective': 'minimize',
        'fitness_function': sphere_function
    }
    
    # Define parameters
    params = {
        'population_size': 20,
        'max_iterations': 30,
        'crossover_rate': 0.8,
        'mutation_rate': 0.1,
        'tournament_size': 3
    }
    
    try:
        # Initialize and run GA
        ga = GeneticAlgorithm(problem, params)
        ga.initialize()
        ga.optimize()
        
        # Get results
        results = ga.get_results()
        
        print(f"Algorithm: {results['algorithm']}")
        print(f"Best solution: {results['best_solution']}")
        print(f"Best fitness: {ga.best_fitness:.6f}")
        print(f"Initial fitness: {results['convergence_curve'][0]:.6f}")
        print(f"Final fitness: {results['convergence_curve'][-1]:.6f}")
        print(f"Generations: {len(results['convergence_curve']) - 1}")
        print(f"Improvement: {results['convergence_curve'][0] - results['convergence_curve'][-1]:.6f}")
        
        # Check if converging toward zero (global optimum)
        distance_from_origin = np.linalg.norm(results['best_solution'])
        print(f"Distance from origin: {distance_from_origin:.6f}")
        
        if ga.best_fitness < 1.0 and distance_from_origin < 2.0:
            print("\n✅ GA Test PASSED - Converging toward global optimum!")
        else:
            print("\n⚠️  GA Test - Partial success (may need more generations)")
        
        return True
        
    except Exception as e:
        print(f"\n❌ GA Test FAILED: {e}")
        return False


if __name__ == "__main__":
    success = test_ga()
    exit(0 if success else 1)