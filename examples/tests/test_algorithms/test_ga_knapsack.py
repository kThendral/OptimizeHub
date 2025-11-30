"""
Interactive Knapsack Problem test for Genetic Algorithm.
User can input custom weights and values, or use predefined examples.
"""

import sys
import numpy as np
from pathlib import Path

# Add backend to path for imports
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

from app.algorithms.genetic_algorithm import GeneticAlgorithm


class KnapsackProblem:
    """0/1 Knapsack Problem implementation for GA testing."""
    
    def __init__(self, weights, values, capacity):
        self.weights = np.array(weights)
        self.values = np.array(values)
        self.capacity = capacity
        self.n_items = len(weights)
        
        # Calculate some useful metrics
        self.value_to_weight_ratio = self.values / self.weights
        self.total_weight = np.sum(self.weights)
        self.total_value = np.sum(self.values)
        
    def fitness_function(self, solution):
        """
        Fitness function for knapsack problem.
        solution: binary array where 1 = take item, 0 = don't take
        """
        # Convert to numpy array if it's a list
        if isinstance(solution, list):
            solution = np.array(solution)
            
        # Convert continuous solution to binary (GA works with continuous)
        binary_solution = (solution >= 0.5).astype(int)
        
        total_weight = np.sum(binary_solution * self.weights)
        total_value = np.sum(binary_solution * self.values)
        
        # Penalty for exceeding capacity
        if total_weight > self.capacity:
            # Heavy penalty proportional to excess weight
            penalty = (total_weight - self.capacity) * max(self.values)
            return total_value - penalty
        
        return total_value
    
    def decode_solution(self, solution):
        """Convert GA solution to readable format."""
        # Convert to numpy array if it's a list
        if isinstance(solution, list):
            solution = np.array(solution)
        
        binary_solution = (solution >= 0.5).astype(int)
        selected_items = []
        total_weight = 0
        total_value = 0
        
        for i, selected in enumerate(binary_solution):
            if selected:
                selected_items.append(i)
                total_weight += self.weights[i]
                total_value += self.values[i]
        
        return {
            'binary_solution': binary_solution.tolist(),
            'selected_items': selected_items,
            'total_weight': total_weight,
            'total_value': total_value,
            'valid': total_weight <= self.capacity
        }
    
    def print_problem(self):
        """Display the knapsack problem details."""
        print(f"\n📦 KNAPSACK PROBLEM")
        print(f"{'='*50}")
        print(f"Capacity: {self.capacity}")
        print(f"Number of items: {self.n_items}")
        print(f"\nItems:")
        print(f"{'Item':<6} {'Weight':<8} {'Value':<8} {'Ratio':<8}")
        print(f"{'-'*35}")
        
        for i in range(self.n_items):
            ratio = self.values[i] / self.weights[i]
            print(f"{i:<6} {self.weights[i]:<8} {self.values[i]:<8} {ratio:<8.2f}")
        
        print(f"\nTotal if all items: Weight={self.total_weight}, Value={self.total_value}")


def get_user_input():
    """Get knapsack problem from user input."""
    print("🎮 INTERACTIVE KNAPSACK PROBLEM SETUP")
    print("="*50)
    
    # Ask if user wants predefined examples or custom input
    print("\nChoose an option:")
    print("1. Quick test with 5 items (predefined)")
    print("2. Medium test with 8 items (predefined)")
    print("3. Custom input (enter your own weights and values)")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        # Small example
        weights = [2, 1, 3, 2, 5]
        values = [12, 10, 20, 15, 25]
        capacity = 8
        print(f"\n✅ Using predefined 5-item problem")
        
    elif choice == "2":
        # Medium example  
        weights = [10, 20, 30, 40, 50, 15, 25, 35]
        values = [60, 100, 120, 160, 200, 50, 75, 95]
        capacity = 100
        print(f"\n✅ Using predefined 8-item problem")
        
    elif choice == "3":
        # Custom input
        try:
            n_items = int(input("\nEnter number of items (3-10): "))
            if n_items < 3 or n_items > 10:
                print("Using 5 items (default)")
                n_items = 5
            
            weights = []
            values = []
            
            print(f"\nEnter {n_items} items:")
            for i in range(n_items):
                weight = float(input(f"Item {i+1} - Weight: "))
                value = float(input(f"Item {i+1} - Value: "))
                weights.append(weight)
                values.append(value)
            
            capacity = float(input(f"\nEnter knapsack capacity: "))
            print(f"\n✅ Using custom {n_items}-item problem")
            
        except (ValueError, KeyboardInterrupt):
            print("\n⚠️  Invalid input, using default 5-item problem")
            weights = [2, 1, 3, 2, 5]
            values = [12, 10, 20, 15, 25]
            capacity = 8
    else:
        print("\n⚠️  Invalid choice, using default 5-item problem")
        weights = [2, 1, 3, 2, 5]
        values = [12, 10, 20, 15, 25]
        capacity = 8
    
    return weights, values, capacity


def solve_knapsack_optimally(weights, values, capacity):
    """Simple brute force solution for small problems (verification)."""
    n = len(weights)
    if n > 10:  # Too many combinations
        return None
    
    best_value = 0
    best_combination = None
    
    # Try all 2^n combinations
    for i in range(2**n):
        combination = []
        total_weight = 0
        total_value = 0
        
        for j in range(n):
            if (i >> j) & 1:  # Bit j is set
                combination.append(j)
                total_weight += weights[j]
                total_value += values[j]
        
        if total_weight <= capacity and total_value > best_value:
            best_value = total_value
            best_combination = combination
    
    return best_combination, best_value


def test_ga_knapsack():
    """Test GA on knapsack problem with user input."""
    
    # Get problem from user
    weights, values, capacity = get_user_input()
    
    # Create knapsack problem
    knapsack = KnapsackProblem(weights, values, capacity)
    knapsack.print_problem()
    
    # Find optimal solution for verification (if small enough)
    optimal_solution = None
    if len(weights) <= 10:
        try:
            optimal_items, optimal_value = solve_knapsack_optimally(weights, values, capacity)
            optimal_solution = {'items': optimal_items, 'value': optimal_value}
            print(f"\n🎯 OPTIMAL SOLUTION (brute force):")
            print(f"Items to take: {optimal_items}")
            print(f"Optimal value: {optimal_value}")
        except:
            print(f"\n⚠️  Could not compute optimal solution")
    
    # Configure GA for binary optimization
    problem = {
        'dimensions': knapsack.n_items,
        'bounds': [(0.0, 1.0)] * knapsack.n_items,  # Each item: 0 (don't take) to 1 (take)
        'objective': 'maximize',  # Maximize knapsack value
        'fitness_function': knapsack.fitness_function
    }
    
    # GA parameters optimized for binary problems
    params = {
        'population_size': 50,  # Larger population for combinatorial problems
        'max_iterations': 100,  # More generations
        'crossover_rate': 0.9,  # High crossover for exploration
        'mutation_rate': 0.15,  # Higher mutation for binary problems
        'tournament_size': 5    # Larger tournament for selection pressure
    }
    
    print(f"\n🧬 RUNNING GENETIC ALGORITHM")
    print(f"{'='*50}")
    print(f"Population size: {params['population_size']}")
    print(f"Generations: {params['max_iterations']}")
    print(f"Crossover rate: {params['crossover_rate']}")
    print(f"Mutation rate: {params['mutation_rate']}")
    
    try:
        # Run GA
        ga = GeneticAlgorithm(problem, params)
        ga.initialize()
        ga.optimize()
        
        # Get results
        results = ga.get_results()
        solution_info = knapsack.decode_solution(results['best_solution'])
        
        print(f"\n📊 GENETIC ALGORITHM RESULTS")
        print(f"{'='*50}")
        print(f"Best fitness: {ga.best_fitness:.2f}")
        print(f"Initial fitness: {results['convergence_curve'][0]:.2f}")
        print(f"Improvement: {ga.best_fitness - results['convergence_curve'][0]:.2f}")
        print(f"Generations completed: {len(results['convergence_curve']) - 1}")
        
        print(f"\n📦 SOLUTION DETAILS")
        print(f"{'='*50}")
        print(f"Selected items: {solution_info['selected_items']}")
        print(f"Binary solution: {solution_info['binary_solution']}")
        print(f"Total weight: {solution_info['total_weight']:.1f} / {capacity}")
        print(f"Total value: {solution_info['total_value']:.1f}")
        print(f"Valid solution: {'✅ Yes' if solution_info['valid'] else '❌ No (exceeds capacity)'}")
        
        # Compare with optimal if available
        if optimal_solution:
            efficiency = (solution_info['total_value'] / optimal_solution['value']) * 100
            print(f"\n🎯 COMPARISON WITH OPTIMAL")
            print(f"{'='*50}")
            print(f"GA value: {solution_info['total_value']:.1f}")
            print(f"Optimal value: {optimal_solution['value']:.1f}")
            print(f"Efficiency: {efficiency:.1f}%")
            
            if efficiency >= 90:
                print(f"🏆 Excellent! GA found near-optimal solution")
            elif efficiency >= 70:
                print(f"✅ Good! GA found a good solution")
            else:
                print(f"⚠️  GA could improve (may need more generations)")
        
        return True
        
    except Exception as e:
        print(f"\n❌ GA Test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("🧬 GENETIC ALGORITHM - KNAPSACK PROBLEM TEST")
    print("="*60)
    
    success = test_ga_knapsack()
    
    print(f"\n{'='*60}")
    if success:
        print("🎉 Test completed successfully!")
    else:
        print("❌ Test failed")
    
    input("\nPress Enter to exit...")
    exit(0 if success else 1)