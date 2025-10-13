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
        'characteristics': {
            'speed': 'fast',
            'accuracy': 'excellent',
            'speed_rank': 4,  # out of 5 stars
            'accuracy_rank': 4,  # out of 5 stars
            'typical_runtime': '0.025-0.030s per iteration',
            'best_for': 'Quick optimization with excellent accuracy, smooth continuous functions'
        },
        'use_cases': [
            'Continuous optimization',
            'Non-convex problems',
            'Real-time parameter tuning',
            'Smooth function optimization'
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
        'characteristics': {
            'speed': 'fastest',
            'accuracy': 'good',
            'speed_rank': 5,  # out of 5 stars - FASTEST
            'accuracy_rank': 3,  # out of 5 stars
            'typical_runtime': '0.012-0.015s per iteration',
            'best_for': 'Robust optimization, excels at multi-modal and complex discrete problems'
        },
        'use_cases': [
            'Multi-modal optimization',
            'Discrete and continuous optimization',
            'Combinatorial problems',
            'Complex search spaces with many local optima'
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
        'status': 'available',
        'display_name': 'Differential Evolution',
        'class_name': 'DifferentialEvolution',
        'module': 'app.algorithms.differential_evolution',
        'description': (
            'Population-based optimization algorithm that creates new candidates '
            'by combining existing solutions using vector differences. '
            'Particularly effective for continuous optimization problems.'
        ),
        'characteristics': {
            'speed': 'fast',
            'accuracy': 'very good',
            'speed_rank': 4,  # out of 5 stars
            'accuracy_rank': 4,  # out of 5 stars
            'typical_runtime': '0.020-0.030s per iteration',
            'best_for': 'Global optimization, non-differentiable continuous functions'
        },
        'use_cases': [
            'Continuous optimization',
            'Global optimization',
            'Non-differentiable functions',
            'Numerical optimization'
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
        'status': 'available',
        'display_name': 'Ant Colony Optimization',
        'class_name': 'AntColonyOptimization',
        'module': 'app.algorithms.ant_colony',
        'description': (
            'Continuous ACO (ACOR) using solution archives and Gaussian sampling. '
            'Ants construct solutions by sampling from a weighted archive of good solutions. '
            'Achieves machine-precision accuracy on smooth functions.'
        ),
        'characteristics': {
            'speed': 'fast',
            'accuracy': 'excellent',
            'speed_rank': 5,  # out of 5 stars - Very fast
            'accuracy_rank': 5,  # out of 5 stars - Best accuracy
            'typical_runtime': '0.015-0.020s per iteration',
            'best_for': 'High-precision optimization on smooth functions, engineering design requiring exact solutions'
        },
        'use_cases': [
            'High-precision continuous optimization',
            'Engineering design optimization',
            'Smooth function optimization',
            'Scientific computing'
        ],
        'default_params': {
            'colony_size': 30,
            'max_iterations': 50,
            'archive_size': 10,
            'q': 0.01,
            'xi': 0.85
        },
        'parameter_info': {
            'colony_size': {
                'type': 'int',
                'min': 5,
                'description': 'Number of ants generating solutions per iteration',
                'recommendation': '20-50 for most problems'
            },
            'max_iterations': {
                'type': 'int',
                'min': 1,
                'max': 100,
                'description': 'Maximum number of iterations'
            },
            'archive_size': {
                'type': 'int',
                'min': 1,
                'description': 'Size of solution archive (pheromone memory)',
                'recommendation': '10-20, must be ≤ colony_size'
            },
            'q': {
                'type': 'float',
                'min': 0.0,
                'description': 'Locality of search parameter (intensification)',
                'recommendation': '0.001-0.1, lower = more intensification'
            },
            'xi': {
                'type': 'float',
                'min': 0.0,
                'max': 1.0,
                'description': 'Speed of convergence parameter',
                'recommendation': '0.7-0.95, higher = faster convergence'
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
