# Real-World Problems Integration Guide

## Overview
The backend already has support for real-world optimization problems. This document explains how they work and what's needed to fully integrate them into the UI.

## Available Problem Types

### 1. Traveling Salesman Problem (TSP) 🗺️
**File:** `backend/app/core/real_world_problems.py`

**What it does:** Finds the shortest route through a set of cities, returning to the start.

**Example Input:**
```python
cities = [
    (0, 0),    # City A at coordinates (0, 0)
    (1, 2),    # City B at coordinates (1, 2)
    (3, 1),    # City C
    (5, 3),    # City D
    (2, 4)     # City E
]
```

**How it works:**
- Solution is a permutation (order to visit cities)
- Fitness = total distance traveled
- Algorithm minimizes total route distance

**UI Needed:**
- Input form for city coordinates (or drag-and-drop on map)
- Result visualization showing the route on a 2D map
- Distance matrix display

---

### 2. Knapsack Problem 🎒
**File:** `backend/app/core/real_world_problems.py`

**What it does:** Selects items to maximize value without exceeding weight capacity.

**Example Input:**
```python
items = [
    {"name": "Laptop", "weight": 3, "value": 500},
    {"name": "Camera", "weight": 2, "value": 300},
    {"name": "Book", "weight": 1, "value": 50},
    {"name": "Phone", "weight": 1, "value": 200}
]
capacity = 5  # kg
```

**How it works:**
- Solution is binary (0 or 1 for each item)
- Fitness = negative total value (we minimize)
- Penalty if total weight exceeds capacity

**UI Needed:**
- Table input for items (name, weight, value)
- Capacity slider
- Result showing selected items with total weight/value
- Visual bar chart of utilization

---

### 3. Job Scheduling 📅
**File:** `backend/app/core/real_world_problems.py`

**What it does:** Assigns jobs to machines to minimize total completion time (makespan).

**Example Input:**
```python
jobs = [
    {"name": "Job 1", "time": 3},
    {"name": "Job 2", "time": 2},
    {"name": "Job 3", "time": 4},
    {"name": "Job 4", "time": 1},
    {"name": "Job 5", "time": 5}
]
n_machines = 2
```

**How it works:**
- Solution is job ordering
- Jobs assigned to machines with least load
- Fitness = maximum completion time across machines

**UI Needed:**
- Job list input (name, processing time)
- Number of machines selector
- Gantt chart visualization of schedule
- Machine utilization bars

---

## Integration Steps

### Phase 1: Backend API Extension ✅ DONE
- [x] Create fitness functions for TSP, Knapsack, Scheduling
- [x] Add `real_world_problems.py` module
- [ ] Add API endpoint to accept custom problem data
- [ ] Update problem validation for real-world types

### Phase 2: Frontend UI (TODO)
- [ ] Add "Problem Type" selector (Benchmark vs Real-World)
- [ ] Create custom input forms:
  - [ ] TSP: City coordinate input
  - [ ] Knapsack: Item table
  - [ ] Scheduling: Job list
- [ ] Add problem-specific result visualizations
- [ ] Add presets for each problem type

### Phase 3: Visualization (TODO)
- [ ] TSP: Interactive route map
- [ ] Knapsack: Item selection display
- [ ] Scheduling: Gantt chart timeline
- [ ] Add export results to CSV/JSON

---

## How to Use (When Fully Integrated)

### Example: Solving TSP

1. **Select Problem Type:** Dropdown shows "Traveling Salesman Problem"
2. **Input Cities:** 
   ```
   City A: (0, 0)
   City B: (3, 4)
   City C: (7, 1)
   City D: (5, 6)
   ```
3. **Select Algorithm:** PSO or GA
4. **Configure Parameters:** Use defaults or customize
5. **Run Optimization**
6. **View Results:**
   - Best route: A → C → B → D → A
   - Total distance: 18.45 km
   - Map showing the route with arrows
   - Distance matrix

---

## Current Status

✅ **Backend:** Fully functional fitness functions
🔄 **Frontend:** Placeholder in dropdown (shows "COMING SOON")
❌ **Integration:** Not yet connected
❌ **Visualization:** Not implemented

**Next Steps:**
1. Create custom input forms for each problem type
2. Update API to accept problem-specific data
3. Add result visualizations
4. Add real-world problem presets

---

## Testing Real-World Problems (Backend)

You can test the backend functions directly:

```python
from app.core.real_world_problems import create_tsp_fitness
import numpy as np

# Create TSP fitness function
cities = [(0, 0), (1, 2), (3, 1), (5, 3)]
fitness_fn = create_tsp_fitness(cities)

# Test with a solution (continuous values will be ranked)
solution = np.array([0.5, 0.2, 0.9, 0.1])
distance = fitness_fn(solution)
print(f"Total distance: {distance}")
```

This allows you to verify the optimization logic works correctly before UI integration.
