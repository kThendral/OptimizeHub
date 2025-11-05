# Simple numeric benchmark functions that the algorithms can call by name.
# The Celery task will map problem['fitness_function'] (a string) to a callable here.

import numpy as np
from typing import Sequence

def sphere(x: Sequence[float]) -> float:
    """Sphere function: sum(x_i^2). Minimum at 0."""
    x = np.asarray(x, dtype=float)
    return float(np.sum(x * x))

def rastrigin(x: Sequence[float]) -> float:
    """Rastrigin function (common benchmark)."""
    x = np.asarray(x, dtype=float)
    A = 10.0
    n = x.size
    return float(A * n + np.sum(x * x - A * np.cos(2 * np.pi * x)))