# Docker Sandboxing for Custom Fitness Functions

Complete guide to using the Docker-based sandboxing feature for securely executing user-uploaded custom fitness functions in OptimizeHub.

---

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Security Features](#security-features)
- [Setup Instructions](#setup-instructions)
- [Usage Guide](#usage-guide)
- [Creating Custom Fitness Functions](#creating-custom-fitness-functions)
- [Configuration Reference](#configuration-reference)
- [API Reference](#api-reference)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Production Deployment](#production-deployment)
- [Technical Details](#technical-details)

---

## Overview

The Docker sandboxing feature allows users to upload custom Python fitness functions that are executed in isolated Docker containers. This provides:

✅ **Security** - Malicious code cannot harm the platform
✅ **Flexibility** - Users can define any optimization problem
✅ **Compatibility** - Works with all 5 algorithms (PSO, GA, DE, SA, ACOR)
✅ **User-Friendly** - Simple upload interface with real-time results

### Key Features

- **Isolated Execution**: Each function runs in a separate Docker container
- **AST Validation**: Static code analysis blocks dangerous operations
- **Resource Limits**: 512MB RAM, 2 CPUs, 30-second timeout
- **No Network Access**: Containers cannot connect to the internet
- **Read-Only Filesystem**: Cannot modify files (except /tmp)
- **Automatic Cleanup**: Containers and temp files are destroyed after execution

---

## Quick Start

### 5-Minute Setup

```bash
# 1. Build Docker image (2 minutes)
./setup_docker_sandbox.sh

# 2. Install backend dependencies (1 minute)
cd backend
pip install -r requirements.txt

# 3. Start backend
uvicorn app.main:app --reload

# 4. Start frontend (new terminal)
cd frontend
npm install && npm run dev

# 5. Test it!
# Open http://localhost:5173
# Click "Custom Fitness 🔒" tab
# Upload: examples/custom_fitness/sphere_fitness.py
# Upload: examples/custom_fitness/sphere_config.yaml
# Click "Run Optimization"
```

### Test with API

```bash
curl -X POST http://localhost:8000/api/optimize/custom \
  -F "fitness_file=@examples/custom_fitness/sphere_fitness.py" \
  -F "config_file=@examples/custom_fitness/sphere_config.yaml"
```

---

## Architecture

### System Flow

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend                             │
│  - Upload .py + .yaml files                                 │
│  - Display results & convergence charts                     │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTP POST /api/optimize/custom
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                           │
│  1. Validate file types & sizes (max 1MB each)              │
│  2. Run AST security validation                             │
│  3. Parse YAML configuration                                │
│  4. Create unique execution directory                       │
│  5. Spawn Docker container (isolated)                       │
│  6. Monitor execution (30s timeout)                         │
│  7. Parse JSON results from stdout                          │
│  8. Cleanup temp files & destroy container                  │
└────────────────────┬────────────────────────────────────────┘
                     │ Docker SDK
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              Docker Container (Isolated)                     │
│                                                              │
│  Environment:                                                │
│  - Python 3.11-slim base image                              │
│  - numpy 1.24.3 (only library)                              │
│  - Read-only filesystem (except /tmp)                       │
│  - No network access (--network none)                       │
│  - Non-root user (1000:1000)                                │
│  - 512MB RAM limit                                          │
│  - 2 CPU cores limit                                        │
│  - 30 second hard timeout                                   │
│                                                              │
│  Execution Steps:                                            │
│  1. Load user's fitness function                            │
│  2. Load algorithm configuration                            │
│  3. Run selected algorithm (PSO/GA/DE/SA/ACOR)             │
│  4. Output JSON results to stdout                           │
│  5. Exit (container auto-destroyed)                         │
└─────────────────────────────────────────────────────────────┘
```

### Components

| Component | Location | Purpose |
|-----------|----------|---------|
| **Dockerfile.sandbox** | `backend/docker/` | Minimal Python image definition |
| **runner.py** | `backend/docker/` | Container execution script (495 lines) |
| **code_validator.py** | `backend/app/validators/` | AST security scanner (273 lines) |
| **docker_executor.py** | `backend/app/services/` | Container lifecycle manager (263 lines) |
| **routes.py** | `backend/app/api/` | API endpoint `/optimize/custom` |
| **CustomFitnessUpload.jsx** | `frontend/src/components/` | Upload UI (369 lines) |

---

## Security Features

### Multi-Layer Security

| Layer | Protection | Implementation |
|-------|------------|----------------|
| **Input Validation** | File type/size checks | FastAPI route validation |
| **AST Analysis** | Static code scanning | Python `ast` module |
| **Docker Isolation** | Container sandboxing | Docker SDK with resource limits |
| **Network Blocking** | No internet access | `--network none` flag |
| **Filesystem Protection** | Read-only FS | `--read-only` + tmpfs |
| **Resource Limits** | CPU/RAM/time caps | Docker constraints |
| **User Restrictions** | Non-root execution | User 1000:1000 |

### AST Validator Checks

The security validator blocks:

❌ **Forbidden Imports**
- `os`, `sys`, `subprocess` - System operations
- `socket`, `urllib`, `http`, `requests` - Network operations
- `pickle`, `shelve`, `marshal` - Serialization (code execution risk)
- `multiprocessing`, `threading` - Process/thread spawning
- `importlib`, `__import__` - Dynamic imports

❌ **Forbidden Operations**
- `open()`, `read()`, `write()` - File I/O
- `eval()`, `exec()`, `compile()` - Code execution
- `with` statements - Often used for file operations
- Dunder attribute access (`__globals__`, `__code__`, etc.)

✅ **Allowed Operations**
- `import math` or `import numpy as np`
- Basic Python operations (loops, conditionals, functions)
- NumPy array operations
- Math functions
- Return numeric values

---

## Setup Instructions

### Prerequisites

1. **Docker** (required)
   ```bash
   # Check installation
   docker --version
   # Should output: Docker version 20.x.x or higher

   # Verify daemon is running
   docker info
   ```

2. **Python 3.11+**
   ```bash
   python --version
   ```

3. **Node.js 18+**
   ```bash
   node --version
   npm --version
   ```

### Installation Steps

#### 1. Build Docker Sandbox Image

```bash
# Automated setup (recommended)
./setup_docker_sandbox.sh

# Manual setup
cd backend
docker build -t optimizehub-sandbox:latest -f docker/Dockerfile.sandbox docker/
```

**Verify the build:**
```bash
docker images | grep optimizehub-sandbox
```

Expected output:
```
optimizehub-sandbox   latest   <image-id>   <time>   ~200MB
```

#### 2. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

New dependencies added:
- `python-multipart==0.0.9` - File upload handling
- `PyYAML==6.0.1` - YAML configuration parsing

#### 3. Start Services

**Terminal 1 - Backend:**
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
Backend: http://localhost:8000
API Docs: http://localhost:8000/docs

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install  # First time only
npm run dev
```
Frontend: http://localhost:5173

---

## Usage Guide

### Method 1: Web Interface (Recommended)

1. Open http://localhost:5173 in browser
2. Click "Start Optimizing"
3. Click **"Custom Fitness 🔒"** tab
4. Upload your fitness function (.py file)
5. Upload your configuration (.yaml file)
6. Click "Run Optimization"
7. View results and convergence chart

### Method 2: API with curl

```bash
curl -X POST http://localhost:8000/api/optimize/custom \
  -F "fitness_file=@path/to/fitness.py" \
  -F "config_file=@path/to/config.yaml"
```

### Method 3: API with Python

```python
import requests

files = {
    'fitness_file': open('fitness.py', 'rb'),
    'config_file': open('config.yaml', 'rb')
}

response = requests.post(
    'http://localhost:8000/api/optimize/custom',
    files=files
)

result = response.json()
print(f"Best fitness: {result['best_fitness']}")
print(f"Best solution: {result['best_solution']}")
```

### Method 4: Postman

1. Create POST request to `http://localhost:8000/api/optimize/custom`
2. Body → form-data
3. Add `fitness_file` (File type) → select .py file
4. Add `config_file` (File type) → select .yaml file
5. Send

---

## Creating Custom Fitness Functions

### Template

```python
import numpy as np

def fitness(x):
    """
    Your fitness function description.

    Args:
        x: numpy array of decision variables

    Returns:
        float: fitness value to minimize
    """
    # Your optimization problem here
    return np.sum(x**2)  # Example: sphere function
```

### Requirements

| Requirement | Description |
|-------------|-------------|
| **Function name** | MUST be `fitness` (exact, lowercase) |
| **Parameters** | MUST accept exactly one parameter `x` (numpy array) |
| **Return type** | MUST return a number (int, float, np.number) |
| **Imports** | ONLY `math` and `numpy` (as `np`) allowed |
| **Operations** | No file I/O, network, or system calls |

### Examples

#### Example 1: Sphere Function (Simple)
```python
import numpy as np

def fitness(x):
    """Sphere function: f(x) = sum(x_i^2)"""
    return np.sum(x**2)
```

#### Example 2: Rosenbrock Function (Complex)
```python
import numpy as np

def fitness(x):
    """Rosenbrock function - classic benchmark"""
    return np.sum(100.0 * (x[1:] - x[:-1]**2)**2 + (1 - x[:-1])**2)
```

#### Example 3: Custom with Penalty
```python
import numpy as np

def fitness(x):
    """Custom function with L1 regularization"""
    objective = np.sum(x**2)
    penalty = 0.1 * np.sum(np.abs(x))
    return objective + penalty
```

#### Example 4: Using Math Library
```python
import math
import numpy as np

def fitness(x):
    """Using math library for trigonometric functions"""
    return sum(math.sin(xi)**2 + math.cos(xi) for xi in x)
```

### Configuration File

```yaml
algorithm: PSO  # Options: PSO, GA, DE, SA, ACOR

parameters:
  # PSO parameters
  num_particles: 30      # Population size
  max_iterations: 100    # Number of iterations
  w: 0.7                 # Inertia weight
  c1: 1.5                # Cognitive parameter
  c2: 1.5                # Social parameter

problem:
  dimensions: 10         # Problem dimensionality
  lower_bound: -5.0      # Lower bound for all variables
  upper_bound: 5.0       # Upper bound for all variables
```

---

## Configuration Reference

### Algorithm-Specific Parameters

#### PSO (Particle Swarm Optimization)
```yaml
algorithm: PSO
parameters:
  num_particles: 30      # 10-100 typical
  max_iterations: 100    # 50-500 typical
  w: 0.7                 # Inertia (0.4-0.9)
  c1: 1.5                # Cognitive (1.0-2.0)
  c2: 1.5                # Social (1.0-2.0)
```

#### GA (Genetic Algorithm)
```yaml
algorithm: GA
parameters:
  population_size: 50    # 20-200 typical
  max_generations: 100   # 50-500 typical
  mutation_rate: 0.1     # 0.01-0.2
  crossover_rate: 0.8    # 0.6-0.95
```

#### DE (Differential Evolution)
```yaml
algorithm: DE
parameters:
  population_size: 50    # 5*dimensions typical
  max_generations: 100
  F: 0.8                 # Differential weight (0.5-1.0)
  CR: 0.9                # Crossover probability (0.5-1.0)
```

#### SA (Simulated Annealing)
```yaml
algorithm: SA
parameters:
  max_iterations: 1000   # Higher than population-based
  initial_temperature: 100.0
  cooling_rate: 0.95     # 0.8-0.99
```

#### ACOR (Ant Colony for Continuous Domains)
```yaml
algorithm: ACOR
parameters:
  num_ants: 50
  max_iterations: 100
  archive_size: 50
  q: 0.5                 # 0.01-1.0
  xi: 0.85               # 0.5-1.0
```

---

## API Reference

### Endpoint: POST /api/optimize/custom

**URL**: `http://localhost:8000/api/optimize/custom`

**Method**: `POST`

**Content-Type**: `multipart/form-data`

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `fitness_file` | File | Yes | Python file containing fitness function (.py) |
| `config_file` | File | Yes | YAML configuration file (.yaml or .yml) |

**Success Response (200 OK)**:
```json
{
  "status": "success",
  "algorithm": "PSO",
  "best_solution": [0.001, -0.002, 0.003, ...],
  "best_fitness": 0.000014,
  "iterations": 100,
  "convergence_history": [1.5, 0.8, 0.3, ...],
  "execution_time": 2.45,
  "message": "Optimization completed successfully using custom fitness function"
}
```

**Error Responses**:

**400 Bad Request** - Validation failed
```json
{
  "detail": {
    "error": "Security validation failed",
    "message": "Import 'os' not allowed. Only 'math' and 'numpy' are permitted."
  }
}
```

**500 Internal Server Error** - Execution failed
```json
{
  "detail": {
    "error": "Execution failed",
    "error_type": "timeout",
    "message": "Optimization exceeded 30 seconds timeout. Try reducing iterations or problem complexity."
  }
}
```

**Error Types**:
- `validation_error` - Security/code validation failed
- `timeout` - Execution exceeded 30 seconds
- `container_error` - Docker container failed
- `parse_error` - Failed to parse output
- `execution_error` - General execution error

---

## Testing

### Quick Tests

#### 1. Test with Sphere Function
```bash
curl -X POST http://localhost:8000/api/optimize/custom \
  -F "fitness_file=@examples/custom_fitness/sphere_fitness.py" \
  -F "config_file=@examples/custom_fitness/sphere_config.yaml"
```
**Expected**: `best_fitness` ≈ 0.0, `best_solution` ≈ [0, 0, ..., 0]

#### 2. Test with Rosenbrock Function
```bash
curl -X POST http://localhost:8000/api/optimize/custom \
  -F "fitness_file=@examples/custom_fitness/rosenbrock_fitness.py" \
  -F "config_file=@examples/custom_fitness/rosenbrock_config.yaml"
```
**Expected**: `best_fitness` ≈ 0.0, `best_solution` ≈ [1, 1, ..., 1]

#### 3. Test Security Validator
```bash
cd backend/app/validators
python code_validator.py
```
All tests should pass.

### Component Tests

#### Test Docker Executor
```python
from app.services.docker_executor import get_docker_executor

executor = get_docker_executor()

test_code = """
import numpy as np
def fitness(x):
    return np.sum(x**2)
"""

test_config = {
    "algorithm": "PSO",
    "parameters": {
        "num_particles": 20,
        "max_iterations": 50,
        "w": 0.7,
        "c1": 1.5,
        "c2": 1.5
    },
    "problem": {
        "dimensions": 5,
        "lower_bound": -5.0,
        "upper_bound": 5.0
    }
}

result = executor.execute_custom_fitness(test_code, test_config)
print(result)
```

#### Test Code Validator
```python
from app.validators.code_validator import validate_fitness_code

# Valid code
valid_code = """
import numpy as np
def fitness(x):
    return np.sum(x**2)
"""
is_valid, error = validate_fitness_code(valid_code)
print(f"Valid: {is_valid}, Error: {error}")

# Invalid code (file I/O)
invalid_code = """
def fitness(x):
    with open('file.txt', 'r') as f:
        data = f.read()
    return sum(x)
"""
is_valid, error = validate_fitness_code(invalid_code)
print(f"Valid: {is_valid}, Error: {error}")
```

---

## Troubleshooting

### Common Issues

#### Issue: "Docker is not installed or not in PATH"
**Cause**: Docker not installed or not accessible

**Solution**:
1. Install Docker: https://docs.docker.com/get-docker/
2. On Mac/Windows: Start Docker Desktop
3. On Linux: `sudo systemctl start docker`
4. Verify: `docker --version`

#### Issue: "Docker daemon is not running"
**Cause**: Docker service is not started

**Solution**:
- **Mac/Windows**: Start Docker Desktop application
- **Linux**: `sudo systemctl start docker`
- Verify: `docker info`

#### Issue: "Docker image not found"
**Cause**: Sandbox image not built

**Solution**:
```bash
./setup_docker_sandbox.sh
# Or manually:
cd backend
docker build -t optimizehub-sandbox:latest -f docker/Dockerfile.sandbox docker/
```

#### Issue: "Permission denied" (Linux)
**Cause**: User not in docker group

**Solution**:
```bash
sudo usermod -aG docker $USER
newgrp docker
# Log out and log back in
```

#### Issue: "Execution exceeded 30 seconds timeout"
**Causes**:
- Too many iterations
- High problem dimensionality
- Complex fitness function

**Solutions**:
- Reduce `max_iterations` in config
- Reduce `dimensions` in problem
- Simplify fitness function
- Increase timeout in `docker_executor.py:24` (advanced)

#### Issue: "Import 'os' not allowed"
**Cause**: Forbidden import in fitness function

**Solution**:
Remove unauthorized imports. Only `math` and `numpy` are allowed:
```python
# ❌ Wrong
import os
import sys

# ✅ Correct
import math
import numpy as np
```

#### Issue: "Fitness function must be named 'fitness'"
**Cause**: Function has different name

**Solution**:
Rename your function to exactly `fitness`:
```python
# ❌ Wrong
def my_fitness(x):
    return sum(x**2)

# ✅ Correct
def fitness(x):
    return sum(x**2)
```

#### Issue: "CORS error in frontend"
**Cause**: Backend not running or CORS misconfigured

**Solution**:
1. Ensure backend is running on port 8000
2. Access frontend via `http://localhost:5173` (not 127.0.0.1)
3. Check CORS settings in `backend/app/main.py`

#### Issue: "Container failed to start"
**Diagnosis**:
```bash
# List all containers
docker ps -a

# Check logs
docker logs <container-id>
```

**Common causes**:
- Docker daemon not running
- Insufficient resources (RAM/disk)
- Port conflicts

---

## Production Deployment

### Recommended Enhancements

#### 1. Authentication
Add JWT or OAuth:
```python
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

security = HTTPBearer()

@router.post("/optimize/custom")
async def optimize_custom(
    ...,
    token: str = Depends(security)
):
    # Verify token
    verify_token(token)
    ...
```

#### 2. Rate Limiting
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@limiter.limit("5/minute")
@router.post("/optimize/custom")
async def optimize_custom(...):
    ...
```

#### 3. Execution Queue
Use Celery + Redis for async execution:
```python
from celery import Celery

app = Celery('tasks', broker='redis://localhost:6379')

@app.task
def run_optimization(fitness_code, config):
    executor = get_docker_executor()
    return executor.execute_custom_fitness(fitness_code, config)
```

#### 4. Monitoring
```python
from prometheus_client import Counter, Histogram

execution_counter = Counter('optimization_executions_total', 'Total executions')
execution_duration = Histogram('optimization_duration_seconds', 'Execution duration')

@router.post("/optimize/custom")
async def optimize_custom(...):
    execution_counter.inc()
    with execution_duration.time():
        # Execute optimization
        ...
```

#### 5. Resource Quotas
Add per-user limits in database:
```python
def check_user_quota(user_id: str):
    executions_today = db.count_executions(user_id, today)
    if executions_today >= MAX_DAILY_EXECUTIONS:
        raise HTTPException(429, "Daily quota exceeded")
```

### Kubernetes Deployment

**Example deployment:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: optimizehub-backend
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: backend
        image: optimizehub-backend:latest
        resources:
          limits:
            memory: "2Gi"
            cpu: "1000m"
        volumeMounts:
        - name: docker-sock
          mountPath: /var/run/docker.sock
      volumes:
      - name: docker-sock
        hostPath:
          path: /var/run/docker.sock
```

**Security considerations**:
- Use Pod Security Policies
- Limit Docker socket access
- Use separate node pool for execution
- Implement network policies

---

## Technical Details

### Resource Limits

| Resource | Limit | Configurable In |
|----------|-------|-----------------|
| Execution timeout | 30 seconds | `docker_executor.py:24` |
| Memory limit | 512 MB | `docker_executor.py:25` |
| CPU limit | 2 cores | `docker_executor.py:26` |
| File size | 1 MB each | `routes.py:129,135` |
| Max dimensions | Unlimited | Config file |
| Max iterations | Unlimited | Config file |

### Performance Metrics

| Metric | Typical Value |
|--------|---------------|
| Image size | ~200 MB |
| Container startup | ~500 ms |
| First execution | 2-5 seconds |
| Subsequent executions | 1-3 seconds overhead |
| Result parsing | ~100 ms |
| Cleanup | ~200 ms |

### File Sizes

| Component | Lines | Size |
|-----------|-------|------|
| runner.py | 495 | 15 KB |
| code_validator.py | 273 | 9 KB |
| docker_executor.py | 263 | 9 KB |
| CustomFitnessUpload.jsx | 369 | 12 KB |
| CustomFitnessUpload.css | 321 | 9 KB |
| **Total (new code)** | **1,721** | **54 KB** |

### Docker Image Layers

```
python:3.11-slim          ~150 MB
├── numpy==1.24.3         ~50 MB
└── user setup            <1 MB
────────────────────────────────
Total:                    ~200 MB
```

---

## Additional Resources

- **Docker Security**: https://docs.docker.com/engine/security/
- **FastAPI File Uploads**: https://fastapi.tiangolo.com/tutorial/request-files/
- **Python AST**: https://docs.python.org/3/library/ast.html
- **Example Files**: `examples/custom_fitness/README.md`

---

## Support

If you encounter issues:

1. **Check logs**:
   - Docker: `docker logs <container-id>`
   - Backend: Terminal where uvicorn is running
   - Frontend: Browser console (F12)

2. **Verify setup**:
   ```bash
   # Check Docker
   docker --version
   docker images | grep optimizehub-sandbox

   # Check backend
   curl http://localhost:8000/api/health

   # Check frontend
   curl http://localhost:5173
   ```

3. **Test components individually**:
   ```bash
   # Test validator
   cd backend/app/validators && python code_validator.py

   # Test executor
   cd backend/app/services && python docker_executor.py
   ```

4. **Review examples**: Check `examples/custom_fitness/` for working examples

---

## Summary

✅ **Secure**: Multi-layer security with Docker + AST validation
✅ **Flexible**: Supports all 5 algorithms with custom fitness
✅ **Easy to Use**: Simple upload interface
✅ **Well-Documented**: Complete guides and examples
✅ **Production-Ready**: With recommended enhancements

**Implementation Date**: 2025-11-05
**Version**: 1.0
**Status**: ✅ Complete and tested

---

**Happy Optimizing! 🚀**
