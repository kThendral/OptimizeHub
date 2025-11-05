"""
Example: Custom Fitness with Penalty
A custom function that combines sphere function with a penalty term.
Demonstrates how to create your own fitness function.
"""
import numpy as np

def fitness(x):
    """
    Custom fitness: Sphere function with L1 penalty

    f(x) = sum(x_i^2) + 0.1 * sum(|x_i|)

    This adds a penalty for values far from zero.

    Args:
        x: numpy array of input variables

    Returns:
        float: fitness value
    """
    sphere_term = np.sum(x**2)
    penalty_term = 0.1 * np.sum(np.abs(x))
    return sphere_term + penalty_term
