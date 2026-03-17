# OptimizeHub 🚀

**OptimizeHub** is a modern web platform for running optimization algorithms including Particle Swarm Optimization (PSO), Genetic Algorithm (GA), and more. Built with FastAPI (backend) and React + Vite (frontend).

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![React](https://img.shields.io/badge/react-19.1.1-blue.svg)

---

## ✨ Features

- **🎯 Multiple Algorithms**: PSO, GA, DE, SA, ACOR (5 algorithms available)
- **📊 5 Benchmark Functions**: Sphere, Rastrigin, Rosenbrock, Ackley, Griewank
- **🔒 Custom Fitness Functions**: Upload your own Python code in secure Docker sandbox
- **🎨 Modern UI**: Clean interface with Deep Violet color scheme
- **📝 Triple Input Modes**:
  - Manual form input with parameter explanations
  - YAML file upload for automation
  - Custom fitness function upload (Docker-isolated)
- **🔧 Hybrid Component Architecture**: Shared + algorithm-specific forms
- **📈 Real-time Results**: View solutions, fitness, and convergence data
- **🔐 Security**: Docker isolation, AST validation, resource limits
- **📚 Beginner-Friendly**: Tooltips and explanations for all parameters

---

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Usage](#-usage)
- [Custom Fitness Functions (Docker Sandbox)](#-custom-fitness-functions-docker-sandbox)
- [Project Structure](#-project-structure)
- [API Documentation](#-api-documentation)
- [YAML Configuration](#-yaml-configuration)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🚀 Quick Start

**Requirements:** Python 3.11+, Node.js 18+, Docker (for custom fitness functions)

### 1. Install

```bash
git clone https://github.com/kThendral/OptimizeHub.git
cd OptimizeHub

# Backend
cd backend && python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Frontend
cd ../frontend && npm install
```

### 2. Configure Environment

**`backend/.env`:**
```
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
```

**`frontend/.env`:**
```
VITE_API_URL=http://localhost:8000
VITE_SUPABASE_URL=https://xxxxx.supabase.co
VITE_SUPABASE_ANON_KEY=your_anon_key
```

### 3. Run

> **Start backend first** — the frontend connects to it on load.

**Terminal 1 - Backend:**
```bash
cd backend && source venv/bin/activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend && npm run dev
```

Open **http://localhost:5173** (not `127.0.0.1:5173` — causes CORS issues).

---

## 📖 Usage

### Manual Input Mode

1. Navigate to `http://localhost:5173`
2. Click "Get Started" on the landing page
3. Select an algorithm (PSO or GA)
4. Configure problem definition:
   - Choose fitness function (sphere, rastrigin, etc.)
   - Set dimensions and bounds
   - Select objective (minimize/maximize)
5. Set algorithm-specific parameters
6. Click "Run Algorithm"
7. View results including best solution and convergence curve

### YAML Upload Mode

1. Click the "YAML Upload" tab
2. Either:
   - Upload a `.yaml` file
   - Paste YAML content directly
3. Click "Run from YAML"

**Sample YAML files** are available in `frontend/public/`:
- `sample_pso.yaml` - Particle Swarm Optimization example
- `sample_ga.yaml` - Genetic Algorithm example

---

## 🔒 Custom Fitness Functions (Docker Sandbox)

**NEW FEATURE**: Upload your own Python fitness functions that run in secure, isolated Docker containers!

### Quick Start

1. **Build Docker Image** (first time only):
   ```bash
   ./setup_docker_sandbox.sh
   ```

2. **Upload Custom Function**:
   - Click the **"Custom Fitness 🔒"** tab
   - Upload your fitness function (`.py` file)
   - Upload configuration (`.yaml` file)
   - Click "Run Optimization"

### Example Files

Test with provided examples in `examples/custom_fitness/`:
- `sphere_fitness.py` + `sphere_config.yaml` (PSO)
- `rosenbrock_fitness.py` + `rosenbrock_config.yaml` (DE)
- `custom_penalty_fitness.py` + `custom_penalty_config.yaml` (GA)

### Create Your Own

**Fitness Function Template:**
```python
import numpy as np

def fitness(x):
    """Your fitness function"""
    return np.sum(x**2)  # Minimize this value
```

**Requirements:**
- ✅ Function must be named `fitness`
- ✅ Must accept one parameter (numpy array)
- ✅ Must return a number
- ✅ Only `math` and `numpy` imports allowed
- ❌ No file I/O, network, or system calls

**Configuration Template:**
```yaml
algorithm: PSO  # PSO, GA, DE, SA, or ACOR
parameters:
  num_particles: 30
  max_iterations: 100
  w: 0.7
  c1: 1.5
  c2: 1.5
problem:
  dimensions: 10
  lower_bound: -5.0
  upper_bound: 5.0
```

### Security Features

- **Docker Isolation**: Code runs in isolated containers
- **AST Validation**: Blocks dangerous operations before execution
- **No Network**: Containers cannot access the internet
- **Read-Only**: Cannot modify the filesystem
- **Resource Limits**: 512MB RAM, 2 CPUs, 30-second timeout

### API Usage

```bash
curl -X POST http://localhost:8000/api/optimize/custom \
  -F "fitness_file=@your_fitness.py" \
  -F "config_file=@your_config.yaml"
```

📖 **Full Documentation**: See [DOCKER_SANDBOXING.md](DOCKER_SANDBOXING.md) for detailed setup, troubleshooting, and advanced usage.

---

## 🗂️ Project Structure

```
OptimizeHub/
├── backend/
│   ├── app/
│   │   ├── algorithms/          # Algorithm implementations
│   │   │   ├── base.py          # Base class for all algorithms
│   │   │   ├── particle_swarm.py
│   │   │   ├── genetic_algorithm.py
│   │   │   ├── differential_evolution.py
│   │   │   ├── simulated_annealing.py
│   │   │   └── ant_colony.py
│   │   ├── api/
│   │   │   └── routes.py        # API endpoints (includes /optimize/custom)
│   │   ├── core/
│   │   │   ├── utils.py         # Fitness functions
│   │   │   └── validation.py   # Input validation
│   │   ├── models/
│   │   │   ├── problem.py       # Pydantic models
│   │   │   └── result.py
│   │   ├── services/
│   │   │   ├── executor.py      # Algorithm execution service
│   │   │   ├── docker_executor.py  # 🔒 Docker container manager
│   │   │   └── comparison.py
│   │   ├── validators/
│   │   │   └── code_validator.py   # 🔒 AST security validator
│   │   ├── docker/
│   │   │   ├── Dockerfile.sandbox  # 🔒 Docker sandbox image
│   │   │   └── runner.py           # 🔒 Container execution script
│   │   ├── config.py            # Algorithm registry
│   │   └── main.py              # FastAPI app entry point
│   ├── tests/                   # Backend tests
│   ├── requirements.txt
│   └── requirements-dev.txt
│
├── frontend/
│   ├── public/
│   │   ├── sample_pso.yaml      # PSO example config
│   │   └── sample_ga.yaml       # GA example config
│   ├── src/
│   │   ├── api/
│   │   │   └── index.js         # API client
│   │   ├── components/
│   │   │   ├── forms/
│   │   │   │   ├── ProblemDefinitionForm.jsx  # Shared form
│   │   │   │   ├── PSOParametersForm.jsx      # PSO params
│   │   │   │   ├── GAParametersForm.jsx       # GA params
│   │   │   │   ├── DEParametersForm.jsx       # DE params
│   │   │   │   ├── SAParametersForm.jsx       # SA params
│   │   │   │   └── ACORParametersForm.jsx     # ACOR params
│   │   │   ├── AlgorithmSelector.jsx          # Main dashboard
│   │   │   ├── CustomFitnessUpload.jsx        # 🔒 Custom fitness UI
│   │   │   ├── CustomFitnessUpload.css        # 🔒 Styling
│   │   │   ├── LandingPage.jsx
│   │   │   └── ResultsDisplay.jsx
│   │   ├── styles/
│   │   │   └── theme.css        # Deep Violet color theme
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
├── examples/
│   └── custom_fitness/          # 🔒 Example custom fitness functions
│       ├── sphere_fitness.py
│       ├── sphere_config.yaml
│       ├── rosenbrock_fitness.py
│       ├── rosenbrock_config.yaml
│       ├── custom_penalty_fitness.py
│       ├── custom_penalty_config.yaml
│       └── README.md
│
├── DOCKER_SANDBOXING.md         # 🔒 Complete Docker sandbox guide
├── setup_docker_sandbox.sh      # 🔒 Automated setup script
├── LICENSE
└── README.md
```

🔒 = Docker sandboxing feature

---

## 🔌 API Documentation

### Base URL
```
http://localhost:8000/api
```

### Endpoints

#### `GET /api/algorithms`
List all available algorithms.

**Response:**
```json
{
  "algorithms": [
    {
      "name": "particle_swarm",
      "display_name": "Particle Swarm Optimization",
      "status": "available",
      "description": "..."
    }
  ]
}
```

#### `POST /api/optimize`
Run an optimization algorithm.

**Request Body:**
```json
{
  "algorithm": "particle_swarm",
  "problem": {
    "dimensions": 2,
    "bounds": [[-5, 5], [-5, 5]],
    "objective": "minimize",
    "fitness_function_name": "sphere"
  },
  "params": {
    "swarm_size": 30,
    "max_iterations": 50,
    "w": 0.7,
    "c1": 1.5,
    "c2": 1.5
  }
}
```

**Response:**
```json
{
  "status": "success",
  "algorithm": "particle_swarm",
  "best_solution": [0.001, -0.002],
  "best_fitness": 0.000005,
  "iterations_run": 50,
  "convergence_curve": [...]
}
```

#### `POST /api/optimize/custom` 🔒
Run optimization with custom fitness function (Docker sandbox).

**Request:**
- Content-Type: `multipart/form-data`
- `fitness_file`: Python file (.py)
- `config_file`: YAML configuration (.yaml)

**Response:**
```json
{
  "status": "success",
  "algorithm": "PSO",
  "best_solution": [0.001, -0.002],
  "best_fitness": 0.000005,
  "iterations": 100,
  "convergence_history": [...],
  "execution_time": 2.4,
  "message": "Optimization completed successfully using custom fitness function"
}
```

#### `GET /api/health`
Health check endpoint.

**Interactive API Docs:** `http://localhost:8000/docs`

---

## 📝 YAML Configuration

### Format

```yaml
algorithm: particle_swarm  # or genetic_algorithm

problem:
  dimensions: 2
  fitness_function: sphere  # sphere, rastrigin, rosenbrock, ackley, griewank
  lower_bound: -5
  upper_bound: 5
  objective: minimize       # or maximize

params:
  # For PSO:
  swarm_size: 30
  max_iterations: 50
  w: 0.7
  c1: 1.5
  c2: 1.5
  
  # For GA:
  # population_size: 50
  # max_iterations: 50
  # crossover_rate: 0.8
  # mutation_rate: 0.1
  # tournament_size: 3
```

### Examples

See `frontend/public/sample_pso.yaml` and `frontend/public/sample_ga.yaml` for complete examples.

---

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest tests/
```

Run specific test files:
```bash
pytest tests/test_api.py
pytest tests/test_algorithms/test_pso.py
```

### Frontend (Development)

```bash
cd frontend
npm run dev
```

---

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Pydantic** - Data validation
- **NumPy** - Numerical computations
- **Uvicorn** - ASGI server

### Frontend
- **React 19.1.1** - UI library
- **Vite 7.1.7** - Build tool
- **Tailwind CSS 4.0** - Styling
- **Custom theme system** - 60/30/10 color rule

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🐛 Troubleshooting

| Error | Fix |
|-------|-----|
| `ERR_CONNECTION_TIMED_OUT` | Start backend first, then refresh |
| `Failed to fetch algorithms` | Check backend is on port 8000; verify `VITE_API_URL` in `frontend/.env` |
| `SUPABASE_URL must be set` | Create `backend/.env` with your Supabase credentials |
| YAML parsing errors | Use 2-space indentation; ensure `algorithm`, `problem`, `params` sections exist |

> **Note:** Redis and Celery are only needed for async optimization tasks, not basic usage.

**API Docs:** http://localhost:8000/docs (when backend is running)

---

**Happy Optimizing! 🎯**
