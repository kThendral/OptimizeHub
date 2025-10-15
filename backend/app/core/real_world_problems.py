"""
Real-world optimization problem definitions.
These can be solved using optimization algorithms with custom fitness functions.
"""
import numpy as np
from typing import List, Tuple, Dict, Any, Callable


# ==============================================================================
# Traveling Salesman Problem (TSP) / Shortest Path
# ==============================================================================

def create_tsp_fitness(cities: List[Tuple[float, float]]) -> Callable:
    """
    Create a fitness function for the Traveling Salesman Problem.
    
    Args:
        cities: List of (x, y) coordinates for each city
        
    Returns:
        Fitness function that calculates total tour distance
        
    Example:
        cities = [(0, 0), (1, 2), (3, 1), (5, 3)]
        fitness_fn = create_tsp_fitness(cities)
        # Solution is a permutation: [0, 2, 1, 3] means visit in that order
    """
    n_cities = len(cities)
    
    def tsp_fitness(solution: np.ndarray) -> float:
        """Calculate total distance of tour."""
        # Convert continuous values to permutation (rankings)
        tour = np.argsort(solution)
        
        total_distance = 0.0
        for i in range(n_cities):
            city_a = cities[tour[i]]
            city_b = cities[tour[(i + 1) % n_cities]]  # Return to start
            distance = np.sqrt((city_a[0] - city_b[0])**2 + (city_a[1] - city_b[1])**2)
            total_distance += distance
            
        return total_distance
    
    return tsp_fitness


# ==============================================================================
# Knapsack Problem
# ==============================================================================

def create_knapsack_fitness(
    weights: List[float],
    values: List[float],
    capacity: float,
    penalty_factor: float = 1000.0
) -> Callable:
    """
    Create a fitness function for the 0/1 Knapsack Problem.
    
    Args:
        weights: Weight of each item
        values: Value of each item
        capacity: Maximum weight capacity of knapsack
        penalty_factor: Penalty for exceeding capacity
        
    Returns:
        Fitness function (we want to MINIMIZE negative value)
        
    Example:
        weights = [2, 3, 4, 5]
        values = [3, 4, 5, 6]
        capacity = 8
        fitness_fn = create_knapsack_fitness(weights, values, capacity)
        # Solution in [0, 1] for each item - threshold at 0.5
    """
    n_items = len(weights)
    
    def knapsack_fitness(solution: np.ndarray) -> float:
        """
        Calculate negative value (since we minimize).
        Returns: -total_value if valid, penalty if over capacity
        """
        # Convert continuous [0,1] to binary [0 or 1]
        selected = (solution > 0.5).astype(int)
        
        total_weight = np.sum(selected * weights)
        total_value = np.sum(selected * values)
        
        # Penalty if over capacity
        if total_weight > capacity:
            over_capacity = total_weight - capacity
            return penalty_factor * over_capacity  # High fitness = bad
        
        # Return negative value (minimize)
        return -total_value
    
    return knapsack_fitness


# ==============================================================================
# Job Scheduling Problem
# ==============================================================================
# NOTE: This problem is implemented but not yet integrated into the UI.
# Planned for integration after Celery/Redis queuing system is added.
# Backend functionality is complete and tested.

def create_scheduling_fitness(
    processing_times: List[float],
    n_machines: int = 1
) -> Callable:
    """
    Create a fitness function for Job Scheduling (minimize makespan).
    
    Args:
        processing_times: Time required for each job
        n_machines: Number of machines available
        
    Returns:
        Fitness function that minimizes makespan (completion time)
        
    Example:
        processing_times = [3, 2, 4, 1, 5]
        fitness_fn = create_scheduling_fitness(processing_times, n_machines=2)
    """
    n_jobs = len(processing_times)
    
    def scheduling_fitness(solution: np.ndarray) -> float:
        """Calculate makespan (max completion time across machines)."""
        # Convert to job order
        job_order = np.argsort(solution)
        
        # Assign jobs to machines in order
        machine_times = np.zeros(n_machines)
        
        for job_idx in job_order:
            # Assign to machine with least load
            min_machine = np.argmin(machine_times)
            machine_times[min_machine] += processing_times[job_idx]
        
        # Makespan is the maximum time
        return float(np.max(machine_times))
    
    return scheduling_fitness


# ==============================================================================
# Feature Selection Problem
# ==============================================================================
# NOTE: This problem is implemented but not yet integrated into the UI.
# Planned for integration after Celery/Redis queuing system is added.
# Backend functionality is complete and tested.

def create_feature_selection_fitness(
    X_train: np.ndarray,
    y_train: np.ndarray,
    model_evaluator: Callable,
    alpha: float = 0.01
) -> Callable:
    """
    Create a fitness function for feature selection.
    
    Args:
        X_train: Training features (n_samples, n_features)
        y_train: Training labels
        model_evaluator: Function that returns model error given (X, y)
        alpha: Penalty for number of features selected
        
    Returns:
        Fitness function that balances accuracy and feature count
    """
    n_features = X_train.shape[1]
    
    def feature_selection_fitness(solution: np.ndarray) -> float:
        """
        Returns: model_error + alpha * n_features_selected
        """
        # Convert to binary feature mask
        selected = (solution > 0.5).astype(bool)
        
        # Need at least one feature
        if not np.any(selected):
            return 1000.0  # High penalty
        
        # Evaluate model with selected features
        X_selected = X_train[:, selected]
        error = model_evaluator(X_selected, y_train)
        
        # Add penalty for number of features
        n_selected = np.sum(selected)
        fitness = error + alpha * (n_selected / n_features)
        
        return float(fitness)
    
    return feature_selection_fitness


# ==============================================================================
# Portfolio Optimization
# ==============================================================================
# NOTE: This problem is implemented but not yet integrated into the UI.
# Planned for integration after Celery/Redis queuing system is added.
# Backend functionality is complete and tested.

def create_portfolio_fitness(
    returns: np.ndarray,
    covariance: np.ndarray,
    risk_aversion: float = 0.5
) -> Callable:
    """
    Create a fitness function for portfolio optimization.
    
    Args:
        returns: Expected returns for each asset
        covariance: Covariance matrix of returns
        risk_aversion: Trade-off between return and risk (0-1)
        
    Returns:
        Fitness function (minimize negative Sharpe-like ratio)
        
    Example:
        returns = np.array([0.05, 0.07, 0.12])
        covariance = np.array([[0.01, 0.001, 0.002],
                               [0.001, 0.02, 0.003],
                               [0.002, 0.003, 0.03]])
        fitness_fn = create_portfolio_fitness(returns, covariance)
        # Solution: weights for each asset (normalized to sum to 1)
    """
    n_assets = len(returns)
    
    def portfolio_fitness(solution: np.ndarray) -> float:
        """
        Calculate portfolio performance.
        Returns: negative (expected_return - risk_aversion * variance)
        """
        # Normalize weights to sum to 1
        weights = np.abs(solution)
        weights = weights / np.sum(weights) if np.sum(weights) > 0 else np.ones(n_assets) / n_assets
        
        # Expected return
        portfolio_return = np.dot(weights, returns)
        
        # Portfolio variance
        portfolio_variance = np.dot(weights, np.dot(covariance, weights))
        
        # Objective: maximize return - risk_aversion * variance
        # We minimize, so return negative
        objective = portfolio_return - risk_aversion * portfolio_variance
        
        return -objective
    
    return portfolio_fitness


# ==============================================================================
# Problem Registry
# ==============================================================================

PROBLEM_TYPES = {
    'tsp': {
        'name': 'Traveling Salesman Problem',
        'description': 'Find shortest route visiting all cities',
        'creator': create_tsp_fitness,
        'example_params': {
            'cities': [(0, 0), (1, 2), (3, 1), (5, 3), (2, 4)]
        }
    },
    'knapsack': {
        'name': '0/1 Knapsack Problem',
        'description': 'Maximize value without exceeding weight capacity',
        'creator': create_knapsack_fitness,
        'example_params': {
            'weights': [2, 3, 4, 5, 1],
            'values': [3, 4, 5, 6, 2],
            'capacity': 10
        }
    },
    'scheduling': {
        'name': 'Job Scheduling Problem',
        'description': 'Minimize completion time across machines',
        'creator': create_scheduling_fitness,
        'example_params': {
            'processing_times': [3, 2, 4, 1, 5, 3],
            'n_machines': 2
        }
    }
}


def get_problem_example(problem_type: str) -> Dict[str, Any]:
    """Get example configuration for a real-world problem."""
    if problem_type not in PROBLEM_TYPES:
        raise ValueError(f"Unknown problem type: {problem_type}")
    
    return PROBLEM_TYPES[problem_type]
