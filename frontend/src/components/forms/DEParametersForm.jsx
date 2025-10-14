// Location: frontend/src/components/forms/DEParametersForm.jsx

/**
 * Differential Evolution-specific parameter form.
 * Handles population_size, max_iterations, F, and CR.
 */

export default function DEParametersForm({ formData, onChange }) {
  const handleChange = (field, value) => {
    onChange({ ...formData, [field]: value });
  };

  return (
    <div className="mb-4 p-4 bg-purple-50 rounded-lg border border-purple-200">
      <h3 className="font-semibold text-gray-700 mb-3">
        Differential Evolution Parameters
      </h3>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        {/* Population Size */}
        <div>
          <label className="block text-sm font-medium text-gray-600 mb-1">
            Population Size:
          </label>
          <input
            type="number"
            min="10"
            value={formData.population_size}
            onChange={e => handleChange('population_size', e.target.value)}
            className="w-full p-2 border border-gray-300 rounded focus:ring-1 focus:ring-purple-400 bg-white text-sm"
          />
          <p className="text-xs text-gray-500 mt-1">
            Number of individuals (min: 10). Recommended: 10×dimensions.
          </p>
        </div>

        {/* Max Iterations */}
        <div>
          <label className="block text-sm font-medium text-gray-600 mb-1">
            Max Iterations:
          </label>
          <input
            type="number"
            min="1"
            max="100"
            value={formData.max_iterations}
            onChange={e => handleChange('max_iterations', e.target.value)}
            className="w-full p-2 border border-gray-300 rounded focus:ring-1 focus:ring-purple-400 bg-white text-sm"
          />
          <p className="text-xs text-gray-500 mt-1">
            Number of generations (max: 100). More = better exploration.
          </p>
        </div>

        {/* Differential Weight (F) */}
        <div>
          <label className="block text-sm font-medium text-gray-600 mb-1">
            Differential Weight (F):
          </label>
          <input
            type="number"
            step="0.05"
            min="0.0"
            max="2.0"
            value={formData.F}
            onChange={e => handleChange('F', e.target.value)}
            className="w-full p-2 border border-gray-300 rounded focus:ring-1 focus:ring-purple-400 bg-white text-sm"
          />
          <p className="text-xs text-gray-500 mt-1">
            Scaling factor for mutation (typical: 0.5–1.0).
          </p>
        </div>

        {/* Crossover Probability (CR) */}
        <div>
          <label className="block text-sm font-medium text-gray-600 mb-1">
            Crossover Probability (CR):
          </label>
          <input
            type="number"
            step="0.05"
            min="0.0"
            max="1.0"
            value={formData.CR}
            onChange={e => handleChange('CR', e.target.value)}
            className="w-full p-2 border border-gray-300 rounded focus:ring-1 focus:ring-purple-400 bg-white text-sm"
          />
          <p className="text-xs text-gray-500 mt-1">
            Probability of exchanging components (typical: 0.7–0.9).
          </p>
        </div>
      </div>
    </div>
  );
}
