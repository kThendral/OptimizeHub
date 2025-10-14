/**
 * Human-readable results display for optimization algorithms.
 * Shows: Summary, Best Solution, Performance Metrics, and Convergence.
 */
export default function ResultsDisplay({ result }) {
  if (!result) return null;

  // Calculate improvement metrics
  const hasConvergence = result.convergence_curve && result.convergence_curve.length > 0;
  const initialFitness = hasConvergence ? result.convergence_curve[0] : null;
  const finalFitness = result.best_fitness;
  const improvement = initialFitness && finalFitness !== null 
    ? initialFitness - finalFitness 
    : null;
  const improvementPercent = initialFitness && improvement !== null && initialFitness !== 0
    ? ((improvement / Math.abs(initialFitness)) * 100).toFixed(2)
    : null;

  // Get algorithm display name
  const getAlgoName = (algo) => {
    const names = {
      'ParticleSwarmOptimization': 'Particle Swarm Optimization (PSO)',
      'GeneticAlgorithm': 'Genetic Algorithm (GA)',
      'particle_swarm': 'Particle Swarm Optimization (PSO)',
      'genetic_algorithm': 'Genetic Algorithm (GA)',
    };
    return names[algo] || algo;
  };

  // Format large numbers
  const formatNumber = (num) => {
    if (num === null || num === undefined) return 'N/A';
    if (Math.abs(num) < 0.0001) return num.toExponential(4);
    if (Math.abs(num) > 1000000) return num.toExponential(4);
    return num.toFixed(6);
  };

  return (
    <div className="mt-8 space-y-6">
      {/* Header */}
      <div className="flex items-center gap-3">
        <span className="text-3xl">🎉</span>
        <h3 className="text-2xl font-bold text-gray-800">Optimization Results</h3>
      </div>

      {/* Summary Card */}
      <div className="bg-gradient-to-r from-green-50 to-emerald-50 rounded-xl shadow-md border-2 border-green-200 overflow-hidden">
        <div className="bg-gradient-to-r from-green-600 to-emerald-600 px-6 py-3">
          <h4 className="text-lg font-bold text-white flex items-center gap-2">
            <span>✓</span> Optimization Complete
          </h4>
        </div>
        <div className="p-6 grid grid-cols-2 md:grid-cols-4 gap-4">
          <div>
            <p className="text-xs text-gray-500 uppercase font-semibold mb-1">Algorithm</p>
            <p className="text-sm font-medium text-gray-800">{getAlgoName(result.algorithm)}</p>
          </div>
          <div>
            <p className="text-xs text-gray-500 uppercase font-semibold mb-1">Status</p>
            <p className="text-sm font-medium text-green-600 capitalize">{result.status}</p>
          </div>
          <div>
            <p className="text-xs text-gray-500 uppercase font-semibold mb-1">Iterations</p>
            <p className="text-sm font-medium text-gray-800">{result.iterations_completed || 'N/A'}</p>
          </div>
          <div>
            <p className="text-xs text-gray-500 uppercase font-semibold mb-1">Execution Time</p>
            <p className="text-sm font-medium text-gray-800">
              {result.execution_time ? `${result.execution_time.toFixed(3)}s` : 'N/A'}
            </p>
          </div>
        </div>
      </div>

      {/* Best Solution Card */}
      <div className="bg-white rounded-xl shadow-md border-2 border-purple-200 overflow-hidden">
        <div className="bg-gradient-to-r from-purple-600 to-indigo-600 px-6 py-3">
          <h4 className="text-lg font-bold text-white flex items-center gap-2">
            <span>🎯</span> Best Solution Found
          </h4>
        </div>
        <div className="p-6">
          {/* Knapsack-specific results */}
          {result.problem_type === 'knapsack' && result.knapsack_result && (
            <div className="space-y-4">
              <div className="bg-gradient-to-r from-orange-50 to-yellow-50 p-4 rounded-lg border-2 border-orange-200">
                <h5 className="font-bold text-gray-800 mb-3 flex items-center gap-2">
                  <span>🎒</span> Knapsack Solution
                </h5>
                <div className="grid grid-cols-2 gap-3 mb-4">
                  <div className="bg-white p-3 rounded border border-orange-300">
                    <p className="text-xs text-gray-500 uppercase font-semibold">Total Value</p>
                    <p className="text-2xl font-bold text-green-600">${result.knapsack_result.total_value}</p>
                  </div>
                  <div className="bg-white p-3 rounded border border-orange-300">
                    <p className="text-xs text-gray-500 uppercase font-semibold">Total Weight</p>
                    <p className="text-2xl font-bold text-blue-600">
                      {result.knapsack_result.total_weight} / {result.knapsack_result.capacity}
                    </p>
                  </div>
                </div>
                <div className="bg-white p-3 rounded border border-orange-300 mb-4">
                  <p className="text-xs text-gray-500 uppercase font-semibold mb-1">Capacity Utilization</p>
                  <div className="flex items-center gap-2">
                    <div className="flex-1 bg-gray-200 rounded-full h-4">
                      <div 
                        className="bg-gradient-to-r from-orange-500 to-yellow-500 h-4 rounded-full"
                        style={{ width: `${result.knapsack_result.weight_utilization}%` }}
                      ></div>
                    </div>
                    <span className="font-bold text-purple-600">{result.knapsack_result.weight_utilization}%</span>
                  </div>
                </div>
                <div>
                  <p className="text-sm font-semibold text-gray-700 mb-2">
                    Selected Items ({result.knapsack_result.total_items_selected}):
                  </p>
                  <div className="space-y-2">
                    {result.knapsack_result.selected_items.map((item, idx) => (
                      <div key={idx} className="bg-white p-2 rounded border border-gray-300 flex justify-between items-center">
                        <span className="font-medium text-gray-800">✓ {item.name}</span>
                        <div className="flex gap-3 text-sm">
                          <span className="text-blue-600">Weight: {item.weight}</span>
                          <span className="text-green-600">Value: ${item.value}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* TSP-specific results */}
          {result.problem_type === 'tsp' && result.tsp_result && (
            <div className="space-y-4">
              <div className="bg-gradient-to-r from-blue-50 to-cyan-50 p-4 rounded-lg border-2 border-blue-200">
                <h5 className="font-bold text-gray-800 mb-3 flex items-center gap-2">
                  <span>🗺️</span> TSP Solution
                </h5>
                <div className="grid grid-cols-2 gap-3 mb-4">
                  <div className="bg-white p-3 rounded border border-blue-300">
                    <p className="text-xs text-gray-500 uppercase font-semibold">Total Distance</p>
                    <p className="text-2xl font-bold text-blue-600">{result.tsp_result.total_distance} units</p>
                  </div>
                  <div className="bg-white p-3 rounded border border-blue-300">
                    <p className="text-xs text-gray-500 uppercase font-semibold">Cities Visited</p>
                    <p className="text-2xl font-bold text-purple-600">{result.tsp_result.total_cities}</p>
                  </div>
                </div>
                <div>
                  <p className="text-sm font-semibold text-gray-700 mb-2">
                    Optimal Route:
                  </p>
                  <div className="bg-white p-3 rounded border border-blue-300 mb-3">
                    <p className="text-sm font-mono text-gray-800">
                      {result.tsp_result.route_order.join(' → ')} → {result.tsp_result.route_order[0]}
                    </p>
                  </div>
                  <p className="text-sm font-semibold text-gray-700 mb-2">
                    Route Segments:
                  </p>
                  <div className="space-y-1">
                    {result.tsp_result.segments.map((segment, idx) => (
                      <div key={idx} className="bg-white p-2 rounded border border-gray-300 flex justify-between items-center text-sm">
                        <span className="text-gray-700">{segment.from} → {segment.to}</span>
                        <span className="font-mono text-blue-600">{segment.distance} units</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Standard benchmark results */}
          {!result.problem_type && (
            <>
              <div className="mb-4">
                <p className="text-sm text-gray-600 mb-2">Fitness Value:</p>
                <p className="text-3xl font-bold text-purple-600">
                  {formatNumber(finalFitness)}
                </p>
              </div>
              
              {result.best_solution && (
                <div>
                  <p className="text-sm text-gray-600 mb-2">Solution Coordinates:</p>
                  <div className="bg-gray-50 p-4 rounded-lg border border-gray-200">
                    <div className="flex flex-wrap gap-2">
                      {result.best_solution.map((val, idx) => (
                        <div key={idx} className="bg-white px-3 py-2 rounded border border-gray-300">
                          <span className="text-xs text-gray-500">x[{idx}] = </span>
                          <span className="text-sm font-mono font-semibold text-gray-800">
                            {formatNumber(val)}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              )}
            </>
          )}
        </div>
      </div>

      {/* Performance Metrics Card */}
      {hasConvergence && (
        <div className="bg-white rounded-xl shadow-md border-2 border-blue-200 overflow-hidden">
          <div className="bg-gradient-to-r from-blue-600 to-cyan-600 px-6 py-3">
            <h4 className="text-lg font-bold text-white flex items-center gap-2">
              <span>📊</span> Performance Metrics
            </h4>
          </div>
          <div className="p-6">
            {/* Convergence Summary */}
            <div className="mb-6 p-4 bg-gradient-to-r from-blue-50 to-cyan-50 rounded-lg border-2 border-blue-300">
              <h5 className="font-bold text-gray-800 mb-3 flex items-center gap-2">
                <span>🎯</span> Convergence Summary
              </h5>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Overall Improvement:</span>
                  <span className="font-bold text-green-600 text-lg">
                    {improvementPercent ? `${improvementPercent}%` : 'N/A'}
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Convergence Status:</span>
                  <span className={`font-semibold ${
                    parseFloat(improvementPercent) > 99 ? 'text-green-600' :
                    parseFloat(improvementPercent) > 90 ? 'text-blue-600' :
                    parseFloat(improvementPercent) > 50 ? 'text-yellow-600' :
                    'text-orange-600'
                  }`}>
                    {parseFloat(improvementPercent) > 99 ? '✅ Excellent (>99%)' :
                     parseFloat(improvementPercent) > 90 ? '✓ Very Good (>90%)' :
                     parseFloat(improvementPercent) > 50 ? '⚠ Moderate (>50%)' :
                     '⚠ Low (<50%)'}
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Iterations Used:</span>
                  <span className="font-semibold text-gray-800">
                    {result.iterations_completed} / {result.iterations_completed}
                  </span>
                </div>
                {result.convergence_curve && result.convergence_curve.length > 10 && (
                  <div className="mt-3 pt-3 border-t border-blue-200">
                    <p className="text-xs text-gray-600 leading-relaxed">
                      <strong>How to interpret:</strong> The algorithm reduced the fitness from{' '}
                      <span className="font-mono bg-white px-1 rounded">{formatNumber(initialFitness)}</span> to{' '}
                      <span className="font-mono bg-white px-1 rounded">{formatNumber(finalFitness)}</span>.
                      {parseFloat(improvementPercent) > 99 ? (
                        <span className="text-green-700"> Near-perfect convergence indicates the solution is very close to the global optimum.</span>
                      ) : parseFloat(improvementPercent) > 90 ? (
                        <span className="text-blue-700"> Strong convergence indicates a high-quality solution was found.</span>
                      ) : (
                        <span className="text-orange-700"> Moderate convergence - consider increasing iterations or adjusting parameters for better results.</span>
                      )}
                    </p>
                  </div>
                )}
              </div>
            </div>

            {/* Metrics Grid */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
                <p className="text-xs text-gray-600 uppercase font-semibold mb-1">Initial Fitness</p>
                <p className="text-xl font-bold text-gray-800">{formatNumber(initialFitness)}</p>
              </div>
              <div className="bg-green-50 p-4 rounded-lg border border-green-200">
                <p className="text-xs text-gray-600 uppercase font-semibold mb-1">Final Fitness</p>
                <p className="text-xl font-bold text-green-600">{formatNumber(finalFitness)}</p>
              </div>
              <div className="bg-purple-50 p-4 rounded-lg border border-purple-200">
                <p className="text-xs text-gray-600 uppercase font-semibold mb-1">Total Reduction</p>
                <p className="text-xl font-bold text-purple-600">
                  {improvement !== null ? formatNumber(Math.abs(improvement)) : 'N/A'}
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Convergence Curve Card */}
      {hasConvergence && (
        <div className="bg-white rounded-xl shadow-md border-2 border-orange-200 overflow-hidden">
          <div className="bg-gradient-to-r from-orange-600 to-red-600 px-6 py-3">
            <h4 className="text-lg font-bold text-white flex items-center gap-2">
              <span>📈</span> Convergence Curve
            </h4>
          </div>
          <div className="p-6">
            <p className="text-sm text-gray-600 mb-4">
              Shows how the best fitness improved over {result.iterations_completed} iterations
            </p>
            
            {/* Simple ASCII-style visualization */}
            <div className="bg-gray-50 p-4 rounded-lg border border-gray-200 overflow-x-auto">
              <div className="font-mono text-xs space-y-1">
                {result.convergence_curve.filter((_, i) => i % Math.ceil(result.convergence_curve.length / 20) === 0 || i === result.convergence_curve.length - 1).map((fitness, idx, arr) => {
                  const maxFitness = Math.max(...result.convergence_curve);
                  const minFitness = Math.min(...result.convergence_curve);
                  const range = maxFitness - minFitness || 1;
                  const barWidth = Math.round(((maxFitness - fitness) / range) * 50);
                  
                  return (
                    <div key={idx} className="flex items-center gap-2">
                      <span className="text-gray-500 w-12 text-right">
                        {Math.round((idx / (arr.length - 1)) * result.iterations_completed)}
                      </span>
                      <span className="text-gray-400">│</span>
                      <div className="flex-1">
                        <div 
                          className="bg-gradient-to-r from-red-500 to-green-500 h-4 rounded"
                          style={{ width: `${Math.max(barWidth, 2)}%` }}
                        ></div>
                      </div>
                      <span className="text-gray-600 w-24">
                        {formatNumber(fitness)}
                      </span>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Data points summary */}
            <div className="mt-4 text-xs text-gray-500 flex gap-4">
              <span>🔴 Worse fitness</span>
              <span>🟢 Better fitness</span>
              <span className="ml-auto">Showing {Math.min(20, result.convergence_curve.length)} of {result.convergence_curve.length} iterations</span>
            </div>
          </div>
        </div>
      )}

      {/* Raw Data (Collapsible) */}
      <details className="bg-gray-50 rounded-lg border border-gray-300">
        <summary className="px-6 py-3 cursor-pointer font-semibold text-gray-700 hover:bg-gray-100">
          🔍 View Raw JSON Data
        </summary>
        <div className="px-6 pb-4">
          <pre className="text-xs text-gray-600 font-mono whitespace-pre-wrap bg-white p-4 rounded border border-gray-200 overflow-x-auto">
            {JSON.stringify(result, null, 2)}
          </pre>
        </div>
      </details>
    </div>
  );
}
