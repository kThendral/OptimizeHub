"""
Upstash Redis migration verification tests.

These tests connect to the REAL Upstash Redis URL from the REDIS_URL environment
variable — Redis is NOT mocked. The purpose is to verify the actual cloud
connection works end-to-end.

Prerequisites:
  - REDIS_URL must be set in the environment (or backend/.env)
  - For Test 4 (Celery round-trip), a Celery worker must be running:
      cd backend && celery -A app.celery_app.celery worker --loglevel=info

Run from the backend/ directory:
    python -m pytest tests/test_upstash_migration.py -v
"""

import os
import sys
import threading
import time

import pytest

# Ensure the backend package root is on the path when running from any directory
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))

REDIS_URL = os.environ.get("REDIS_URL")

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _require_redis_url():
    """Skip a test with a clear message when REDIS_URL is not configured."""
    if not REDIS_URL:
        pytest.skip("REDIS_URL not set — set it in backend/.env or the environment")
    if REDIS_URL.startswith("redis://localhost") or REDIS_URL.startswith("redis://127"):
        pytest.skip(
            "REDIS_URL points to local Redis, not Upstash — "
            "set it to your Upstash rediss:// URL to run migration tests"
        )
    # Detect unfilled placeholder values from .env.example / .env
    if "YOUR_UPSTASH" in REDIS_URL or "YOUR_" in REDIS_URL:
        pytest.skip(
            "REDIS_URL still contains placeholder values — "
            "replace YOUR_UPSTASH_PASSWORD and YOUR_UPSTASH_HOST in backend/.env "
            "with your real Upstash credentials from https://console.upstash.com"
        )


# ---------------------------------------------------------------------------
# Test 1 — Celery broker connection
# ---------------------------------------------------------------------------

def test_celery_broker_connection():
    """
    Verify Celery can connect to Upstash as its broker.

    We use celery.control.inspect(timeout=5).ping(). This sends a control
    command over the broker transport. A ConnectionError here means the broker
    URL is wrong or unreachable. None/empty result is acceptable (no workers
    running), but no exception should be raised.
    """
    _require_redis_url()

    from app.celery_app import celery

    try:
        inspect = celery.control.inspect(timeout=5)
        result = inspect.ping()
        # result is None when no workers are running — that is fine.
        # What we're testing is that no ConnectionError is raised.
        assert result is None or isinstance(result, dict), (
            f"Unexpected ping result type: {type(result)}"
        )
    except Exception as exc:
        pytest.fail(f"Celery broker connection failed: {exc}")

    print("\n[TEST 1] Celery broker connection to Upstash: OK")


# ---------------------------------------------------------------------------
# Test 2 — Direct Redis SET / GET
# ---------------------------------------------------------------------------

def test_direct_redis_set_get():
    """
    Connect to Upstash directly, run SET and GET, assert they work.

    ssl_cert_reqs=None disables certificate verification — required for
    Upstash free-tier certs on some platforms.
    """
    _require_redis_url()

    import redis

    r = redis.from_url(REDIS_URL, ssl_cert_reqs=None)

    key = "optimizehub_test_key"
    value = "migration_test"

    try:
        r.set(key, value, ex=60)
        retrieved = r.get(key)
        assert retrieved is not None, "GET returned None — SET may have failed"
        assert retrieved.decode() == value, (
            f"Expected '{value}', got '{retrieved.decode()}'"
        )
    finally:
        r.delete(key)

    print("\n[TEST 2] Direct Redis SET/GET on Upstash: OK")


# ---------------------------------------------------------------------------
# Test 3 — Pub/Sub works with Upstash
# ---------------------------------------------------------------------------

def test_pubsub():
    """
    Verify Redis pub/sub works over the Upstash TLS connection.

    NOTE: This project's SSE endpoint does NOT use Redis pub/sub — it polls
    Celery AsyncResult state instead. This test validates that pub/sub is
    available on the Upstash connection in case it is used in the future,
    and confirms the connection itself is healthy.

    A subscriber thread listens on a test channel; the main thread publishes
    one message and verifies it is received.
    """
    _require_redis_url()

    import redis

    CHANNEL = "optimizehub:test:progress"
    received = []
    subscriber_ready = threading.Event()

    def subscriber():
        r_sub = redis.from_url(REDIS_URL, ssl_cert_reqs=None)
        p = r_sub.pubsub()
        p.subscribe(CHANNEL)
        # Signal that we have subscribed before the publisher runs
        for message in p.listen():
            if message["type"] == "subscribe":
                subscriber_ready.set()
            if message["type"] == "message":
                received.append(message["data"])
                break

    t = threading.Thread(target=subscriber, daemon=True)
    t.start()

    # Wait up to 5 s for the subscriber to be ready
    subscriber_ready.wait(timeout=5)
    assert subscriber_ready.is_set(), "Subscriber did not subscribe within 5 s"

    r_pub = redis.from_url(REDIS_URL, ssl_cert_reqs=None)
    r_pub.publish(CHANNEL, '{"iteration": 1, "best_fitness": 0.5}')

    t.join(timeout=5)
    assert len(received) == 1, f"Expected 1 message, got {len(received)}"
    assert b"best_fitness" in received[0], f"Unexpected payload: {received[0]}"

    print(f"\n[TEST 3] Pub/Sub on Upstash: OK (received: {received[0]})")


# ---------------------------------------------------------------------------
# Test 4 — Celery task round-trip
# ---------------------------------------------------------------------------

def test_celery_task_roundtrip():
    """
    Submit a lightweight ping task to Celery and verify the result arrives
    via the Upstash backend within 30 seconds.

    IMPORTANT: This test requires a running Celery worker. Start one with:
        cd backend && celery -A app.celery_app.celery worker --loglevel=info

    If no worker is running, the task will remain PENDING and the test will
    time out with a clear message.
    """
    _require_redis_url()

    from app.celery_app import celery

    @celery.task(name="optimizehub.tests.ping")
    def _test_ping():
        return "pong"

    try:
        async_result = _test_ping.delay()
        result = async_result.get(timeout=30)
    except Exception as exc:
        exc_name = type(exc).__name__
        if "TimeoutError" in exc_name or "TimeLimitExceeded" in exc_name:
            pytest.fail(
                "Task timed out waiting for result. "
                "Is a Celery worker running? "
                "Start one with: celery -A app.celery_app.celery worker --loglevel=info"
            )
        pytest.fail(f"Celery task round-trip failed: {exc}")

    assert result == "pong", f"Expected 'pong', got: {result!r}"
    print(f"\n[TEST 4] Celery task round-trip via Upstash: OK (result={result!r})")


# ---------------------------------------------------------------------------
# Test 5 — SSE streaming pipeline simulation
# ---------------------------------------------------------------------------

def test_sse_streaming_pipeline():
    """
    Simulate the full SSE streaming pipeline end-to-end.

    The actual SSE endpoint (app/api/sse.py) polls Celery AsyncResult state —
    it does NOT use Redis pub/sub channels. This test simulates that pattern:

      1. A mock task result is stored directly in the Celery result backend
         (Upstash Redis) using Celery's internal store API.
      2. An AsyncResult is constructed for that task ID.
      3. We verify AsyncResult.state and .result are readable from Upstash,
         matching the SSE endpoint's polling loop.

    This validates that the Upstash backend correctly stores and retrieves
    task results — which is the data path the real SSE endpoint depends on.
    """
    _require_redis_url()

    import uuid
    from celery.result import AsyncResult
    from app.celery_app import celery

    task_id = str(uuid.uuid4())
    expected_result = {"iteration": 3, "best_fitness": 0.42, "status": "SUCCESS"}

    # Store a fake result directly in the Celery backend (Upstash)
    backend = celery.backend
    backend.store_result(
        task_id,
        expected_result,
        "SUCCESS",
    )

    # Now read it back via AsyncResult — same path as the SSE endpoint
    async_result = AsyncResult(task_id, app=celery)

    assert async_result.state == "SUCCESS", (
        f"Expected state SUCCESS, got {async_result.state}"
    )
    stored = async_result.result
    assert stored == expected_result, (
        f"Result mismatch.\nExpected: {expected_result}\nGot:      {stored}"
    )

    # Simulate 3 progress updates read by the SSE polling loop
    updates_received = []
    for i in range(3):
        state = async_result.state
        result = async_result.result if state == "SUCCESS" else None
        updates_received.append({"state": state, "result": result})

    assert len(updates_received) == 3
    assert all(u["state"] == "SUCCESS" for u in updates_received)
    assert all(u["result"] == expected_result for u in updates_received)

    # Clean up — forget() is the correct AsyncResult API (removes from backend)
    async_result.forget()

    print(f"\n[TEST 5] SSE streaming pipeline simulation via Upstash: OK")
    print(f"         Polled {len(updates_received)} updates, all state=SUCCESS")
