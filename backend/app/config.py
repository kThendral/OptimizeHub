"""
Configuration settings and algorithm registry for OptimizeHub.
"""
from typing import Dict, Any


# ==============================================================================
# Platform Constraints
# ==============================================================================

MAX_DIMENSIONS = 50
"""Maximum number of dimensions allowed in optimization problems."""

MAX_ITERATIONS = 100
"""Maximum number of iterations allowed per algorithm run."""

EXECUTION_TIMEOUT = 30
"""Maximum execution time in seconds."""


# ==============================================================================
# Algorithm Registry
# ==============================================================================

ALGORITHM_REGISTRY: Dict[str, Dict[str, Any]] = {
    'particle_swarm': {
        'status': 'available',
        'display_name': 'Particle Swarm Optimization',
        'class_name': 'ParticleSwarmOptimization',
        'module': 'app.algorithms.particle_swarm',
        'description': (
            'Bio-inspired algorithm simulating social behavior of birds flocking. '
            'Particles move through the search space influenced by their own best '
            'position and the swarm\'s global best position.'
        ),
        'use_cases': [
            'Continuous optimization',
            'Non-convex problems',
            'Multi-modal landscapes'
        ],
        'default_params': {
            'swarm_size': 30,
            'max_iterations': 50,
            'w': 0.7,
            'c1': 1.5,
            'c2': 1.5
        },
        'parameter_info': {
            'swarm_size': {
                'type': 'int',
                'min': 10,
                'description': 'Number of particles in the swarm',
                'recommendation': '20-50 for most problems'
            },
            'max_iterations': {
                'type': 'int',
                'min': 1,
                'max': 100,
                'description': 'Maximum number of iterations'
            },
            'w': {
                'type': 'float',
                'description': 'Inertia weight (controls exploration vs exploitation)',
                'recommendation': '0.4-0.9 for good convergence'
            },
            'c1': {
                'type': 'float',
                'description': 'Cognitive coefficient (attraction to personal best)',
                'recommendation': '1.0-2.0'
            },
            'c2': {
                'type': 'float',
                'description': 'Social coefficient (attraction to global best)',
                'recommendation': '1.0-2.0'
            }
        }
    },

    'genetic_algorithm': {
        'status': 'available',  
        'display_name': 'Genetic Algorithm',
        'class_name': 'GeneticAlgorithm',
        'module': 'app.algorithms.genetic_algorithm',
        'description': (
            'Evolutionary algorithm inspired by natural selection. '
            'Uses selection, crossover, and mutation operators to evolve '
            'a population of candidate solutions towards better fitness.'
        ),
        'use_cases': [
            'Discrete and continuous optimization',
            'Combinatorial problems',
            'Multi-objective optimization'
        ],
        'default_params': {
            'population_size': 50,
            'max_iterations': 50,
            'crossover_rate': 0.8,
            'mutation_rate': 0.1,
            'tournament_size': 3
        },
        'parameter_info': {
            'population_size': {
                'type': 'int',
                'min': 10,
                'description': 'Number of individuals in the population',
                'recommendation': '30-100 for most problems'
            },
            'max_iterations': {
                'type': 'int',
                'min': 1,
                'max': 100,
                'description': 'Maximum number of generations'
            },
            'crossover_rate': {
                'type': 'float',
                'min': 0.0,
                'max': 1.0,
                'description': 'Probability of crossover between parents',
                'recommendation': '0.6-0.9'
            },
            'mutation_rate': {
                'type': 'float',
                'min': 0.0,
                'max': 1.0,
                'description': 'Probability of random mutation',
                'recommendation': '0.01-0.1'
            },
            'tournament_size': {
                'type': 'int',
                'min': 2,
                'description': 'Number of individuals competing in tournament selection',
                'recommendation': '2-5'
            }
        }
    },

    'differential_evolution': {
        'status': 'coming_soon',
        'display_name': 'Differential Evolution',
        'class_name': 'DifferentialEvolution',
        'module': 'app.algorithms.differential_evolution',
        'description': (
            'Population-based optimization algorithm that creates new candidates '
            'by combining existing solutions using vector differences. '
            'Particularly effective for continuous optimization problems.'
        ),
        'use_cases': [
            'Continuous optimization',
            'Global optimization',
            'Non-differentiable functions'
        ],
        'default_params': {
            'population_size': 50,
            'max_iterations': 50,
            'F': 0.8,  # Differential weight
            'CR': 0.9  # Crossover probability
        },
        'parameter_info': {
            'population_size': {
                'type': 'int',
                'min': 10,
                'description': 'Number of individuals in the population',
                'recommendation': '10*dimensions'
            },
            'max_iterations': {
                'type': 'int',
                'min': 1,
                'max': 100,
                'description': 'Maximum number of generations'
            },
            'F': {
                'type': 'float',
                'min': 0.0,
                'max': 2.0,
                'description': 'Differential weight (scaling factor)',
                'recommendation': '0.5-1.0'
            },
            'CR': {
                'type': 'float',
                'min': 0.0,
                'max': 1.0,
                'description': 'Crossover probability',
                'recommendation': '0.7-0.9'
            }
        }
    },

    'simulated_annealing': {
        'status': 'coming_soon',
        'display_name': 'Simulated Annealing',
        'class_name': 'SimulatedAnnealing',
        'module': 'app.algorithms.simulated_annealing',
        'description': (
            'Probabilistic optimization technique inspired by metallurgy annealing process. '
            'Accepts worse solutions with decreasing probability to escape local minima.'
        ),
        'use_cases': [
            'Discrete optimization',
            'Combinatorial problems',
            'Avoiding local minima'
        ],
        'default_params': {
            'initial_temperature': 100.0,
            'cooling_rate': 0.95,
            'max_iterations': 50,
            'min_temperature': 0.01
        },
        'parameter_info': {
            'initial_temperature': {
                'type': 'float',
                'min': 0.1,
                'description': 'Starting temperature (higher = more exploration)',
                'recommendation': '10-1000 depending on problem scale'
            },
            'cooling_rate': {
                'type': 'float',
                'min': 0.0,
                'max': 1.0,
                'description': 'Rate at which temperature decreases',
                'recommendation': '0.9-0.99'
            },
            'max_iterations': {
                'type': 'int',
                'min': 1,
                'max': 100,
                'description': 'Maximum number of iterations'
            },
            'min_temperature': {
                'type': 'float',
                'min': 0.0,
                'description': 'Temperature at which to stop',
                'recommendation': '0.001-0.1'
            }
        }
    },

    'ant_colony': {
        'status': 'coming_soon',
        'display_name': 'Ant Colony Optimization',
        'class_name': 'AntColonyOptimization',
        'module': 'app.algorithms.ant_colony',
        'description': (
            'Inspired by foraging behavior of ants. Ants deposit pheromones '
            'on paths, and subsequent ants probabilistically choose paths with '
            'stronger pheromone trails. Excellent for path and graph problems.'
        ),
        'use_cases': [
            'Traveling salesman problem',
            'Vehicle routing',
            'Network routing'
        ],
        'default_params': {
            'num_ants': 30,
            'max_iterations': 50,
            'alpha': 1.0,  # Pheromone importance
            'beta': 2.0,   # Heuristic importance
            'evaporation_rate': 0.5,
            'pheromone_deposit': 1.0
        },
        'parameter_info': {
            'num_ants': {
                'type': 'int',
                'min': 5,
                'description': 'Number of ants in the colony',
                'recommendation': '10-50'
            },
            'max_iterations': {
                'type': 'int',
                'min': 1,
                'max': 100,
                'description': 'Maximum number of iterations'
            },
            'alpha': {
                'type': 'float',
                'min': 0.0,
                'description': 'Pheromone importance factor',
                'recommendation': '1.0'
            },
            'beta': {
                'type': 'float',
                'min': 0.0,
                'description': 'Heuristic information importance',
                'recommendation': '2.0-5.0'
            },
            'evaporation_rate': {
                'type': 'float',
                'min': 0.0,
                'max': 1.0,
                'description': 'Rate at which pheromone evaporates',
                'recommendation': '0.1-0.5'
            }
        }
    }
}


# ==============================================================================
# Helper Functions
# ==============================================================================

def get_available_algorithms() -> list:
    """Get list of algorithm names that are currently available."""
    return [
        name for name, info in ALGORITHM_REGISTRY.items()
        if info['status'] == 'available'
    ]


def get_coming_soon_algorithms() -> list:
    """Get list of algorithm names that are in development."""
    return [
        name for name, info in ALGORITHM_REGISTRY.items()
        if info['status'] == 'coming_soon'
    ]


def is_algorithm_available(algorithm_name: str) -> bool:
    """Check if an algorithm is available for use."""
    return (
        algorithm_name in ALGORITHM_REGISTRY and
        ALGORITHM_REGISTRY[algorithm_name]['status'] == 'available'
    )


def get_algorithm_info(algorithm_name: str) -> Dict[str, Any]:
    """Get information about a specific algorithm."""
    if algorithm_name not in ALGORITHM_REGISTRY:
        raise ValueError(f"Unknown algorithm: {algorithm_name}")
    return ALGORITHM_REGISTRY[algorithm_name]
