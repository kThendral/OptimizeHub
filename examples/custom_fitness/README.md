# Custom Fitness Function Examples

This directory contains example fitness functions and configurations for testing the Docker-based sandboxing feature.

## Files

### 1. Sphere Function (Simple)
- **Fitness**: `sphere_fitness.py`
- **Config**: `sphere_config.yaml`
- **Algorithm**: PSO (Particle Swarm Optimization)
- **Description**: Simple convex function, good for testing basic functionality
- **Expected Result**: Should converge to ~0.0 at x = [0, 0, ..., 0]

### 2. Rosenbrock Function (Medium)
- **Fitness**: `rosenbrock_fitness.py`
- **Config**: `rosenbrock_config.yaml`
- **Algorithm**: DE (Differential Evolution)
- **Description**: Classic non-convex optimization benchmark
- **Expected Result**: Should converge to ~0.0 at x = [1, 1, ..., 1]

### 3. Custom Penalty Function (Advanced)
- **Fitness**: `custom_penalty_fitness.py`
- **Config**: `custom_penalty_config.yaml`
- **Algorithm**: GA (Genetic Algorithm)
- **Description**: Custom fitness combining sphere with L1 penalty
- **Expected Result**: Should converge to values near 0.0

## Usage

### Via Frontend
1. Navigate to the "Custom Fitness" tab
2. Upload the `.py` fitness function file
3. Upload the corresponding `.yaml` config file
4. Click "Run Optimization"
5. View results and convergence chart

### Via API (curl)
```bash
curl -X POST http://localhost:8000/api/optimize/custom \
  -F "fitness_file=@sphere_fitness.py" \
  -F "config_file=@sphere_config.yaml"
```

### Via API (Python)
```python
import requests

files = {
    'fitness_file': open('sphere_fitness.py', 'rb'),
    'config_file': open('sphere_config.yaml', 'rb')
}

response = requests.post('http://localhost:8000/api/optimize/custom', files=files)
print(response.json())
```

## Creating Your Own Fitness Function

### Requirements
1. **Function name must be `fitness`**
2. **Must accept one parameter** (numpy array)
3. **Must return a numeric value** (float or int)
4. **Only allowed imports**: `math`, `numpy` (imported as `np`)

### Example Template
```python
import numpy as np

def fitness(x):
    """
    Your fitness function description.

    Args:
        x: numpy array of input variables

    Returns:
        float: fitness value to minimize
    """
    # Your calculation here
    return np.sum(x**2)  # Example: sphere function
```

### Security Restrictions
The following operations are **NOT allowed** (sandbox will reject):
- File I/O (`open`, `read`, `write`)
- Network operations (`socket`, `urllib`, `requests`)
- System calls (`os.system`, `subprocess`)
- Eval/exec operations
- Importing unauthorized modules

## Configuration Format

### YAML Structure
```yaml
algorithm: PSO  # PSO, GA, DE, SA, or ACOR
parameters:
  # Algorithm-specific parameters
  num_particles: 30      # For PSO
  max_iterations: 100
  w: 0.7
  c1: 1.5
  c2: 1.5
problem:
  dimensions: 10          # Problem dimensionality
  lower_bound: -5.0       # Lower bound for all dimensions
  upper_bound: 5.0        # Upper bound for all dimensions
```

### Algorithm Parameters

#### PSO (Particle Swarm Optimization)
```yaml
parameters:
  num_particles: 30
  max_iterations: 100
  w: 0.7    # Inertia weight
  c1: 1.5   # Cognitive parameter
  c2: 1.5   # Social parameter
```

#### GA (Genetic Algorithm)
```yaml
parameters:
  population_size: 50
  max_generations: 100
  mutation_rate: 0.1
  crossover_rate: 0.8
```

#### DE (Differential Evolution)
```yaml
parameters:
  population_size: 50
  max_generations: 100
  F: 0.8    # Differential weight
  CR: 0.9   # Crossover probability
```

#### SA (Simulated Annealing)
```yaml
parameters:
  max_iterations: 1000
  initial_temperature: 100.0
  cooling_rate: 0.95
```

#### ACOR (Ant Colony Optimization for Continuous Domains)
```yaml
parameters:
  num_ants: 50
  max_iterations: 100
  archive_size: 50
  q: 0.5
  xi: 0.85
```

## Resource Limits

- **Timeout**: 30 seconds
- **Memory**: 512 MB
- **CPU**: 2 cores
- **Max file size**: 1 MB each

## Troubleshooting

### Error: "Fitness function must be named 'fitness'"
- Ensure your function is named exactly `fitness` (lowercase)

### Error: "Import not allowed"
- Only `math` and `numpy` are allowed
- Remove any other import statements

### Error: "Timeout"
- Reduce `max_iterations` in config
- Reduce `dimensions` in problem
- Simplify your fitness function

### Error: "Container failed"
- Check syntax errors in your Python code
- Ensure fitness function returns a number
- Test locally first: `python -c "from your_file import fitness; import numpy as np; print(fitness(np.zeros(5)))"`

## Testing Locally

Before uploading, test your fitness function locally:

```python
import numpy as np
from your_fitness_file import fitness

# Test with sample input
test_input = np.array([1.0, 2.0, 3.0])
result = fitness(test_input)
print(f"Fitness value: {result}")
print(f"Type: {type(result)}")
```

Expected output:
```
Fitness value: 14.0
Type: <class 'numpy.float64'>
```
