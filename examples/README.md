# Custom Fitness Function Examples

This directory contains realistic optimization examples for students and small business owners using OptimizeHub.

## 📦 Examples Included

### 1. 🚚 Delivery Route Optimization (Small Bakery)
**Files:**
- `delivery_route_fitness.py`
- `delivery_route_config.yaml`

**Use Case:** A small bakery needs to optimize morning delivery routes to 5 customers, minimizing fuel costs and delivery time.

**Key Features:**
- Minimizes total distance and fuel costs
- Penalizes long routes (traffic delays)
- Encourages balanced route segments
- Real-world cost parameters ($0.15/km)

**Best Algorithm:** PSO (Particle Swarm Optimization)

---

### 2. 💰 Student Monthly Budget Optimization
**Files:**
- `student_budget_fitness.py`
- `student_budget_config.yaml`

**Use Case:** A college student with $1200/month needs to allocate budget across 5 categories while maximizing savings.

**Key Features:**
- Enforces minimum requirements (food, housing, transport)
- Maximizes savings
- Penalizes overspending in discretionary categories
- Balances needs vs wants

**Best Algorithm:** GA (Genetic Algorithm)

---

### 3. 📱 Marketing Campaign Budget Allocation
**Files:**
- `marketing_campaign_fitness.py`
- `marketing_campaign_config.yaml`

**Use Case:** A small e-commerce business with $5000 marketing budget needs to allocate across 4 channels to maximize customer acquisition.

**Key Features:**
- Different ROI per channel (Email: 12, Google: 8, Social: 5, Influencer: 4)
- Brand awareness bonus for influencer marketing
- Encourages diversification across channels
- Minimum effective spend per channel

**Best Algorithm:** DE (Differential Evolution)

---

## 🚀 How to Use These Examples

### Step 1: Download the Files
Download both the `.py` and `.yaml` files for the example you want to try.

### Step 2: Go to Custom Fitness Page
Navigate to the "Custom Fitness" section in OptimizeHub.

### Step 3: Upload Files
- Upload the Python fitness function (`.py` file)
- Upload the YAML configuration (`.yaml` file)

### Step 4: Run Optimization
Click "Run Optimization" and wait for results (typically 10-30 seconds).

### Step 5: Analyze Results
Review the optimization results:
- **Best Solution:** The optimal allocation/route/budget
- **Best Fitness:** The minimized cost/penalty
- **Convergence Chart:** How the algorithm improved over iterations

---

## 📖 Understanding the Results

### Delivery Route Example
**Best Solution:** `[3.5, 4.2, 5.8, 3.1, 4.9]`
- Represents distances in km for each route segment
- Total distance: ~21.5 km
- Estimated fuel cost: ~$3.23
- Balanced segments (no extreme distances)

### Student Budget Example
**Best Solution:** `[250, 500, 80, 120, 250]`
- Food: $250 (meets $200 minimum, reasonable)
- Housing: $500 (meets minimum)
- Transport: $80 (meets $50 minimum)
- Entertainment: $120 (moderate)
- Savings: $250 (maximized!)
- Total: $1200 (exactly on budget)

### Marketing Campaign Example
**Best Solution:** `[800, 1500, 2000, 700]`
- Social Media: $800 (40 customers)
- Google Ads: $1500 (120 customers)
- Email: $2000 (240 customers) ← Highest ROI!
- Influencer: $700 (28 customers + brand bonus)
- Total Customers: ~428 + brand awareness
- Total Budget: $5000 (exactly on budget)

---

## 🔧 Customizing for Your Needs

### Modify the Fitness Function
Edit the `.py` file to change:
- Cost parameters (fuel price, ROI values, etc.)
- Penalty weights
- Number of variables (dimensions)
- Constraint requirements

### Modify the Configuration
Edit the `.yaml` file to change:
- Algorithm selection (PSO, GA, DE, SA, ACOR)
- Algorithm parameters (population size, iterations, etc.)
- Problem dimensions
- Variable bounds

---

## 💡 Tips for Success

### 1. **Start with Provided Examples**
Run the examples as-is first to understand how they work.

### 2. **Adjust Bounds Appropriately**
- Too wide: Slow convergence
- Too narrow: May miss optimal solution
- Use realistic bounds based on your problem

### 3. **Choose the Right Algorithm**
- **PSO:** Route/path optimization, continuous problems
- **GA:** Budget allocation, constrained problems
- **DE:** Complex constraints, high-dimensional
- **SA:** Local optimization, escaping local minima
- **ACOR:** Combinatorial problems, discrete choices

### 4. **Tune Iterations**
- Simple problems: 50-100 iterations
- Complex problems: 150-300 iterations
- More iterations = better solution (but slower)

### 5. **Interpret Negative Fitness**
Some examples return negative values for maximization:
- **Fitness = -50** is better than **Fitness = -30**
- Lower is always better in minimization problems
- Think of negative profit as "maximizing profit"

---

## 🎓 Learning Resources

### Understanding the Code

**Fitness Function Structure:**
```python
import numpy as np

def fitness(x):
    # x is an array of decision variables
    # Example: [budget1, budget2, budget3]

    # 1. Extract variables
    var1, var2, var3 = x

    # 2. Calculate objective (what you want to optimize)
    objective = calculate_cost(x)

    # 3. Add penalties for constraint violations
    penalties = calculate_penalties(x)

    # 4. Return total (lower is better)
    return objective + penalties
```

**Configuration Structure:**
```yaml
algorithm: PSO  # Choose: PSO, GA, DE, SA, ACOR

parameters:
  # Algorithm-specific parameters
  # See documentation for each algorithm

problem:
  dimensions: 5        # Number of decision variables
  lower_bound: 0.0     # Minimum value for each variable
  upper_bound: 100.0   # Maximum value for each variable
```

---

## ❓ FAQ

**Q: Can I use these examples for my actual business?**
A: Yes! These are realistic examples. Adjust parameters to match your specific situation.

**Q: What if my problem has different dimensions?**
A: Change `dimensions` in the YAML and adjust the fitness function to handle the new number of variables.

**Q: Can I mix different units (dollars, kilometers, etc.)?**
A: Yes, but normalize or weight them appropriately in the fitness function for best results.

**Q: How do I add more constraints?**
A: Add penalty terms in the fitness function that increase when constraints are violated.

**Q: Which algorithm is fastest?**
A: PSO is often fastest for continuous problems. GA and DE are more robust for constrained problems.

---

## 🤝 Contributing Your Examples

Have a great real-world optimization example? We'd love to see it!

Requirements:
1. Well-commented fitness function
2. Realistic parameters and constraints
3. Clear YAML configuration
4. Brief explanation of the use case

Share your examples with the community!

---

## 📞 Need Help?

If you have questions about:
- Modifying these examples for your needs
- Choosing the right algorithm
- Interpreting results
- Troubleshooting errors

Please check the main documentation or tutorial video on the Custom Fitness page.

---

**Happy Optimizing! 🎯**
