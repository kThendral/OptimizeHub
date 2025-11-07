import React from 'react';
import { Line } from 'react-chartjs-2';
import ResultsDisplay from './ResultsDisplay';

/**
 * AlgorithmComparisonView Component
 *
 * Displays results from multiple algorithms side-by-side for easy comparison.
 * Shows summary table, convergence comparison chart, and individual detailed results.
 */
export default function AlgorithmComparisonView({ results, onBack }) {
  if (!results || results.length === 0) {
    return (
      <div className="p-6 bg-yellow-50 border border-yellow-200 rounded-lg">
        <p className="text-yellow-800">No results available for comparison.</p>
      </div>
    );
  }

  // Get algorithm display name
  const getAlgoDisplayName = (algoKey) => {
    const nameMap = {
      'particle_swarm': 'PSO',
      'genetic_algorithm': 'GA',
      'simulated_annealing': 'SA',
      'ant_colony': 'ACOR',
      'differential_evolution': 'DE',
      'genetic': 'GA',
    };
    return nameMap[algoKey] || algoKey;
  };

  // Get full algorithm name
  const getFullAlgoName = (algoKey) => {
    const nameMap = {
      'particle_swarm': 'Particle Swarm Optimization',
      'genetic_algorithm': 'Genetic Algorithm',
      'simulated_annealing': 'Simulated Annealing',
      'ant_colony': 'Ant Colony Optimization',
      'differential_evolution': 'Differential Evolution',
      'genetic': 'Genetic Algorithm',
    };
    return nameMap[algoKey] || algoKey;
  };

  // Find best result based on objective
  const objective = results[0]?.objective || 'minimize';
  const bestResult = results.reduce((best, current) => {
    if (!best) return current;
    if (objective === 'minimize') {
      return current.best_fitness < best.best_fitness ? current : best;
    } else {
      return current.best_fitness > best.best_fitness ? current : best;
    }
  }, null);

  // Color palette for different algorithms
  const colors = [
    { bg: 'rgba(59, 130, 246, 0.2)', border: 'rgb(59, 130, 246)' },   // Blue
    { bg: 'rgba(16, 185, 129, 0.2)', border: 'rgb(16, 185, 129)' },   // Green
    { bg: 'rgba(245, 158, 11, 0.2)', border: 'rgb(245, 158, 11)' },   // Amber
    { bg: 'rgba(239, 68, 68, 0.2)', border: 'rgb(239, 68, 68)' },     // Red
    { bg: 'rgba(139, 92, 246, 0.2)', border: 'rgb(139, 92, 246)' },   // Purple
  ];

  // Prepare convergence comparison chart data
  const convergenceChartData = {
    labels: results[0]?.convergence_curve
      ? Array.from({ length: results[0].convergence_curve.length }, (_, i) => i)
      : [],
    datasets: results.map((result, index) => ({
      label: getFullAlgoName(result.algorithm),
      data: result.convergence_curve || [],
      borderColor: colors[index % colors.length].border,
      backgroundColor: colors[index % colors.length].bg,
      borderWidth: 2,
      tension: 0.1,
      pointRadius: 0,
      pointHoverRadius: 4,
    })),
  };

  const convergenceChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
        labels: {
          boxWidth: 12,
          padding: 15,
          font: { size: 11 },
        },
      },
      title: {
        display: true,
        text: 'Convergence Comparison',
        font: { size: 16, weight: 'bold' },
      },
      tooltip: {
        mode: 'index',
        intersect: false,
      },
    },
    scales: {
      y: {
        title: {
          display: true,
          text: 'Fitness Value',
        },
        beginAtZero: false,
      },
      x: {
        title: {
          display: true,
          text: 'Iteration',
        },
      },
    },
  };

  return (
    <div className="max-w-7xl mx-auto">
      {/* Header with back button */}
      <div className="mb-6">
        <button
          onClick={onBack}
          className="text-primary hover:underline mb-4 flex items-center gap-2"
        >
          ← Back to Configuration
        </button>

        <div className="flex items-center gap-3">
          <span className="text-3xl">📊</span>
          <div>
            <h2 className="text-2xl font-semibold text-primary">
              Algorithm Comparison Results
            </h2>
            <p className="text-sm text-gray-600">
              Comparing {results.length} algorithm{results.length > 1 ? 's' : ''} on the same problem
            </p>
          </div>
        </div>
      </div>

      {/* Summary Comparison Table */}
      <div className="mb-8 bg-white rounded-lg shadow-lg overflow-hidden border border-gray-200">
        <div className="bg-gradient-to-r from-blue-500 to-indigo-600 px-6 py-4">
          <h3 className="text-lg font-semibold text-white flex items-center gap-2">
            <span>📋</span>
            Performance Summary
          </h3>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Algorithm
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Best Fitness
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Iterations
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Execution Time
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Winner
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {results.map((result, index) => {
                const isWinner = result.algorithm === bestResult?.algorithm;
                return (
                  <tr
                    key={index}
                    className={`${
                      isWinner ? 'bg-green-50' : 'hover:bg-gray-50'
                    } transition-colors`}
                  >
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center gap-2">
                        <div
                          className="w-3 h-3 rounded-full"
                          style={{ backgroundColor: colors[index % colors.length].border }}
                        ></div>
                        <span className="text-sm font-medium text-gray-900">
                          {getFullAlgoName(result.algorithm)}
                        </span>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="text-sm text-gray-900 font-mono">
                        {result.best_fitness?.toExponential(4) || 'N/A'}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {result.iterations_completed || 'N/A'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {result.execution_time ? `${result.execution_time.toFixed(2)}s` : 'N/A'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      {isWinner && (
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                          🏆 Best
                        </span>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      {/* Convergence Comparison Chart */}
      {results.every(r => r.convergence_curve && r.convergence_curve.length > 0) && (
        <div className="mb-8 bg-white rounded-lg shadow-lg p-6 border border-gray-200">
          <div className="h-96">
            <Line data={convergenceChartData} options={convergenceChartOptions} />
          </div>
          <div className="mt-4 p-4 bg-blue-50 rounded-lg">
            <p className="text-sm text-gray-700">
              <strong>💡 Reading the Chart:</strong> The convergence curve shows how each algorithm's
              best fitness improves over iterations. Algorithms that reach lower values faster
              (for minimization) are more efficient. Look for steep drops early on and stable
              convergence toward the end.
            </p>
          </div>
        </div>
      )}

      {/* Individual Detailed Results */}
      <div className="mb-8">
        <h3 className="text-xl font-semibold text-gray-800 mb-4 flex items-center gap-2">
          <span>🔍</span>
          Detailed Individual Results
        </h3>
        <div className="space-y-6">
          {results.map((result, index) => {
            const isWinner = result.algorithm === bestResult?.algorithm;
            return (
              <div
                key={index}
                className={`border-2 rounded-lg overflow-hidden ${
                  isWinner ? 'border-green-500 shadow-lg' : 'border-gray-300'
                }`}
              >
                {/* Algorithm Header */}
                <div
                  className="px-6 py-4 flex items-center justify-between"
                  style={{
                    backgroundColor: isWinner ? 'rgb(240, 253, 244)' : colors[index % colors.length].bg,
                  }}
                >
                  <div className="flex items-center gap-3">
                    <div
                      className="w-4 h-4 rounded-full"
                      style={{ backgroundColor: colors[index % colors.length].border }}
                    ></div>
                    <h4 className="text-lg font-semibold text-gray-800">
                      {getFullAlgoName(result.algorithm)}
                    </h4>
                  </div>
                  {isWinner && (
                    <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-500 text-white">
                      🏆 Winner
                    </span>
                  )}
                </div>

                {/* Results Display */}
                <div className="p-6 bg-white">
                  <ResultsDisplay result={result} />
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Key Insights Section */}
      <div className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-lg p-6 border-2 border-purple-200">
        <h3 className="text-lg font-semibold text-gray-800 mb-3 flex items-center gap-2">
          <span>💡</span>
          Key Insights
        </h3>
        <ul className="space-y-2 text-sm text-gray-700">
          <li className="flex items-start gap-2">
            <span className="text-green-600 font-bold mt-0.5">✓</span>
            <span>
              <strong>Best Performer:</strong> {getFullAlgoName(bestResult?.algorithm)} achieved the{' '}
              {objective === 'minimize' ? 'lowest' : 'highest'} fitness value of{' '}
              {bestResult?.best_fitness?.toExponential(4)}.
            </span>
          </li>
          <li className="flex items-start gap-2">
            <span className="text-blue-600 font-bold mt-0.5">ℹ</span>
            <span>
              <strong>Fastest Convergence:</strong> Look at the convergence chart to see which algorithm
              reached near-optimal solutions fastest.
            </span>
          </li>
          <li className="flex items-start gap-2">
            <span className="text-purple-600 font-bold mt-0.5">⚡</span>
            <span>
              <strong>Efficiency:</strong> Compare execution times to understand the computational cost
              of each algorithm for this problem.
            </span>
          </li>
        </ul>
      </div>
    </div>
  );
}
