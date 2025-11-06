"""
Example: Infinite Loop Function
This function creates an infinite loop to test timeout protection.
Should be TERMINATED by Docker sandbox after timeout limit.
"""

def fitness(x):
    """
    Creates infinite loop to test resource limits.
    Should be killed by timeout protection.
    """
    while True:
        pass  # Infinite loop - should trigger timeout
    
    return sum(x**2)  # Never reached