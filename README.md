# OptimizeHub 🚀

**OptimizeHub** is a modern web platform for running optimization algorithms including Particle Swarm Optimization (PSO), Genetic Algorithm (GA), and more. Built with FastAPI (backend) and React + Vite (frontend).

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![React](https://img.shields.io/badge/react-19.1.1-blue.svg)

> **📖 New to OptimizeHub?** Read [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) for a comprehensive guide covering:
> - What this project does and why it exists
> - Complete feature list and implementation status
> - Future plans including AI/LLM integration for intelligent explanations
> - Use cases for academia (teaching & research) and businesses (logistics, resource management)
> - Technical specifications and roadmap

---

## ✨ Features

- **🎯 Multiple Algorithms**: PSO, GA (with SA, ACO, DE coming soon)
- **📊 5 Benchmark Functions**: Sphere, Rastrigin, Rosenbrock, Ackley, Griewank
- **🎨 Modern UI**: Clean interface with Deep Violet color scheme
- **📝 Dual Input Modes**: 
  - Manual form input with parameter explanations
  - YAML file upload for automation
- **🔧 Hybrid Component Architecture**: Shared + algorithm-specific forms
- **📈 Real-time Results**: View solutions, fitness, and convergence data
- **🔐 Input Validation**: Both frontend and backend validation
- **📚 Beginner-Friendly**: Tooltips and explanations for all parameters

---

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [API Documentation](#-api-documentation)
- [YAML Configuration](#-yaml-configuration)
- [Contributing](#-contributing)
- [License](#-license)

> **📖 Want a comprehensive overview?** Check out [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) for detailed information about completed features, future enhancements (including LLM integration), and use cases for academia and businesses.

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+**
- **Node.js 18+** and npm
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/kThendral/OptimizeHub.git
   cd OptimizeHub
   ```

2. **Set up the Backend**
   ```bash
   cd backend
   
   # Create virtual environment (optional but recommended)
   python -m venv venv
   
   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Set up the Frontend**
   ```bash
   cd ../frontend
   
   # Install dependencies
   npm install
   ```

### Running the Application

**Terminal 1 - Backend:**
```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: `http://localhost:8000`
API Documentation: `http://localhost:8000/docs`

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

Frontend will be available at: `http://localhost:5173`

**⚠️ Important:** Access the frontend via `http://localhost:5173` (NOT `127.0.0.1:5173`) to avoid CORS issues.

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

## 🗂️ Project Structure

```
OptimizeHub/
├── backend/
│   ├── app/
│   │   ├── algorithms/          # Algorithm implementations
│   │   │   ├── base.py          # Base class for all algorithms
│   │   │   ├── particle_swarm.py
│   │   │   ├── genetic_algorithm.py
│   │   │   └── ...
│   │   ├── api/
│   │   │   └── routes.py        # API endpoints
│   │   ├── core/
│   │   │   ├── utils.py         # Fitness functions
│   │   │   └── validation.py   # Input validation
│   │   ├── models/
│   │   │   ├── problem.py       # Pydantic models
│   │   │   └── result.py
│   │   ├── services/
│   │   │   ├── executor.py      # Algorithm execution service
│   │   │   └── comparison.py
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
│   │   │   │   └── GAParametersForm.jsx       # GA params
│   │   │   ├── AlgorithmSelector.jsx          # Main dashboard
│   │   │   ├── LandingPage.jsx
│   │   │   └── ResultsDisplay.jsx
│   │   ├── styles/
│   │   │   └── theme.css        # Deep Violet color theme
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
├── COMPONENT_STRUCTURE.md       # Frontend architecture docs
├── CLEANUP_AND_YAML_SUMMARY.md  # Recent changes documentation
├── TROUBLESHOOTING.md           # Common issues and fixes
├── LICENSE
└── README.md
```

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

## 🎨 Customization

### Change Color Scheme

Edit `frontend/src/styles/theme.css`:

```css
:root {
  --color-primary: #5B21B6;    /* Deep Violet */
  --color-secondary: #F3E8FF;  /* Light Purple */
  --color-accent: #00D4FF;     /* Cyan */
}
```

### Add New Algorithm

1. Create algorithm class in `backend/app/algorithms/`
2. Inherit from `OptimizationAlgorithm`
3. Implement `initialize()` and `optimize()`
4. Register in `backend/app/config.py`
5. Create parameter form in `frontend/src/components/forms/`
6. Add conditional rendering in `AlgorithmSelector.jsx`

See `COMPONENT_STRUCTURE.md` for detailed instructions.

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

### "Failed to fetch" error

- ✅ Make sure backend is running on port 8000
- ✅ Access frontend via `http://localhost:5173` (NOT `127.0.0.1:5173`)
- ✅ Check browser console for detailed errors

### YAML parsing errors

- ✅ Ensure proper indentation (2 spaces)
- ✅ Check that `algorithm`, `problem`, and `params` sections exist
- ✅ Verify parameter names match backend expectations

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for more details.

---

## 📚 Documentation

- **API Documentation**: http://localhost:8000/docs (when backend is running)
- **[FEATURE_SUMMARY.md](FEATURE_SUMMARY.md)** - Quick reference guide (start here!)
- **[PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)** - Comprehensive project guide with future plans
- **Component Structure**: [COMPONENT_STRUCTURE.md](frontend/COMPONENT_STRUCTURE.md)
- **Recent Changes**: [CLEANUP_AND_YAML_SUMMARY.md](CLEANUP_AND_YAML_SUMMARY.md)
- **Troubleshooting**: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

## 🙏 Acknowledgments

- Inspired by classic optimization algorithm benchmarks
- Built with modern web technologies
- Deep Violet color scheme for visual appeal

---

**Happy Optimizing! 🎯**