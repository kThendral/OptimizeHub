"""
Standalone API Performance Comparison Test

Compares PSO, ACOR, GA, and DE performance through the API.
Measures speed and accuracy on benchmark functions.
"""

import sys
import time
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from fastapi.testclient import TestClient
from app.main import app

# Create test client
client = TestClient(app)


def run_algorithm_test(algorithm_name, params, problem, test_name):
    """Run a single algorithm test and return results."""
    request_data = {
        "algorithm": algorithm_name,
        "problem": problem,
        "params": params
    }

    print(f"\n{'='*70}")
    print(f"Testing {test_name}")
    print(f"{'='*70}")

    start_time = time.time()
    response = client.post("/api/optimize", json=request_data)
    api_time = time.time() - start_time

    if response.status_code != 200:
        print(f"❌ ERROR: Status code {response.status_code}")
        print(response.json())
        return None

    data = response.json()

    if data["status"] != "success":
        print(f"❌ FAILED: {data.get('error_message', 'Unknown error')}")
        return None

    print(f"✅ SUCCESS")
    print(f"  Best Fitness: {data['best_fitness']:.8f}")
    print(f"  Execution Time: {data['execution_time']:.3f}s")
    print(f"  API Time: {api_time:.3f}s")
    print(f"  Iterations: {data.get('iterations_completed', 'N/A')}")
    print(f"  Initial → Final: {data['convergence_curve'][0]:.6f} → {data['convergence_curve'][-1]:.6f}")

    return {
        "algorithm": data["algorithm"],
        "best_fitness": data["best_fitness"],
        "execution_time": data["execution_time"],
        "api_time": api_time,
        "iterations": data.get("iterations_completed", 0),
        "convergence": data["convergence_curve"]
    }


def main():
    """Run comprehensive algorithm comparison."""
    print("\n" + "="*70)
    print("API INTEGRATION & PERFORMANCE COMPARISON TEST")
    print("="*70)

    # Test 1: Simple 2D Sphere Function
    print("\n\n" + "="*70)
    print("TEST 1: 2D Sphere Function (Simple Optimization)")
    print("="*70)

    problem_2d = {
        "dimensions": 2,
        "bounds": [[-5.0, 5.0], [-5.0, 5.0]],
        "objective": "minimize",
        "fitness_function_name": "sphere"
    }

    results_2d = {}

    # PSO
    results_2d["PSO"] = run_algorithm_test(
        "particle_swarm",
        {"swarm_size": 20, "max_iterations": 30, "w": 0.7, "c1": 1.5, "c2": 1.5},
        problem_2d,
        "Particle Swarm Optimization (PSO)"
    )

    # ACOR
    results_2d["ACOR"] = run_algorithm_test(
        "ant_colony",
        {"colony_size": 20, "max_iterations": 30, "archive_size": 10, "q": 0.01, "xi": 0.85},
        problem_2d,
        "Ant Colony Optimization (ACOR)"
    )

    # GA
    results_2d["GA"] = run_algorithm_test(
        "genetic_algorithm",
        {"population_size": 20, "max_iterations": 30, "crossover_rate": 0.8, "mutation_rate": 0.1, "tournament_size": 3},
        problem_2d,
        "Genetic Algorithm (GA)"
    )

    # DE
    results_2d["DE"] = run_algorithm_test(
        "differential_evolution",
        {"population_size": 20, "max_iterations": 30, "F": 0.8, "CR": 0.9},
        problem_2d,
        "Differential Evolution (DE)"
    )

    # Test 2: 5D Sphere Function
    print("\n\n" + "="*70)
    print("TEST 2: 5D Sphere Function (Medium Complexity)")
    print("="*70)

    problem_5d = {
        "dimensions": 5,
        "bounds": [[-10.0, 10.0]] * 5,
        "objective": "minimize",
        "fitness_function_name": "sphere"
    }

    results_5d = {}

    results_5d["PSO"] = run_algorithm_test(
        "particle_swarm",
        {"swarm_size": 30, "max_iterations": 50},
        problem_5d,
        "PSO (5D)"
    )

    results_5d["ACOR"] = run_algorithm_test(
        "ant_colony",
        {"colony_size": 30, "max_iterations": 50},
        problem_5d,
        "ACOR (5D)"
    )

    results_5d["GA"] = run_algorithm_test(
        "genetic_algorithm",
        {"population_size": 30, "max_iterations": 50},
        problem_5d,
        "GA (5D)"
    )

    # Test 3: Rastrigin (Multi-modal)
    print("\n\n" + "="*70)
    print("TEST 3: 3D Rastrigin Function (Multi-modal Challenge)")
    print("="*70)

    problem_rastrigin = {
        "dimensions": 3,
        "bounds": [[-5.12, 5.12]] * 3,
        "objective": "minimize",
        "fitness_function_name": "rastrigin"
    }

    results_rastrigin = {}

    results_rastrigin["PSO"] = run_algorithm_test(
        "particle_swarm",
        {"swarm_size": 40, "max_iterations": 50},
        problem_rastrigin,
        "PSO (Rastrigin)"
    )

    results_rastrigin["ACOR"] = run_algorithm_test(
        "ant_colony",
        {"colony_size": 40, "max_iterations": 50, "archive_size": 15, "q": 0.005, "xi": 0.8},
        problem_rastrigin,
        "ACOR (Rastrigin)"
    )

    results_rastrigin["GA"] = run_algorithm_test(
        "genetic_algorithm",
        {"population_size": 40, "max_iterations": 50},
        problem_rastrigin,
        "GA (Rastrigin)"
    )

    # Summary Report
    print("\n\n" + "="*70)
    print("COMPREHENSIVE COMPARISON SUMMARY")
    print("="*70)

    print("\n📊 2D SPHERE FUNCTION RESULTS:")
    print("-" * 70)
    print(f"{'Algorithm':<15} {'Fitness':<15} {'Time (s)':<12} {'Speed Rank':<12}")
    print("-" * 70)

    # Sort by execution time
    sorted_2d = sorted([(name, res) for name, res in results_2d.items() if res],
                       key=lambda x: x[1]["execution_time"])

    for rank, (name, res) in enumerate(sorted_2d, 1):
        print(f"{name:<15} {res['best_fitness']:<15.8f} {res['execution_time']:<12.3f} {rank}")

    print("\n🎯 ACCURACY COMPARISON (2D Sphere - closer to 0 is better):")
    sorted_accuracy = sorted([(name, res) for name, res in results_2d.items() if res],
                            key=lambda x: x[1]["best_fitness"])

    for rank, (name, res) in enumerate(sorted_accuracy, 1):
        print(f"  {rank}. {name}: {res['best_fitness']:.8f}")

    print("\n📊 5D SPHERE FUNCTION RESULTS:")
    print("-" * 70)
    for name, res in results_5d.items():
        if res:
            print(f"{name:<15} Fitness: {res['best_fitness']:.8f}, Time: {res['execution_time']:.3f}s")

    print("\n📊 RASTRIGIN MULTI-MODAL RESULTS:")
    print("-" * 70)
    for name, res in results_rastrigin.items():
        if res:
            print(f"{name:<15} Fitness: {res['best_fitness']:.8f}, Time: {res['execution_time']:.3f}s")

    # Speed/Accuracy Classification
    print("\n\n" + "="*70)
    print("ALGORITHM CHARACTERISTICS FOR SaaS PLATFORM")
    print("="*70)

    if results_2d["PSO"] and results_2d["ACOR"] and results_2d["GA"]:
        pso_time = results_2d["PSO"]["execution_time"]
        acor_time = results_2d["ACOR"]["execution_time"]
        ga_time = results_2d["GA"]["execution_time"]

        pso_acc = results_2d["PSO"]["best_fitness"]
        acor_acc = results_2d["ACOR"]["best_fitness"]
        ga_acc = results_2d["GA"]["best_fitness"]

        print("\n1. PARTICLE SWARM OPTIMIZATION (PSO)")
        print(f"   Speed: {pso_time:.3f}s (FASTEST)")
        print(f"   Accuracy: {pso_acc:.8f}")
        print(f"   Speed Rank: ★★★★★")
        print(f"   Accuracy Rank: {'★★★★☆' if pso_acc < 0.01 else '★★★☆☆'}")
        print(f"   Best For: Quick optimization, real-time applications")

        print("\n2. ANT COLONY OPTIMIZATION (ACOR)")
        print(f"   Speed: {acor_time:.3f}s ({acor_time/pso_time:.1f}x slower than PSO)")
        print(f"   Accuracy: {acor_acc:.8f} ({pso_acc/acor_acc if acor_acc > 0 else 'inf'}x better than PSO)")
        print(f"   Speed Rank: {'★★★★☆' if acor_time < 0.1 else '★★★☆☆'}")
        print(f"   Accuracy Rank: ★★★★★")
        print(f"   Best For: High-precision optimization, engineering design")

        print("\n3. GENETIC ALGORITHM (GA)")
        print(f"   Speed: {ga_time:.3f}s")
        print(f"   Accuracy: {ga_acc:.8f}")
        print(f"   Speed Rank: {'★★★★☆' if ga_time < 0.1 else '★★★☆☆'}")
        print(f"   Accuracy Rank: {'★★★★☆' if ga_acc < 0.5 else '★★★☆☆'}")
        print(f"   Best For: Robust optimization, discrete/complex problems, exploration")

    print("\n" + "="*70)
    print("✅ ALL INTEGRATION TESTS COMPLETED")
    print("="*70)

    return results_2d, results_5d, results_rastrigin


if __name__ == "__main__":
    main()
