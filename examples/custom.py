def fitness(x):
    weights = [2, 1, 3, 2, 5]
    values = [12, 10, 20, 15, 25]
    capacity = 8

    total_weight = sum(w * (1 if xi >= 0.5 else 0) for w, xi in zip(weights, x))
    total_value = sum(v * (1 if xi >= 0.5 else 0) for v, xi in zip(values, x))

    # Apply penalty if over capacity
    if total_weight > capacity:
        total_value -= (total_weight - capacity) * 10

    # Since GA usually minimizes fitness, return the negative (maximize profit)
    return -total_value
