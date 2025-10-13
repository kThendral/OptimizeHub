"""
Optimization Algorithms Package

This package contains implementations of various metaheuristic optimization algorithms.
All algorithms inherit from the OptimizationAlgorithm base class and follow a consistent
interface for problem definition, initialization, and optimization.

Available Algorithms:
    - ParticleSwarmOptimization: Bio-inspired swarm intelligence algorithm
    - GeneticAlgorithm: Evolutionary algorithm with selection, crossover, and mutation
    - DifferentialEvolution: Population-based algorithm using vector differences
    - AntColonyOptimization: ACOR algorithm for continuous optimization using archive-based sampling

Usage:
    from app.algorithms import ParticleSwarmOptimization

    problem = {
        'dimensions': 2,
        'bounds': [(-5, 5), (-5, 5)],
        'objective': 'minimize',
        'fitness_function': my_function
    }

    params = {'swarm_size': 30, 'max_iterations': 50}

    pso = ParticleSwarmOptimization(problem, params)
    pso.initialize()
    pso.optimize()
    results = pso.get_results()
"""

from app.algorithms.base import OptimizationAlgorithm
from app.algorithms.particle_swarm import ParticleSwarmOptimization
from app.algorithms.genetic_algorithm import GeneticAlgorithm
from app.algorithms.differential_evolution import DifferentialEvolution
from app.algorithms.ant_colony import AntColonyOptimization

__all__ = [
    'OptimizationAlgorithm',
    'ParticleSwarmOptimization',
    'GeneticAlgorithm',
    'DifferentialEvolution',
    'AntColonyOptimization',
]
