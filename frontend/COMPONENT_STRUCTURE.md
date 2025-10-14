# Frontend Component Structure (Hybrid Approach)

## Architecture Overview

The refactored frontend uses a **hybrid approach** where:
- **Shared components** (problem definition) are reused across all algorithms
- **Algorithm-specific forms** are conditionally rendered based on user selection

## Component Hierarchy

```
AlgorithmSelector (Main Container)
├── ProblemDefinitionForm (Shared)
│   ├── Fitness Function selector
│   ├── Dimensions input
│   ├── Bounds (lower/upper)
│   └── Objective (minimize/maximize)
│
└── Algorithm-Specific Forms (Conditional)
    ├── PSOParametersForm (when algorithm === 'particle_swarm')
    │   ├── swarm_size
    │   ├── max_iterations
    │   ├── w (inertia weight)
    │   ├── c1 (cognitive coefficient)
    │   └── c2 (social coefficient)
    │
    ├── GAParametersForm (when algorithm === 'genetic_algorithm')
    │   ├── population_size
    │   ├── max_iterations
    │   ├── crossover_rate
    │   ├── mutation_rate
    │   └── tournament_size
    │
    └── [Future: SAParametersForm, ACOParametersForm, etc.]
```

## File Structure

```
frontend/src/components/
├── AlgorithmSelector.jsx          # Main container component
├── ResultsDisplay.jsx              # Results visualization
└── forms/
    ├── ProblemDefinitionForm.jsx   # Shared problem definition
    ├── PSOParametersForm.jsx       # PSO-specific parameters
    └── GAParametersForm.jsx        # GA-specific parameters
```

## Benefits of This Approach

### 1. **Separation of Concerns**
- Each algorithm's parameters are isolated in their own component
- Problem definition is shared, avoiding duplication
- Easy to maintain and test

### 2. **Scalability**
Adding a new algorithm requires:
1. Create new parameter form component (e.g., `SAParametersForm.jsx`)
2. Import it in `AlgorithmSelector.jsx`
3. Add conditional rendering block
4. Add backend payload mapping

### 3. **Better UX**
- Users only see relevant parameters for their selected algorithm
- No confusion from irrelevant fields
- Each form has algorithm-specific help text

### 4. **Type Safety & Validation**
- Each form validates its own parameter constraints
- Backend validation errors map clearly to specific forms
- Easier to add field-level validation

## Component Communication Pattern

### Parent → Child (Props)
```jsx
<ProblemDefinitionForm 
  formData={problemData}
  onChange={setProblemData}
/>
```

### Child → Parent (Callback)
```jsx
// Inside ProblemDefinitionForm.jsx
const handleChange = (field, value) => {
  onChange({ ...formData, [field]: value });
};
```

## State Management

### Centralized in AlgorithmSelector
```javascript
// Shared state
const [problemData, setProblemData] = useState({...});

// Algorithm-specific state
const [psoParams, setPsoParams] = useState({...});
const [gaParams, setGaParams] = useState({...});
```

### Payload Construction
```javascript
// Problem object (shared)
const problem = {
  dimensions: parseInt(problemData.dimensions),
  bounds: [...],
  objective: problemData.objective,
  fitness_function_name: problemData.fitnessFunction
};

// Algorithm-specific params
if (selectedAlgorithm === 'particle_swarm') {
  params = {
    swarm_size: parseInt(psoParams.swarmSize),
    max_iterations: parseInt(psoParams.maxIterations),
    w: parseFloat(psoParams.w),
    c1: parseFloat(psoParams.c1),
    c2: parseFloat(psoParams.c2)
  };
}
```

## Visual Indicators

Each algorithm form has a unique color scheme:
- **PSO**: Purple background (`bg-purple-50` / `border-purple-200`)
- **GA**: Green background (`bg-green-50` / `border-green-200`)
- **Problem Definition**: Gray background (`bg-gray-50` / `border-gray-200`)

This helps users visually distinguish between shared and algorithm-specific sections.

## Adding a New Algorithm (Example: Simulated Annealing)

### Step 1: Create Parameter Form
```jsx
// frontend/src/components/forms/SAParametersForm.jsx
export default function SAParametersForm({ formData, onChange }) {
  return (
    <div className="mb-4 p-4 bg-orange-50 rounded-lg border border-orange-200">
      <h3 className="font-semibold text-gray-700 mb-3">
        Simulated Annealing Parameters
      </h3>
      {/* Form fields for initial_temperature, cooling_rate, etc. */}
    </div>
  );
}
```

### Step 2: Import in AlgorithmSelector
```jsx
import SAParametersForm from './forms/SAParametersForm';
```

### Step 3: Add State
```jsx
const [saParams, setSaParams] = useState({
  initialTemperature: 100.0,
  coolingRate: 0.95,
  maxIterations: 50,
  minTemperature: 0.01
});
```

### Step 4: Add Conditional Rendering
```jsx
{selectedAlgorithm === 'simulated_annealing' && (
  <SAParametersForm 
    formData={saParams}
    onChange={setSaParams}
  />
)}
```

### Step 5: Add Payload Mapping
```jsx
else if (selectedAlgorithm === 'simulated_annealing') {
  params = {
    initial_temperature: parseFloat(saParams.initialTemperature),
    cooling_rate: parseFloat(saParams.coolingRate),
    max_iterations: parseInt(saParams.maxIterations),
    min_temperature: parseFloat(saParams.minTemperature)
  };
}
```

## Testing Checklist

- [ ] PSO form appears only when PSO is selected
- [ ] GA form appears only when GA is selected
- [ ] Problem definition form is always visible
- [ ] Payload structure matches backend schema
- [ ] Parameter validation matches backend constraints
- [ ] Help text is clear and accurate
- [ ] Forms are responsive on mobile

## Future Enhancements

1. **Preset Templates**: Add "Quick Start" buttons with preset parameter combinations
2. **Parameter Tooltips**: Add info icons with detailed explanations
3. **Real-time Validation**: Show validation errors before submission
4. **Save/Load Configurations**: Allow users to save favorite parameter sets
5. **Parameter Comparison**: Side-by-side comparison of different parameter sets
