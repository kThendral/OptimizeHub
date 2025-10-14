/**
 * Benchmark function configuration form.
 * Handles dimensions, bounds, and objective for benchmark functions.
 * Note: Fitness function selection is now handled by the collapsible selector in AlgorithmSelector.
 */

export default function ProblemDefinitionForm({ formData, onChange }) {
  const handleChange = (field, value) => {
    onChange({ ...formData, [field]: value });
  };

  return (
    <div className="mb-4 p-4 bg-gray-50 rounded-lg border border-gray-200">
      <h3 className="font-semibold text-gray-700 mb-3">Benchmark Function Configuration</h3>
      
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
