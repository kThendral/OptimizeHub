// Location: frontend/src/components/forms/ACORParametersForm.jsx

/**
 * ACOR-specific parameter form.
 * Handles colony_size, max_iterations, archive_size, q (locality), xi (convergence speed).
 */

export default function ACORParametersForm({ formData, onChange }) {
  const handleChange = (field, value) => {
    onChange({ ...formData, [field]: value });
  };

  return (
    <div className="mb-4 p-4 bg-purple-50 rounded-lg border border-purple-200">
      <h3 className="font-semibold text-gray-700 mb-3">
        Ant Colony Optimization (ACOR) Parameters
      </h3>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        {/* Colony Size */}
        <div>
          <label className="block text-sm font-medium text-gray-600 mb-1">
            Colony Size:
          </label>
          <input
            type="number"
            min="5"
            max="200"
            value={formData.colony_size}
            onChange={e => handleChange('colony_size', e.target.value)}
            className="w-full p-2 border border-gray-300 rounded focus:ring-1 focus:ring-[color:var(--color-primary)] bg-white text-sm"
          />
          <p className="text-xs text-gray-500 mt-1">
            Number of ants (min: 5). More ants = better exploration.
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
            className="w-full p-2 border border-gray-300 rounded focus:ring-1 focus:ring-[color:var(--color-primary)] bg-white text-sm"
          />
          <p className="text-xs text-gray-500 mt-1">
            Number of iterations (max: 100). More iterations = better convergence.
          </p>
        </div>

        {/* Archive Size */}
        <div>
          <label className="block text-sm font-medium text-gray-600 mb-1">
            Archive Size:
          </label>
          <input
            type="number"
            min="1"
            max="50"
            value={formData.archive_size}
            onChange={e => handleChange('archive_size', e.target.value)}
            className="w-full p-2 border border-gray-300 rounded focus:ring-1 focus:ring-[color:var(--color-primary)] bg-white text-sm"
          />
          <p className="text-xs text-gray-500 mt-1">
            Best solutions to keep (typical: 10-50, must be ≤ colony size).
          </p>
        </div>

        {/* q Parameter */}
        <div>
          <label className="block text-sm font-medium text-gray-600 mb-1">
            Locality Parameter (q):
          </label>
          <input
            type="number"
            step="0.001"
            min="0.001"
            max="0.5"
            value={formData.q}
            onChange={e => handleChange('q', e.target.value)}
            className="w-full p-2 border border-gray-300 rounded focus:ring-1 focus:ring-[color:var(--color-primary)] bg-white text-sm"
          />
          <p className="text-xs text-gray-500 mt-1">
            Intensification parameter (smaller = more focused, typical: 0.001-0.1).
          </p>
        </div>

        {/* xi Parameter */}
        <div>
          <label className="block text-sm font-medium text-gray-600 mb-1">
            Convergence Speed (xi):
          </label>
          <input
            type="number"
            step="0.05"
            min="0"
            max="1"
            value={formData.xi}
            onChange={e => handleChange('xi', e.target.value)}
            className="w-full p-2 border border-gray-300 rounded focus:ring-1 focus:ring-[color:var(--color-primary)] bg-white text-sm"
          />
          <p className="text-xs text-gray-500 mt-1">
            Speed of convergence (0-1, typical: 0.7-0.95).
          </p>
        </div>
      </div>
    </div>
  );
}
