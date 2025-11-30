import React from 'react';
import ConvergenceChart from './charts/ConvergenceChart';
import SolutionSpaceChart from './charts/SolutionSpaceChart';
import MetricsBarChart from './charts/MetricsBarChart';
import SolutionRadarChart from './charts/SolutionRadarChart';
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
  const objective = result.problem?.objective || 'minimize';
  const isMaximize = objective === 'maximize';

  // For minimize: improvement = initial - final (positive when final < initial)
  // For maximize: improvement = final - initial (positive when final > initial)
  const improvement = initialFitness && finalFitness !== null
    ? (isMaximize ? finalFitness - initialFitness : initialFitness - finalFitness)
    : null;
  const improvementPercent = initialFitness && improvement !== null && initialFitness !== 0
    ? ((improvement / Math.abs(initialFitness)) * 100).toFixed(2)
    : null;

  // Get algorithm display name
  const getAlgoName = (algo) => {
    const names = {
      'ParticleSwarmOptimization': 'Particle Swarm Optimization (PSO)',
      'GeneticAlgorithm': 'Genetic Algorithm (GA)',
      'DifferentialEvolution': 'Differential Evolution',
      'AntColonyOptimization': 'Ant Colony Optimization (ACOR)',
      'particle_swarm': 'Particle Swarm Optimization (PSO)',
      'genetic_algorithm': 'Genetic Algorithm (GA)',
      'differential_evolution': 'Differential Evolution',
      
      'ant_colony': 'Ant Colony Optimization (ACOR)',
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

  // Get dynamic interpretation for metrics
  const getMetricInterpretation = (metricType, value, context) => {
    const { objective, improvementPercent, algorithm, problemType } = context;
    const isMinimize = objective !== 'maximize';
    const improvePct = parseFloat(improvementPercent) || 0;

    // Helper to get algorithm-specific suggestions
    const getAlgorithmSuggestion = (algoName) => {
      if (algoName?.includes('PSO') || algoName?.includes('Particle')) {
        return 'Try increasing swarm_size or adjusting w (inertia).';
      } else if (algoName?.includes('GA') || algoName?.includes('Genetic')) {
        return 'Try increasing population_size or mutation_rate.';
      } else if (algoName?.includes('ACOR') || algoName?.includes('Ant Colony')) {
        return 'Try increasing archive_size or adjusting q parameter.';
      } else if (algoName?.includes('DE') || algoName?.includes('Differential')) {
        return 'Try adjusting F (scaling factor) or increasing population.';
      }
      return 'Try increasing max_iterations or adjusting parameters.';
    };

    if (metricType === 'initial') {
      // Initial Fitness Interpretation
      if (problemType === 'tsp') {
        return {
          icon: '🗺️',
          text: 'Starting route distance before optimization.',
          color: 'text-blue-600'
        };
      } else if (problemType === 'knapsack') {
        return {
          icon: '🎒',
          text: 'Initial value before optimizing item selection.',
          color: 'text-blue-600'
        };
      } else if (value === null) {
        return { icon: 'ℹ️', text: 'No initial value available.', color: 'text-gray-500' };
      }

      const absValue = Math.abs(value);
      if (absValue > 1000) {
        return {
          icon: '🎯',
          text: 'Started far from optimum. Good room for improvement.',
          color: 'text-blue-600'
        };
      } else if (absValue > 10) {
        return {
          icon: '📍',
          text: 'Moderate starting point in the search space.',
          color: 'text-blue-600'
        };
      } else if (absValue > 0.1) {
        return {
          icon: '✨',
          text: 'Started relatively close to the optimal region.',
          color: 'text-blue-600'
        };
      } else {
        return {
          icon: '🎲',
          text: 'Very close starting point - good initialization.',
          color: 'text-blue-600'
        };
      }
    } else if (metricType === 'final') {
      // Final Fitness Interpretation
      if (problemType === 'tsp') {
        if (improvePct > 50) {
          return {
            icon: '✅',
            text: `Route optimized by ${improvePct.toFixed(1)}% - excellent pathfinding!`,
            color: 'text-green-600'
          };
        } else {
          return {
            icon: '⚠️',
            text: `Limited route improvement. ${getAlgorithmSuggestion(algorithm)}`,
            color: 'text-orange-600'
          };
        }
      } else if (problemType === 'knapsack') {
        if (improvePct > 50) {
          return {
            icon: '💰',
            text: `Value increased by ${improvePct.toFixed(1)}% - great optimization!`,
            color: 'text-green-600'
          };
        } else {
          return {
            icon: '⚠️',
            text: `Small value improvement. ${getAlgorithmSuggestion(algorithm)}`,
            color: 'text-orange-600'
          };
        }
      } else if (value === null) {
        return { icon: 'ℹ️', text: 'No final value available.', color: 'text-gray-500' };
      }

      const absValue = Math.abs(value);
      if (isMinimize) {
        if (absValue < 0.001) {
          return {
            icon: '🎯',
            text: 'Excellent! Nearly reached global optimum (0).',
            color: 'text-green-600'
          };
        } else if (absValue < 0.1) {
          return {
            icon: '✓',
            text: 'Very good result - close to optimum.',
            color: 'text-green-600'
          };
        } else if (absValue < 10) {
          return {
            icon: '📊',
            text: improvePct > 90 ? 'Good convergence achieved.' : 'Decent result, but could improve further.',
            color: improvePct > 90 ? 'text-blue-600' : 'text-yellow-600'
          };
        } else {
          return {
            icon: '⚠️',
            text: `Didn't converge well. ${getAlgorithmSuggestion(algorithm)}`,
            color: 'text-orange-600'
          };
        }
      } else {
        // Maximize - judge based on improvement percentage
        if (improvePct > 90) {
          return {
            icon: '🎯',
            text: `Excellent maximization! ${improvePct.toFixed(1)}% increase achieved.`,
            color: 'text-green-600'
          };
        } else if (improvePct > 50) {
          return {
            icon: '✓',
            text: `Good maximum found with ${improvePct.toFixed(1)}% improvement.`,
            color: 'text-green-600'
          };
        } else if (improvePct > 0) {
          return {
            icon: '📊',
            text: `Moderate maximization (${improvePct.toFixed(1)}%). Could improve further.`,
            color: 'text-yellow-600'
          };
        } else {
          return {
            icon: '⚠️',
            text: `Poor maximization. ${getAlgorithmSuggestion(algorithm)}`,
            color: 'text-orange-600'
          };
        }
      }
    } else if (metricType === 'reduction') {
      // Total Improvement/Reduction Interpretation
      const actionWord = isMinimize ? 'reduced' : 'increased';
      const nounWord = isMinimize ? 'reduction' : 'increase';

      if (problemType === 'tsp') {
        return {
          icon: improvePct > 50 ? '🚀' : '📉',
          text: improvePct > 50
            ? `Distance ${actionWord} by ${improvePct.toFixed(1)}% - efficient routing!`
            : `Only ${improvePct.toFixed(1)}% improvement. Try more iterations.`,
          color: improvePct > 50 ? 'text-purple-600' : 'text-orange-600'
        };
      } else if (problemType === 'knapsack') {
        return {
          icon: improvePct > 50 ? '💎' : '📉',
          text: improvePct > 50
            ? `Value improved by ${improvePct.toFixed(1)}% - great selection!`
            : `Small value gain of ${improvePct.toFixed(1)}%. Adjust parameters.`,
          color: improvePct > 50 ? 'text-purple-600' : 'text-orange-600'
        };
      } else if (value === null) {
        return { icon: 'ℹ️', text: 'No improvement data available.', color: 'text-gray-500' };
      }

      // Handle negative improvement (algorithm performed poorly)
      if (improvePct < 0) {
        return {
          icon: '❌',
          text: isMinimize
            ? `Fitness increased by ${Math.abs(improvePct).toFixed(1)}% instead of decreasing. Algorithm failed to minimize.`
            : `Fitness decreased by ${Math.abs(improvePct).toFixed(1)}% instead of increasing. Algorithm failed to maximize.`,
          color: 'text-red-600'
        };
      }

      if (improvePct > 99) {
        return {
          icon: '🌟',
          text: `${isMinimize ? 'Reduced' : 'Increased'} by ${improvePct.toFixed(2)}% - near-perfect optimization!`,
          color: 'text-purple-600'
        };
      } else if (improvePct > 95) {
        return {
          icon: '✨',
          text: `${isMinimize ? 'Reduced' : 'Increased'} by ${improvePct.toFixed(1)}% - excellent convergence.`,
          color: 'text-purple-600'
        };
      } else if (improvePct > 80) {
        return {
          icon: '✓',
          text: `Good ${improvePct.toFixed(1)}% ${nounWord}. Algorithm performed well.`,
          color: 'text-blue-600'
        };
      } else if (improvePct > 50) {
        return {
          icon: '📊',
          text: `Moderate ${improvePct.toFixed(1)}% improvement. Consider more iterations.`,
          color: 'text-yellow-600'
        };
      } else if (improvePct > 20) {
        return {
          icon: '⚠️',
          text: `Low ${improvePct.toFixed(1)}% improvement. ${getAlgorithmSuggestion(algorithm)}`,
          color: 'text-orange-600'
        };
      } else if (improvePct > 0) {
        return {
          icon: '⚠️',
          text: `Very low ${improvePct.toFixed(1)}% improvement. Increase max_iterations significantly.`,
          color: 'text-red-600'
        };
      } else {
        return {
          icon: 'ℹ️',
          text: 'No improvement detected.',
          color: 'text-gray-500'
        };
      }
    }

    return { icon: 'ℹ️', text: '', color: 'text-gray-500' };
  };

  const downloadResultsAsJSON = () => {
    const dataStr = JSON.stringify(result, null, 2);
    const blob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `optimization_results_${new Date().toISOString()}.json`;
    link.click();
    URL.revokeObjectURL(url);
  };

  const downloadResultsAsCSV = () => {
    const { convergence_curve, best_solution } = result;
    
    let csvContent = 'Iteration,Fitness\n';
    if (convergence_curve) {
      convergence_curve.forEach((fitness, index) => {
        csvContent += `${index + 1},${fitness}\n`;
      });
    }
    
    csvContent += '\nBest Solution\n';
    csvContent += 'Dimension,Value\n';
    if (best_solution) {
      best_solution.forEach((value, index) => {
        csvContent += `${index + 1},${value}\n`;
      });
    }
    
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `optimization_results_${new Date().toISOString()}.csv`;
    link.click();
    URL.revokeObjectURL(url);
  };

   // Extract problem configuration for charts
  const problemConfig = {
    bounds: result.problem?.bounds || (result.best_solution ? result.best_solution.map(() => [-5, 5]) : []),
    fitness_function_name: result.problem?.fitness_function || 'unknown'
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
                    parseFloat(improvementPercent) < 0 ? 'text-red-600' :
                    parseFloat(improvementPercent) > 99 ? 'text-green-600' :
                    parseFloat(improvementPercent) > 90 ? 'text-blue-600' :
                    parseFloat(improvementPercent) > 50 ? 'text-yellow-600' :
                    'text-orange-600'
                  }`}>
                    {parseFloat(improvementPercent) < 0 ? '❌ Failed (negative improvement)' :
                     parseFloat(improvementPercent) > 99 ? '✅ Excellent (>99%)' :
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
                      <strong>How to interpret:</strong> The algorithm {isMaximize ? 'increased' : 'reduced'} the fitness from{' '}
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
              {/* Initial Fitness */}
              <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
                <p className="text-xs text-gray-600 uppercase font-semibold mb-1">Initial Fitness</p>
                <p className="text-xl font-bold text-gray-800 mb-2">{formatNumber(initialFitness)}</p>
                {(() => {
                  const interpretation = getMetricInterpretation('initial', initialFitness, {
                    objective: result.problem?.objective || 'minimize',
                    improvementPercent,
                    algorithm: getAlgoName(result.algorithm),
                    problemType: result.problem_type
                  });
                  return (
                    <div className={`flex items-start gap-1 text-xs ${interpretation.color} mt-2 pt-2 border-t border-blue-300`}>
                      <span className="text-sm">{interpretation.icon}</span>
                      <p className="leading-tight">{interpretation.text}</p>
                    </div>
                  );
                })()}
              </div>

              {/* Final Fitness */}
              <div className="bg-green-50 p-4 rounded-lg border border-green-200">
                <p className="text-xs text-gray-600 uppercase font-semibold mb-1">Final Fitness</p>
                <p className="text-xl font-bold text-green-600 mb-2">{formatNumber(finalFitness)}</p>
                {(() => {
                  const interpretation = getMetricInterpretation('final', finalFitness, {
                    objective: result.problem?.objective || 'minimize',
                    improvementPercent,
                    algorithm: getAlgoName(result.algorithm),
                    problemType: result.problem_type
                  });
                  return (
                    <div className={`flex items-start gap-1 text-xs ${interpretation.color} mt-2 pt-2 border-t border-green-300`}>
                      <span className="text-sm">{interpretation.icon}</span>
                      <p className="leading-tight">{interpretation.text}</p>
                    </div>
                  );
                })()}
              </div>

              {/* Total Improvement/Reduction */}
              <div className="bg-purple-50 p-4 rounded-lg border border-purple-200">
                <p className="text-xs text-gray-600 uppercase font-semibold mb-1">
                  {isMaximize ? 'Total Increase' : 'Total Reduction'}
                </p>
                <p className="text-xl font-bold text-purple-600 mb-2">
                  {improvement !== null ? formatNumber(Math.abs(improvement)) : 'N/A'}
                </p>
                {(() => {
                  const interpretation = getMetricInterpretation('reduction', improvement, {
                    objective: result.problem?.objective || 'minimize',
                    improvementPercent,
                    algorithm: getAlgoName(result.algorithm),
                    problemType: result.problem_type
                  });
                  return (
                    <div className={`flex items-start gap-1 text-xs ${interpretation.color} mt-2 pt-2 border-t border-purple-300`}>
                      <span className="text-sm">{interpretation.icon}</span>
                      <p className="leading-tight">{interpretation.text}</p>
                    </div>
                  );
                })()}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Interactive Charts Section */}
      {hasConvergence && (
        <div className="space-y-8">
          {/* Charts Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Convergence Chart - Always show */}
            <div className="lg:col-span-2">
              <ConvergenceChart 
                convergenceData={result.convergence_curve} 
                algorithmName={getAlgoName(result.algorithm)}
              />
            </div>

            {/* Metrics Bar Chart */}
            <MetricsBarChart 
              results={result} 
              algorithmName={getAlgoName(result.algorithm)}
            />

            {/* Solution Radar Chart */}
            {result.best_solution && result.best_solution.length > 0 && (
              <SolutionRadarChart 
                bestSolution={result.best_solution}
                bounds={problemConfig.bounds}
              />
            )}

            {/* Solution Space Chart (2D visualization) */}
            {result.best_solution && result.best_solution.length >= 2 && (
              <div className="lg:col-span-2">
                <SolutionSpaceChart 
                  bestSolution={result.best_solution}
                  bounds={problemConfig.bounds}
                  fitnessFunction={problemConfig.fitness_function_name}
                />
              </div>
            )}
          </div>
        </div>
      )}

      {/* Export Options */}
      <div className="bg-white p-6 rounded-lg shadow-lg border border-gray-200 no-print">
        <h3 className="text-lg font-bold text-purple-600 mb-4">Export Options</h3>
        <div className="flex flex-wrap gap-4">
          <button
            onClick={downloadResultsAsJSON}
            className="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 transition-colors flex items-center gap-2"
          >
            📊 Download JSON
          </button>
          <button
            onClick={downloadResultsAsCSV}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors flex items-center gap-2"
          >
            📈 Download CSV
          </button>
          <button
            onClick={() => window.print()}
            className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors flex items-center gap-2"
          >
            🖨️ Print Report
          </button>
        </div>
      </div>

      {/* Raw Data (Collapsible) */}
      <details className="bg-gray-50 rounded-lg border border-gray-300 no-print">
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
};