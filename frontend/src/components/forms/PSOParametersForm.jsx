// Location: frontend/src/components/forms/PSOParametersForm.jsx

/**
 * PSO-specific parameter form.
 * Handles swarm_size, max_iterations, w (inertia), c1 (cognitive), c2 (social).
 */

export default function PSOParametersForm({ formData, onChange }) {
  const handleChange = (field, value) => {
    onChange({ ...formData, [field]: value });
  };

  return (
    <div className="mb-4 p-4 bg-purple-50 rounded-lg border border-purple-200">
      <h3 className="font-semibold text-gray-700 mb-3">
        Particle Swarm Optimization Parameters
      </h3>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        {/* Swarm Size */}
        <div>
          <label className="block text-sm font-medium text-gray-600 mb-1">
            Swarm Size:
          </label>
          <input
            type="number"
            min="10"
            max="200"
            value={formData.swarmSize}
            onChange={e => handleChange('swarmSize', e.target.value)}
            className="w-full p-2 border border-gray-300 rounded focus:ring-1 focus:ring-[color:var(--color-primary)] bg-white text-sm"
          />
          <p className="text-xs text-gray-500 mt-1">
            Number of particles (min: 10). More particles = better exploration.
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
            Number of generations (max: 100). More iterations = better convergence.
          </p>
        </div>

        {/* Inertia Weight (w) */}
        <div>
          <label className="block text-sm font-medium text-gray-600 mb-1">
            Inertia Weight (w):
          </label>
          <input
            type="number"
            step="0.1"
            min="0"
            max="1.2"
            value={formData.w}
            onChange={e => handleChange('w', e.target.value)}
            className="w-full p-2 border border-gray-300 rounded focus:ring-1 focus:ring-[color:var(--color-primary)] bg-white text-sm"
          />
          <p className="text-xs text-gray-500 mt-1">
            Controls exploration vs exploitation (typical: 0.4-1.0).
          </p>
        </div>

        {/* Cognitive Coefficient (c1) */}
        <div>
          <label className="block text-sm font-medium text-gray-600 mb-1">
            Cognitive Coefficient (c1):
          </label>
          <input
            type="number"
            step="0.1"
            min="0"
            max="4"
            value={formData.c1}
            onChange={e => handleChange('c1', e.target.value)}
            className="w-full p-2 border border-gray-300 rounded focus:ring-1 focus:ring-[color:var(--color-primary)] bg-white text-sm"
          />
          <p className="text-xs text-gray-500 mt-1">
            Personal best influence (typical: 1.5-2.0).
          </p>
        </div>

        {/* Social Coefficient (c2) */}
        <div>
          <label className="block text-sm font-medium text-gray-600 mb-1">
            Social Coefficient (c2):
          </label>
          <input
            type="number"
            step="0.1"
            min="0"
            max="4"
            value={formData.c2}
            onChange={e => handleChange('c2', e.target.value)}
            className="w-full p-2 border border-gray-300 rounded focus:ring-1 focus:ring-[color:var(--color-primary)] bg-white text-sm"
          />
          <p className="text-xs text-gray-500 mt-1">
            Global best influence (typical: 1.5-2.0).
          </p>
        </div>
      </div>
    </div>
  );
}
