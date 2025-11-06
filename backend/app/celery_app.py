from celery import Celery
import os

# Use environment variable; default for local docker-compose is redis://redis:6379/0
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery = Celery(
    "optimizehub",
    broker_url=REDIS_URL,
    result_backend=REDIS_URL,
    include=["app.tasks"],
)

celery.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    enable_utc=True,
    timezone="UTC",
    # example time limits (adjust per-algorithm in production)
    task_time_limit=600,      # hard limit seconds
    task_soft_time_limit=550, # soft limit seconds
)