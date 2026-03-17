"""
Student Monthly Budget Optimization

Problem: A college student needs to allocate their monthly budget across
5 expense categories to maximize savings while meeting minimum requirements.

Decision Variables (x):
- x[0]: Food budget ($)
- x[1]: Housing budget ($)
- x[2]: Transportation budget ($)
- x[3]: Entertainment budget ($)
- x[4]: Savings ($)

Constraints:
- Food: minimum $200/month
- Housing: minimum $500/month
- Transportation: minimum $50/month
- Total budget: $1200/month
"""

import numpy as np
import math

def fitness(x):
    """
    Calculate the cost/penalty of a budget allocation.

    Lower values are better (minimization problem).
    Goal: Maximize savings while meeting minimum needs.

    Args:
        x: Array of 5 budget allocations

    Returns:
        Penalty score (lower is better)
    """

    food, housing, transport, entertainment, savings = x

    # Total monthly budget
    TOTAL_BUDGET = 1200

    # Minimum requirements
    MIN_FOOD = 200
    MIN_HOUSING = 500
    MIN_TRANSPORT = 50

    # Penalty for not meeting minimum requirements (very high penalty)
    food_penalty = max(0, MIN_FOOD - food) * 100
    housing_penalty = max(0, MIN_HOUSING - housing) * 100
    transport_penalty = max(0, MIN_TRANSPORT - transport) * 100

    # Penalty for exceeding total budget (very high penalty)
    total_spent = food + housing + transport + entertainment + savings
    budget_penalty = max(0, total_spent - TOTAL_BUDGET) * 200

    # Penalty for negative allocations (shouldn't happen with bounds, but safety check)
    negative_penalty = sum([max(0, -val) * 500 for val in x])

    # Objective: Maximize savings (so minimize negative savings)
    # Also prefer balanced allocations over extreme ones
    savings_objective = -savings

    # Small penalty for entertainment being too high (encourage responsibility)
    entertainment_penalty = max(0, entertainment - 100) * 0.5

    # Balance penalty: Prefer not to allocate more than necessary
    # Encourage efficient spending
    efficiency_penalty = (
        max(0, food - 300) * 0.1 +           # Don't overspend on food
        max(0, transport - 150) * 0.1 +      # Don't overspend on transport
        max(0, entertainment - 150) * 0.2    # Don't overspend on entertainment
    )

    # Total penalty (what we want to minimize)
    total_penalty = (
        food_penalty +
        housing_penalty +
        transport_penalty +
        budget_penalty +
        negative_penalty +
        savings_objective +
        entertainment_penalty +
        efficiency_penalty
    )

    return total_penalty
