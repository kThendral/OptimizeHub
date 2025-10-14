"""
Utility functions for decoding optimization solutions into human-readable formats.
Particularly useful for real-world problems like TSP and Knapsack.
"""
import numpy as np
from typing import List, Dict, Any


def decode_knapsack_solution(
    solution: List[float],
    items: List[Dict[str, Any]],
    capacity: float
) -> Dict[str, Any]:
    """
    Decode a knapsack problem solution.
    
    Args:
        solution: Binary-encoded solution (values in [0, 1])
        items: List of items with {name, weight, value}
        capacity: Maximum capacity
        
    Returns:
        Dictionary with selected items and statistics
    """
    # Convert to binary (threshold at 0.5)
    selected_indices = [i for i, val in enumerate(solution) if val > 0.5]
    
    # Get selected items
    selected_items = []
    total_weight = 0.0
    total_value = 0.0
    
    for idx in selected_indices:
        if idx < len(items):
            item = items[idx]
            selected_items.append({
                'name': item['name'],
                'weight': item['weight'],
                'value': item['value']
            })
            total_weight += item['weight']
            total_value += item['value']
    
    return {
        'selected_items': selected_items,
        'total_items_selected': len(selected_items),
        'total_weight': round(total_weight, 2),
        'total_value': round(total_value, 2),
        'capacity': capacity,
        'weight_utilization': round((total_weight / capacity * 100) if capacity > 0 else 0, 2),
        'within_capacity': total_weight <= capacity
    }


def decode_tsp_solution(
    solution: List[float],
    cities: List[Dict[str, Any]],
    total_distance: float
) -> Dict[str, Any]:
    """
    Decode a TSP solution.
    
    Args:
        solution: Continuous values to be ranked
        cities: List of cities with {name, x, y}
        total_distance: Total tour distance (fitness value)
        
    Returns:
        Dictionary with route and statistics
    """
    # Convert to tour order (rank solution values)
    tour_indices = np.argsort(solution).tolist()
    
    # Build route
    route = []
    for idx in tour_indices:
        if idx < len(cities):
            city = cities[idx]
            route.append({
                'name': city['name'],
                'x': city['x'],
                'y': city['y']
            })
    
    # Calculate individual segment distances
    segments = []
    for i in range(len(route)):
        city_a = route[i]
        city_b = route[(i + 1) % len(route)]  # Wrap to start
        
        distance = np.sqrt(
            (city_a['x'] - city_b['x'])**2 + 
            (city_a['y'] - city_b['y'])**2
        )
        
        segments.append({
            'from': city_a['name'],
            'to': city_b['name'],
            'distance': round(distance, 2)
        })
    
    return {
        'route': route,
        'route_order': [city['name'] for city in route],
        'segments': segments,
        'total_cities': len(route),
        'total_distance': round(total_distance, 2),
        'average_segment_distance': round(total_distance / len(route), 2) if route else 0
    }


def add_problem_context_to_result(
    result: Dict[str, Any],
    problem: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Add problem-specific context to optimization result.
    
    Args:
        result: Raw optimization result
        problem: Problem definition
        
    Returns:
        Enhanced result with decoded solutions
    """
    problem_type = problem.get('problem_type')
    
    if problem_type == 'knapsack' and result.get('best_solution'):
        # Decode knapsack solution
        decoded = decode_knapsack_solution(
            solution=result['best_solution'],
            items=problem.get('items', []),
            capacity=problem.get('capacity', 0)
        )
        result['knapsack_result'] = decoded
        result['problem_type'] = 'knapsack'
        
    elif problem_type == 'tsp' and result.get('best_solution'):
        # Decode TSP solution
        decoded = decode_tsp_solution(
            solution=result['best_solution'],
            cities=problem.get('cities', []),
            total_distance=result.get('best_fitness', 0)
        )
        result['tsp_result'] = decoded
        result['problem_type'] = 'tsp'
    
    return result
