# Quick local runner that imports GeneticAlgorithm and runs it directly.
from app.algorithms.genetic_algorithm import GeneticAlgorithm
from app.problem_functions import sphere

def main():
    problem = {
        "dimensions": 2,
        "bounds": [(-5.0, 5.0), (-5.0, 5.0)],
        "fitness_function": sphere,
        "objective": "minimize",
    }
    params = {
        "population_size": 30,
        "max_iterations": 20,
    }

    ga = GeneticAlgorithm(problem, params)
    ga.initialize()
    ga.optimize()
    print("Best solution:", ga.best_solution)
    print("Best fitness:", ga.best_fitness)
    print("Convergence curve:", ga.convergence_curve)

if __name__ == "__main__":
    main()