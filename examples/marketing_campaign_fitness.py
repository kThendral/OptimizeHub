"""
Marketing Campaign Budget Allocation - Small Business Example

Problem: A small e-commerce business has $5000 to spend on marketing.
Need to allocate budget across 4 channels to maximize customer acquisition.

Decision Variables (x):
- x[0]: Social Media Ads budget ($)
- x[1]: Google Ads budget ($)
- x[2]: Email Marketing budget ($)
- x[3]: Influencer Partnerships budget ($)

Expected ROI per channel (customers per $100 spent):
- Social Media: 5 customers
- Google Ads: 8 customers
- Email Marketing: 12 customers
- Influencer: 4 customers (but high brand awareness value)

Constraints:
- Total budget: $5000
- Minimum per channel: $200 (to be effective)
"""

import numpy as np

def fitness(x):
    """
    Calculate the negative of total customers acquired (we minimize in optimization).

    Lower values are better (minimization problem).
    We want to maximize customers, so we return negative customers.

    Args:
        x: Array of 4 budget allocations ($)

    Returns:
        Negative total customer acquisition + penalties
    """

    social_media, google_ads, email, influencer = x

    # Total marketing budget
    TOTAL_BUDGET = 5000

    # ROI: Expected customers per $100 spent
    SOCIAL_ROI = 5.0
    GOOGLE_ROI = 8.0
    EMAIL_ROI = 12.0
    INFLUENCER_ROI = 4.0

    # Minimum spend per channel to be effective
    MIN_CHANNEL_BUDGET = 200

    # Calculate customer acquisition from each channel
    social_customers = (social_media / 100) * SOCIAL_ROI
    google_customers = (google_ads / 100) * GOOGLE_ROI
    email_customers = (email / 100) * EMAIL_ROI
    influencer_customers = (influencer / 100) * INFLUENCER_ROI

    # Brand awareness bonus from influencer marketing
    # Even though direct ROI is lower, it has long-term benefits
    brand_bonus = min(influencer / 1000, 1.0) * 10

    # Total customer acquisition
    total_customers = (
        social_customers +
        google_customers +
        email_customers +
        influencer_customers +
        brand_bonus
    )

    # Penalty for not meeting minimum channel budgets
    # (spending too little per channel is ineffective)
    channel_penalties = 0
    for budget in x:
        if 0 < budget < MIN_CHANNEL_BUDGET:
            channel_penalties += (MIN_CHANNEL_BUDGET - budget) * 0.5

    # Penalty for exceeding total budget
    total_spent = np.sum(x)
    budget_penalty = max(0, total_spent - TOTAL_BUDGET) * 10

    # Penalty for negative budgets
    negative_penalty = sum([max(0, -val) * 100 for val in x])

    # Diversification bonus: Reward spreading budget across channels
    # Don't put all eggs in one basket
    non_zero_channels = np.sum(x > MIN_CHANNEL_BUDGET)
    diversification_bonus = non_zero_channels * 2

    # Objective: Maximize customers (minimize negative customers)
    # Add penalties for constraint violations
    objective = (
        -total_customers +  # Negative because we want to maximize
        channel_penalties +
        budget_penalty +
        negative_penalty -
        diversification_bonus
    )

    return objective
