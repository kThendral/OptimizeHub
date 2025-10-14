# 🧪 Testing Guide for TSP & Knapsack Integration

## ✅ What Was Completed

### Backend Changes:
1. ✅ **Updated `problem.py`**: Added fields for `problem_type`, `items`, `capacity`, `cities`
2. ✅ **Updated `executor.py`**: Added detection and handling of knapsack/TSP problems
3. ✅ **Created `solution_decoder.py`**: Converts raw solutions to human-readable formats
4. ✅ **Integration**: Results now include decoded knapsack_result or tsp_result

### Frontend Changes:
1. ✅ **Created `KnapsackInputForm.jsx`**: Full item management UI
2. ✅ **Created `TSPInputForm.jsx`**: City input with interactive map
3. ✅ **Updated `ResultsDisplay.jsx`**: Shows decoded results beautifully
4. ✅ **Updated `AlgorithmSelector.jsx`**: Switches forms based on problem type

---

## 🚀 How to Test

### 1. Start the Backend
```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Start the Frontend
```bash
cd frontend
npm run dev
```

### 3. Test Knapsack Problem

**Step-by-Step:**
1. Open http://localhost:5173
2. Select algorithm: **Particle Swarm Optimization (PSO)** or **Genetic Algorithm (GA)**
3. In "Fitness Function" dropdown, select: **🎒 Knapsack Problem**
4. You'll see the orange knapsack form appear!

**Example Input:**
```
Items:
- Laptop:  Weight=3,  Value=500
- Camera:  Weight=2,  Value=300
- Book:    Weight=1,  Value=50
- Phone:   Weight=1,  Value=200
- Tablet:  Weight=2,  Value=250

Capacity: 5
```

5. Configure algorithm parameters (or use defaults)
6. Click **Run Optimization**

**Expected Result:**
You should see:
- ✅ Selected items (e.g., "Laptop + Phone + Book" or "Camera + Tablet + Phone")
- 📊 Total Value (e.g., $750)
- ⚖️ Total Weight (e.g., 5/5)
- 📈 Capacity utilization bar (e.g., 100%)
- ✓ Checkmarks next to selected items

### 4. Test TSP Problem

**Step-by-Step:**
1. Select algorithm: **PSO** or **GA**
2. In "Fitness Function" dropdown, select: **🚀 Traveling Salesman (TSP)**
3. You'll see the blue TSP form with a map!

**Example Input:**
```
Cities:
- City A:  x=0,  y=0
- City B:  x=3,  y=4
- City C:  x=7,  y=1
- City D:  x=5,  y=6
```

4. Click **Run Optimization**

**Expected Result:**
You should see:
- 🗺️ Optimal route (e.g., "A → C → B → D → A")
- 📏 Total distance (e.g., 18.45 units)
- 📍 Route segments with individual distances
- 📊 Number of cities visited

---

## 🧪 Test Cases

### Test Case 1: Simple Knapsack
**Input:**
- Items: 3 items (weights: [2, 3, 4], values: [3, 4, 5])
- Capacity: 5
- Algorithm: PSO

**Expected:**
- Should select items 1 and 2 (total weight=5, value=7)
- Or items 0 and 3 if values are better

### Test Case 2: TSP with 4 Cities
**Input:**
- Cities: Square formation (0,0), (5,0), (5,5), (0,5)
- Algorithm: GA

**Expected:**
- Route should be a simple loop around the square
- Total distance ≈ 20 units

### Test Case 3: Overloaded Knapsack
**Input:**
- Items with total weight > capacity
- Capacity: 5
- Total items weight: 15

**Expected:**
- Algorithm selects subset that fits within capacity
- Utilization ≤ 100%
- Warning message shown during input

### Test Case 4: Large TSP (10 Cities)
**Input:**
- 10 random cities
- Algorithm: PSO with 100 iterations

**Expected:**
- Should find reasonable route
- Distance should be significantly better than random

---

## 📝 Sample API Request (via cURL)

### Knapsack Problem:
```bash
curl -X POST http://localhost:8000/api/optimize \
  -H "Content-Type: application/json" \
  -d '{
    "algorithm": "particle_swarm",
    "problem": {
      "problem_type": "knapsack",
      "dimensions": 4,
      "bounds": [[0,1],[0,1],[0,1],[0,1]],
      "objective": "minimize",
      "items": [
        {"name": "Laptop", "weight": 3, "value": 500},
        {"name": "Camera", "weight": 2, "value": 300},
        {"name": "Book", "weight": 1, "value": 50},
        {"name": "Phone", "weight": 1, "value": 200}
      ],
      "capacity": 5
    },
    "params": {
      "swarm_size": 30,
      "max_iterations": 50,
      "w": 0.7,
      "c1": 1.5,
      "c2": 1.5
    }
  }'
```

### TSP Problem:
```bash
curl -X POST http://localhost:8000/api/optimize \
  -H "Content-Type: application/json" \
  -d '{
    "algorithm": "genetic_algorithm",
    "problem": {
      "problem_type": "tsp",
      "dimensions": 4,
      "bounds": [[0,1],[0,1],[0,1],[0,1]],
      "objective": "minimize",
      "cities": [
        {"name": "City A", "x": 0, "y": 0},
        {"name": "City B", "x": 3, "y": 4},
        {"name": "City C", "x": 7, "y": 1},
        {"name": "City D", "x": 5, "y": 6}
      ]
    },
    "params": {
      "population_size": 50,
      "max_iterations": 50,
      "crossover_rate": 0.8,
      "mutation_rate": 0.1,
      "tournament_size": 3
    }
  }'
```

---

## 🐛 Troubleshooting

### Problem: "Missing 'fitness_function_name' in problem definition"
**Solution:** Make sure `problem_type` is set to 'knapsack' or 'tsp' in the request

### Problem: Form doesn't switch when selecting TSP/Knapsack
**Solution:** 
1. Check browser console for errors
2. Make sure `fitnessFunction` state is updating correctly
3. Refresh the page

### Problem: Backend throws "Unknown fitness function"
**Solution:**
- Verify `problem_type` field is being sent in the API request
- Check that items/cities data is included

### Problem: Results show raw numbers instead of decoded solution
**Solution:**
- Check that `solution_decoder.py` is being imported correctly
- Verify `problem_type` is in the response

### Problem: Knapsack selects items over capacity
**Solution:**
- This is a penalty-based approach; algorithm penalizes over-capacity
- Increase iterations or adjust mutation rate
- The fitness function includes heavy penalties for exceeding capacity

---

## 📊 Expected Performance

### Knapsack:
- **Small (4-5 items)**: Should find optimal in <1 second
- **Medium (10 items)**: Should find near-optimal in 1-2 seconds
- **Large (20+ items)**: May need more iterations (100+)

### TSP:
- **4-5 cities**: Should find optimal or near-optimal quickly
- **10 cities**: Should find good solution in 50-100 iterations
- **20+ cities**: May need 200+ iterations and larger population

---

## ✅ Success Criteria

**Knapsack Test Passes If:**
- ✓ Selected items total value is maximized
- ✓ Total weight ≤ capacity
- ✓ UI shows selected items with checkmarks
- ✓ Capacity utilization bar displays correctly

**TSP Test Passes If:**
- ✓ Route visits all cities exactly once
- ✓ Returns to starting city
- ✓ Total distance is reasonable (not visiting cities in random order)
- ✓ UI shows route segments with distances

---

## 🎯 Next Steps After Testing

If tests pass:
1. ✅ Add more real-world problem presets
2. ✅ Add route visualization map for TSP results
3. ✅ Add multi-algorithm comparison
4. ✅ Export results to CSV/JSON

If tests fail:
1. Check browser console for frontend errors
2. Check backend terminal for Python errors
3. Verify API request format matches expected schema
4. Use curl commands above to test backend directly
