// Location: frontend/src/components/forms/SAParametersForm.jsx

/**
 * SA-specific parameter form.
 * Handles initial_temp, final_temp, cooling_rate, max_iterations, neighbor_std, cooling_schedule.
 */

export default function SAParametersForm({ formData, onChange }) {
  const handleChange = (field, value) => {
    onChange({ ...formData, [field]: value });
  };

  return (
    <div className="mb-4 p-4 bg-purple-50 rounded-lg border border-purple-200">
      <h3 className="font-semibold text-gray-700 mb-3">
        Simulated Annealing Parameters
      </h3>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        {/* Initial Temperature */}
        <div>
          <label className="block text-sm font-medium text-gray-600 mb-1">
            Initial Temperature:
          </label>
          <input
            type="number"
            step="0.1"
            min="0.1"
            value={formData.initialTemp}
            onChange={e => handleChange('initialTemp', e.target.value)}
            className="w-full p-2 border border-gray-300 rounded focus:ring-1 focus:ring-[color:var(--color-primary)] bg-white text-sm"
          />
          <p className="text-xs text-gray-500 mt-1">
            Starting temperature (higher = more exploration, typical: 10-1000).
          </p>
        </div>

        {/* Final Temperature */}
        <div>
          <label className="block text-sm font-medium text-gray-600 mb-1">
            Final Temperature:
          </label>
          <input
            type="number"
            step="0.01"
            min="0"
            value={formData.finalTemp}
            onChange={e => handleChange('finalTemp', e.target.value)}
            className="w-full p-2 border border-gray-300 rounded focus:ring-1 focus:ring-[color:var(--color-primary)] bg-white text-sm"
          />
          <p className="text-xs text-gray-500 mt-1">
            Stopping temperature (typical: 0.001-0.1).
          </p>
        </div>

        {/* Cooling Rate */}
        <div>
          <label className="block text-sm font-medium text-gray-600 mb-1">
            Cooling Rate:
          </label>
          <input
            type="number"
            step="0.01"
            min="0"
            max="1"
            value={formData.coolingRate}
            onChange={e => handleChange('coolingRate', e.target.value)}
            className="w-full p-2 border border-gray-300 rounded focus:ring-1 focus:ring-[color:var(--color-primary)] bg-white text-sm"
          />
          <p className="text-xs text-gray-500 mt-1">
            Temperature decay rate (typical: 0.85-0.99, higher = slower cooling).
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
            value={formData.maxIterations}
            onChange={e => handleChange('maxIterations', e.target.value)}
            className="w-full p-2 border border-gray-300 rounded focus:ring-1 focus:ring-[color:var(--color-primary)] bg-white text-sm"
          />
          <p className="text-xs text-gray-500 mt-1">
            Iterations per temperature level (max: 100).
          </p>
        </div>

        {/* Neighbor Std */}
        <div>
          <label className="block text-sm font-medium text-gray-600 mb-1">
            Neighbor Step Size:
          </label>
          <input
            type="number"
            step="0.01"
            min="0"
            max="1"
            value={formData.neighborStd}
            onChange={e => handleChange('neighborStd', e.target.value)}
            className="w-full p-2 border border-gray-300 rounded focus:ring-1 focus:ring-[color:var(--color-primary)] bg-white text-sm"
          />
          <p className="text-xs text-gray-500 mt-1">
            Step size for neighbor generation (typical: 0.01-0.5).
          </p>
        </div>

        {/* Cooling Schedule */}
        <div>
          <label className="block text-sm font-medium text-gray-600 mb-1">
            Cooling Schedule:
          </label>
          <select
            value={formData.coolingSchedule}
            onChange={e => handleChange('coolingSchedule', e.target.value)}
            className="w-full p-2 border border-gray-300 rounded focus:ring-1 focus:ring-[color:var(--color-primary)] bg-white text-sm"
          >
            <option value="geometric">Geometric (fast, default)</option>
            <option value="linear">Linear (medium speed)</option>
            <option value="logarithmic">Logarithmic (slow, thorough)</option>
          </select>
          <p className="text-xs text-gray-500 mt-1">
            Temperature reduction method (geometric recommended).
          </p>
        </div>
      </div>
    </div>
  );
}
