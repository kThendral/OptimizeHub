"""
Server-Sent Events (SSE) endpoint for real-time task status updates.

Provides streaming updates for Celery task status without polling.
"""
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from celery.result import AsyncResult
import json
import asyncio
import logging

from ..celery_app import celery

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/async/tasks/{task_id}/stream")
async def stream_task_status(task_id: str):
    """
    Stream task status updates via Server-Sent Events.

    Client receives updates every 1 second until task completes (SUCCESS or FAILURE).

    Args:
        task_id: Celery task ID to monitor

    Returns:
        StreamingResponse with text/event-stream content type

    Event format:
        data: {"task_id": "...", "state": "PENDING|STARTED|SUCCESS|FAILURE", "result": {...}, "error": "..."}

    Usage:
        const eventSource = new EventSource(`/api/async/tasks/${taskId}/stream`);
        eventSource.onmessage = (event) => {
            const data = JSON.parse(event.data);
            console.log(data.state, data.result);
        };
    """

    async def event_stream():
        """
        Generator function that yields SSE-formatted task status updates.
        """
        logger.info(f"Starting SSE stream for task: {task_id}")

        try:
            while True:
                # Get task status from Celery
                async_result = AsyncResult(task_id, app=celery)

                status_data = {
                    "task_id": task_id,
                    "state": async_result.state,
                    "result": None,
                    "error": None
                }

                # Handle different task states
                if async_result.state == "SUCCESS":
                    status_data["result"] = async_result.result
                    logger.info(f"Task {task_id} completed successfully")
                    yield f"data: {json.dumps(status_data)}\n\n"
                    break  # Stop streaming on success

                elif async_result.state == "FAILURE":
                    # Get error information
                    error_info = str(async_result.info) if async_result.info else "Unknown error"
                    status_data["error"] = error_info
                    logger.warning(f"Task {task_id} failed: {error_info}")
                    yield f"data: {json.dumps(status_data)}\n\n"
                    break  # Stop streaming on failure

                elif async_result.state in ["PENDING", "STARTED"]:
                    # Task is still running - send update
                    yield f"data: {json.dumps(status_data)}\n\n"

                else:
                    # Unknown state - send update
                    logger.debug(f"Task {task_id} in state: {async_result.state}")
                    yield f"data: {json.dumps(status_data)}\n\n"

                # Wait 1 second before next update
                await asyncio.sleep(1)

        except asyncio.CancelledError:
            # Client disconnected
            logger.info(f"SSE stream cancelled for task: {task_id}")

        except Exception as e:
            # Unexpected error
            logger.error(f"Error in SSE stream for task {task_id}: {str(e)}", exc_info=True)
            error_data = {
                "task_id": task_id,
                "state": "ERROR",
                "result": None,
                "error": f"Stream error: {str(e)}"
            }
            yield f"data: {json.dumps(error_data)}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # Disable buffering in nginx
        }
    )
