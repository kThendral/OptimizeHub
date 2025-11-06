from app.tasks import run_algorithm
import time

def main():
    problem = {
        "dimensions": 2,
        "bounds": [(-5.0, 5.0), (-5.0, 5.0)],
        "fitness_function": "sphere",  # pass function name, not callable
        "objective": "minimize",
    }

    params = {
        "population_size": 30,
        "max_iterations": 20,
    }

    print("Submitting Genetic Algorithm task to Celery...")
    result = run_algorithm.delay("genetic", problem, params)

    print(f"Task ID: {result.id}")
    print("Waiting for result...")

    while not result.ready():
        print("⏳ Still running...")
        time.sleep(2)

    print("\n✅ Task completed!")

    # Raw result from Celery
    raw = result.result
    print("Raw result:", raw)

    # Safely extract the inner dictionary
    if raw and "result" in raw:
        final = raw["result"]
        print("\n🎯 Extracted Results:")
        print("Best solution:", final.get("best_solution"))
        print("Best fitness:", final.get("best_fitness"))
        print("Convergence curve:", final.get("convergence_curve"))
    else:
        print("⚠️ Unexpected result format:", raw)


if __name__ == "__main__":
    main()
