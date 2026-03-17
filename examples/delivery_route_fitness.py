"""
Delivery Route Optimization - Small Business Example

Problem: A small bakery needs to deliver orders to 5 customers each morning.
Goal: Find the optimal route to minimize total delivery distance and fuel costs.

Decision Variables (x):
- x[0]: Distance to Customer 1 (km)
- x[1]: Distance to Customer 2 (km)
- x[2]: Distance to Customer 3 (km)
- x[3]: Distance to Customer 4 (km)
- x[4]: Distance to Customer 5 (km)

The fitness function calculates:
- Total distance traveled
- Fuel cost penalty ($0.15 per km)
- Time penalty for distances over 10km (traffic/delays)
"""

import numpy as np

def fitness(x):
    """
    Calculate the total cost of a delivery route.

    Lower values are better (minimization problem).

    Args:
        x: Array of 5 distances (km) representing route segments

    Returns:
        Total cost combining distance, fuel, and time penalties
    """

    # Total distance traveled (sum of all segments)
    total_distance = np.sum(x)

    # Fuel cost: $0.15 per kilometer
    fuel_cost = total_distance * 0.15

    # Time penalty: Extra cost for long segments (traffic/delays)
    # Any segment over 10km adds extra penalty
    time_penalty = np.sum(np.maximum(0, x - 10) * 0.5)

    # Route balance penalty: Prefer balanced routes over uneven ones
    # Penalize high variance in segment distances
    variance_penalty = np.var(x) * 0.1

    # Total cost (what we want to minimize)
    total_cost = fuel_cost + time_penalty + variance_penalty

    return total_cost
