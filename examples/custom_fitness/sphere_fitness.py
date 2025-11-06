"""
Example: Sphere Function
A simple convex optimization problem.
Global minimum at x = [0, 0, ..., 0] with f(x) = 0
"""
import numpy as np

def fitness(x):
    """
    Sphere function: f(x) = sum(x_i^2)

    Args:
        x: numpy array of input variables

    Returns:
        float: fitness value
    """
    return np.sum(x**2)
