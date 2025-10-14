// Location: frontend/src/components/forms/ProblemDefinitionForm.jsx

/**
 * Shared problem definition form used by all algorithms.
 * Handles fitness function selection, dimensions, bounds, and objective.
 */

export default function ProblemDefinitionForm({ formData, onChange }) {
  const fitnessFunctions = [
    { value: 'sphere', label: 'Sphere Function', description: 'Simple unimodal function, good for testing' },
    { value: 'rastrigin', label: 'Rastrigin Function', description: 'Highly multimodal with many local minima' },
    { value: 'rosenbrock', label: 'Rosenbrock Function', description: 'Narrow valley, tests convergence' },
    { value: 'ackley', label: 'Ackley Function', description: 'Nearly flat outer region with central peak' },
    { value: 'griewank', label: 'Griewank Function', description: 'Product and sum components' }
  ];

  const handleChange = (field, value) => {
    onChange({ ...formData, [field]: value });
  };

  return (
    <div className="mb-4 p-4 bg-gray-50 rounded-lg border border-gray-200">
      <h3 className="font-semibold text-gray-700 mb-3">Problem Definition</h3>
      
      {/* Fitness Function Selection */}
      <div className="mb-3">
        <label className="block text-sm font-medium text-gray-600 mb-1">
          Fitness Function:
        </label>
        <select
          value={formData.fitnessFunction}
          onChange={e => handleChange('fitnessFunction', e.target.value)}
          className="w-full p-2 border border-gray-300 rounded focus:ring-1 focus:ring-[color:var(--color-primary)] bg-white text-sm"
        >
          {fitnessFunctions.map(f => (
            <option key={f.value} value={f.value}>
              {f.label}
            </option>
          ))}
        </select>
        <p className="text-xs text-gray-500 mt-1">
          {fitnessFunctions.find(f => f.value === formData.fitnessFunction)?.description}
        </p>
      </div>

      {/* Dimensions and Bounds */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
        <div>
          <label className="block text-sm font-medium text-gray-600 mb-1">
            Dimensions:
          </label>
          <input
            type="number"
            min="1"
            max="50"
            value={formData.dimensions}
            onChange={e => handleChange('dimensions', e.target.value)}
            className="w-full p-2 border border-gray-300 rounded focus:ring-1 focus:ring-[color:var(--color-primary)] bg-white text-sm"
          />
          <p className="text-xs text-gray-500 mt-1">Problem dimensionality (1-50)</p>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-600 mb-1">
            Lower Bound:
          </label>
          <input
            type="number"
            step="0.1"
            value={formData.lowerBound}
            onChange={e => handleChange('lowerBound', e.target.value)}
            className="w-full p-2 border border-gray-300 rounded focus:ring-1 focus:ring-[color:var(--color-primary)] bg-white text-sm"
          />
          <p className="text-xs text-gray-500 mt-1">Search space minimum</p>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-600 mb-1">
            Upper Bound:
          </label>
          <input
            type="number"
            step="0.1"
            value={formData.upperBound}
            onChange={e => handleChange('upperBound', e.target.value)}
            className="w-full p-2 border border-gray-300 rounded focus:ring-1 focus:ring-[color:var(--color-primary)] bg-white text-sm"
          />
          <p className="text-xs text-gray-500 mt-1">Search space maximum</p>
        </div>
      </div>

      {/* Objective */}
      <div className="mt-3">
        <label className="block text-sm font-medium text-gray-600 mb-1">
          Objective:
        </label>
        <select
          value={formData.objective}
          onChange={e => handleChange('objective', e.target.value)}
          className="w-full p-2 border border-gray-300 rounded focus:ring-1 focus:ring-[color:var(--color-primary)] bg-white text-sm"
        >
          <option value="minimize">Minimize</option>
          <option value="maximize">Maximize</option>
        </select>
        <p className="text-xs text-gray-500 mt-1">
          Minimize: find smallest value | Maximize: find largest value
        </p>
      </div>
    </div>
  );
}
