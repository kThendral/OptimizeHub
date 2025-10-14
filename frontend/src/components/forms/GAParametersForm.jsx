// Location: frontend/src/components/forms/GAParametersForm.jsx

/**
 * Genetic Algorithm-specific parameter form.
 * Handles population_size, max_iterations, crossover_rate, mutation_rate, tournament_size.
 */

export default function GAParametersForm({ formData, onChange }) {
  const handleChange = (field, value) => {
    onChange({ ...formData, [field]: value });
  };

  return (
    <div className="mb-4 p-4 bg-green-50 rounded-lg border border-green-200">
      <h3 className="font-semibold text-gray-700 mb-3">
        Genetic Algorithm Parameters
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
            max="200"
            value={formData.populationSize}
            onChange={e => handleChange('populationSize', e.target.value)}
            className="w-full p-2 border border-gray-300 rounded focus:ring-1 focus:ring-[color:var(--color-primary)] bg-white text-sm"
          />
          <p className="text-xs text-gray-500 mt-1">
            Number of individuals (min: 10). Larger = more genetic diversity.
          </p>
        </div>

        {/* Max Iterations */}
        <div>
          <label className="block text-sm font-medium text-gray-600 mb-1">
            Max Generations:
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
            Number of generations (max: 100). More = better evolution.
          </p>
        </div>

        {/* Crossover Rate */}
        <div>
          <label className="block text-sm font-medium text-gray-600 mb-1">
            Crossover Rate:
          </label>
          <input
            type="number"
            step="0.05"
            min="0"
            max="1"
            value={formData.crossoverRate}
            onChange={e => handleChange('crossoverRate', e.target.value)}
            className="w-full p-2 border border-gray-300 rounded focus:ring-1 focus:ring-[color:var(--color-primary)] bg-white text-sm"
          />
          <p className="text-xs text-gray-500 mt-1">
            Probability of combining parent genes (typical: 0.7-0.9).
          </p>
        </div>

        {/* Mutation Rate */}
        <div>
          <label className="block text-sm font-medium text-gray-600 mb-1">
            Mutation Rate:
          </label>
          <input
            type="number"
            step="0.01"
            min="0"
            max="1"
            value={formData.mutationRate}
            onChange={e => handleChange('mutationRate', e.target.value)}
            className="w-full p-2 border border-gray-300 rounded focus:ring-1 focus:ring-[color:var(--color-primary)] bg-white text-sm"
          />
          <p className="text-xs text-gray-500 mt-1">
            Probability of random changes (typical: 0.01-0.2).
          </p>
        </div>

        {/* Tournament Size */}
        <div>
          <label className="block text-sm font-medium text-gray-600 mb-1">
            Tournament Size:
          </label>
          <input
            type="number"
            min="2"
            max="10"
            value={formData.tournamentSize}
            onChange={e => handleChange('tournamentSize', e.target.value)}
            className="w-full p-2 border border-gray-300 rounded focus:ring-1 focus:ring-[color:var(--color-primary)] bg-white text-sm"
          />
          <p className="text-xs text-gray-500 mt-1">
            Selection pressure (higher = more elitism, typical: 2-5).
          </p>
        </div>
      </div>
    </div>
  );
}
