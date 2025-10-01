# Create a Celery task that runs the Genetic Algorithm
# The task should:
# 1. Accept problem definition and GA params.
# 2. Instantiate GeneticAlgorithm with inputs.
# 3. Run initialize() and optimize().
# 4. Return results as a dictionary.

from celery import Celery
from app.algorithms.genetic_algorithm import GeneticAlgorithm

celery_app = Celery(
    "optimizehub",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

@celery_app.task
def run_genetic_algorithm(problem: dict, params: dict):
    ga = GeneticAlgorithm(problem, params)
    ga.initialize()
    ga.optimize()
    return ga.get_results()
