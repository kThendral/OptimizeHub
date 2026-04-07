from celery import Celery
import os
import ssl as _ssl

# REDIS_URL must be set in the environment (Upstash: rediss://default:PASSWORD@HOST.upstash.io:6379)
REDIS_URL = os.environ.get("REDIS_URL")

celery = Celery(
    "optimizehub",
    broker_url=REDIS_URL,
    result_backend=REDIS_URL,
    include=["app.tasks"]
)

celery.conf.update(
    # Serialization
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    enable_utc=True,
    timezone="UTC",

    # Timeouts — Modal cold-start adds ~30-60 s on top of the 30 s execution timeout.
    task_time_limit=90,
    task_soft_time_limit=75,

    # Upstash compatibility — TLS + connection constraints
    broker_transport_options={
        "visibility_timeout": 3600,      # 1 hour — prevents task re-queuing during long runs
        "socket_timeout": 30,
        "socket_connect_timeout": 30,
        "retry_on_timeout": True,
    },
    # SSL for broker (kombu) and backend — required for rediss:// URLs (Upstash)
    broker_use_ssl={"ssl_cert_reqs": _ssl.CERT_NONE},
    redis_backend_use_ssl={"ssl_cert_reqs": _ssl.CERT_NONE},
    redis_socket_timeout=30,
    redis_socket_connect_timeout=30,
    redis_retry_on_timeout=True,

    # Connection pool — Upstash free tier has connection limits (max 100)
    broker_pool_limit=3,
    redis_max_connections=10,

    # Worker config
    worker_prefetch_multiplier=1,        # one task at a time per worker
    task_acks_late=True,                 # only ack after task completes
    worker_cancel_long_running_tasks_on_connection_loss=True,
)

# Explicitly import tasks to ensure registration
import app.tasks
