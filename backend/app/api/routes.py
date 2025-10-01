# Write a FastAPI endpoint to trigger the GA task
# The endpoint should:
# 1. Accept a JSON body with problem + params.
# 2. Call run_genetic_algorithm.delay() to enqueue task.
# 3. Return task ID so frontend can poll for results.

from fastapi import APIRouter
from app.core.tasks import run_genetic_algorithm

router = APIRouter()

@router.post("/optimize/ga")
def run_ga(problem: dict, params: dict):
    task = run_genetic_algorithm.delay(problem, params)
    return {"task_id": task.id}
