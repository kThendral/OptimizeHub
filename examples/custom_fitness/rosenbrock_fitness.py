"""
Example: Rosenbrock Function
A non-convex function commonly used to test optimization algorithms.
Global minimum at x = [1, 1, ..., 1] with f(x) = 0
"""
import numpy as np

def fitness(x):
    """
    Rosenbrock function: f(x) = sum(100*(x_{i+1} - x_i^2)^2 + (1 - x_i)^2)

    Args:
        x: numpy array of input variables

    Returns:
        float: fitness value
    """
    return np.sum(100.0 * (x[1:] - x[:-1]**2)**2 + (1 - x[:-1])**2)
