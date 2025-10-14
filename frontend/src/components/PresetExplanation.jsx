// Location: frontend/src/components/PresetExplanation.jsx

/**
 * Displays educational explanation for selected preset.
 * Shows what the problem is, expected results, and why the configuration was chosen.
 */
export default function PresetExplanation({ preset }) {
  if (!preset || !preset.explanation) return null;

  return (
    <div className="mb-6 bg-gradient-to-br from-indigo-50 to-purple-50 rounded-xl shadow-md overflow-hidden border-2 border-purple-200">
      {/* Header */}
      <div className="bg-gradient-to-r from-purple-600 to-indigo-600 px-6 py-4">
        <div className="flex items-center gap-3">
          <span className="text-3xl">📚</span>
          <div>
            <h3 className="text-xl font-bold text-white">{preset.name}</h3>
            <p className="text-purple-100 text-sm mt-1">{preset.description}</p>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="p-6 space-y-5">
        {/* What is this problem? */}
        <div className="bg-white rounded-lg p-4 border-l-4 border-blue-500">
          <div className="flex items-start gap-3">
            <span className="text-2xl flex-shrink-0">🤔</span>
            <div>
              <h4 className="font-bold text-gray-800 mb-2">What is this problem?</h4>
              <p className="text-gray-700 text-sm leading-relaxed">
                {preset.explanation.problem}
              </p>
            </div>
          </div>
        </div>

        {/* Expected Results */}
        <div className="bg-white rounded-lg p-4 border-l-4 border-green-500">
          <div className="flex items-start gap-3">
            <span className="text-2xl flex-shrink-0">📊</span>
            <div>
              <h4 className="font-bold text-gray-800 mb-2">What results should I expect?</h4>
              <p className="text-gray-700 text-sm leading-relaxed">
                {preset.explanation.expectedResults}
              </p>
            </div>
          </div>
        </div>

        {/* Why these settings? */}
        <div className="bg-white rounded-lg p-4 border-l-4 border-purple-500">
          <div className="flex items-start gap-3">
            <span className="text-2xl flex-shrink-0">⚙️</span>
            <div>
              <h4 className="font-bold text-gray-800 mb-2">Why these parameter settings?</h4>
              <p className="text-gray-700 text-sm leading-relaxed">
                {preset.explanation.why}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Stats Footer */}
      <div className="bg-purple-100 px-6 py-3 border-t border-purple-200">
        <div className="flex flex-wrap gap-4 text-xs">
          <div className="flex items-center gap-1.5">
            <span className="font-semibold text-purple-700">🎯 Algorithm:</span>
            <span className="text-gray-700">
              {preset.algorithm === 'particle_swarm' ? 'Particle Swarm Optimization (PSO)' : 'Genetic Algorithm (GA)'}
            </span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="font-semibold text-purple-700">📐 Dimensions:</span>
            <span className="text-gray-700">{preset.problemData.dimensions}D</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="font-semibold text-purple-700">⏱️ Expected Time:</span>
            <span className="text-gray-700">{preset.expectedTime}</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="font-semibold text-purple-700">🎯 Target Fitness:</span>
            <span className="text-gray-700">{preset.expectedFitness}</span>
          </div>
        </div>
      </div>
    </div>
  );
}
