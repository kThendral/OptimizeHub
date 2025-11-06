from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from celery import group
from celery.result import AsyncResult

from ..tasks import run_algorithm
from ..celery_app import celery

router = APIRouter(prefix="/async", tags=["async"])

class ProblemRequest(BaseModel):
    problem: Dict[str, Any]
    algorithms: List[str]  # e.g. ["genetic", "simulated_annealing"]

@router.post("/optimize")
def optimize(problem_req: ProblemRequest):
    """
    Submit a group of algorithm tasks to Celery (runs in parallel).
    Returns the group id and the child task ids to poll for results.
    """
    if not problem_req.algorithms:
        raise HTTPException(status_code=400, detail="No algorithms specified")

    # Create a group of signatures
    sigs = [run_algorithm.s(algo, problem_req.problem) for algo in problem_req.algorithms]
    job = group(sigs)
    group_result = job.apply_async()
    child_ids = [res.id for res in group_result.results]

    return {"group_id": group_result.id, "task_ids": child_ids}

@router.get("/tasks/{task_id}")
def get_task_status(task_id: str):
    async_res = AsyncResult(task_id, app=celery)
    state = async_res.state
    response = {"task_id": task_id, "state": state}
    if async_res.ready():
        response["result"] = async_res.result
    elif state == "FAILURE":
        response["result"] = async_res.info  # Error details
    return response
