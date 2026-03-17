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


def ackley(x: Sequence[float]) -> float:
    """Ackley function: multimodal with nearly flat outer region. Minimum at 0."""
    x = np.asarray(x, dtype=float)
    n = x.size
    sum_sq = np.sum(x * x)
    sum_cos = np.sum(np.cos(2 * np.pi * x))
    return float(-20 * np.exp(-0.2 * np.sqrt(sum_sq / n)) - np.exp(sum_cos / n) + 20 + np.e)


def rosenbrock(x: Sequence[float]) -> float:
    """Rosenbrock function: narrow valley. Minimum at (1, 1, ..., 1)."""
    x = np.asarray(x, dtype=float)
    result = 0.0
    for i in range(len(x) - 1):
        result += 100 * (x[i + 1] - x[i] ** 2) ** 2 + (1 - x[i]) ** 2
    return float(result)


def griewank(x: Sequence[float]) -> float:
    """Griewank function: many local minima. Minimum at 0."""
    x = np.asarray(x, dtype=float)
    sum_sq = np.sum(x * x) / 4000
    prod_cos = np.prod(np.cos(x / np.sqrt(np.arange(1, len(x) + 1))))
    return float(sum_sq - prod_cos + 1)