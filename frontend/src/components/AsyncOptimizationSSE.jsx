import { useState, useEffect, useRef } from 'react';
import { submitAsyncOptimization } from '../api/index.js';
import { useTaskStream } from '../hooks/useTaskStream.js';
import ResultsDisplay from './ResultsDisplay';
import AlgorithmComparisonView from './AlgorithmComparisonView';

/**
 * AsyncOptimizationSSE Component (with Server-Sent Events)
 *
 * Enhanced version using SSE for real-time updates instead of polling.
 * Provides better UX with instant status updates.
 *
 * Flow:
 * 1. Submit job to Celery queue
 * 2. Subscribe to SSE stream for each task
 * 3. Receive real-time updates
 * 4. Display results when complete
 */
export default function AsyncOptimizationSSE({
  problem,
  algorithms,
  params,
  onBack
}) {
  // Task state
  const [taskIds, setTaskIds] = useState([]);
  const [groupId, setGroupId] = useState(null);
  const [error, setError] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showResults, setShowResults] = useState(false);
  const [completedResults, setCompletedResults] = useState([]);

  // Ref to track if we've shown notification
  const hasShownNotification = useRef(false);

  // Submit async job on mount
  useEffect(() => {
    submitJob();
  }, []);

  const submitJob = async () => {
    setIsSubmitting(true);
    setError(null);

    try {
      // Submit to async endpoint - returns group_id and task_ids
      const response = await submitAsyncOptimization(problem, algorithms, params);

      setGroupId(response.group_id);
      setTaskIds(response.task_ids);
    } catch (err) {
      setError(`Failed to submit async job: ${err.message}`);
    } finally {
      setIsSubmitting(false);
    }
  };

  // Get status badge color
  const getStatusColor = (state) => {
    switch (state) {
      case 'PENDING':
        return 'bg-yellow-100 text-yellow-800 border-yellow-300';
      case 'STARTED':
        return 'bg-blue-100 text-blue-800 border-blue-300';
      case 'SUCCESS':
        return 'bg-green-100 text-green-800 border-green-300';
      case 'FAILURE':
        return 'bg-red-100 text-red-800 border-red-300';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-300';
    }
  };

  // Get status icon
  const getStatusIcon = (state) => {
    switch (state) {
      case 'PENDING':
        return '⏳';
      case 'STARTED':
        return '🔄';
      case 'SUCCESS':
        return '✅';
      case 'FAILURE':
        return '❌';
      default:
        return '❓';
    }
  };

  // Algorithm name mapping for display
  const getAlgorithmDisplayName = (algoKey) => {
    const nameMap = {
      'particle_swarm': 'Particle Swarm Optimization (PSO)',
      'genetic_algorithm': 'Genetic Algorithm (GA)',
      'simulated_annealing': 'Simulated Annealing (SA)',
      'ant_colony': 'Ant Colony Optimization (ACOR)',
      'differential_evolution': 'Differential Evolution'
    };
    return nameMap[algoKey] || algoKey;
  };

  // Normalize algorithm display (DE -> "Differential Evolution")
  const normalizeDisplay = (display, algorithmKey) => {
    if (display && (/^DE(?:\/|$)/i).test(display)) return 'Differential Evolution';
    if (typeof algorithmKey === 'string' && algorithmKey.toLowerCase().includes('differential')) return 'Differential Evolution';
    return display || null;
  };

  // Copy task ID to clipboard
  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
  };

  // Transform Celery result to match ResultsDisplay expected format
  const transformResult = (celeryResult, algorithmName) => {
    // Celery returns: { algo, status, result: { best_solution, best_fitness, ... } }
    // ResultsDisplay expects: { algorithm, best_solution, best_fitness, ... }

    if (!celeryResult) return null;

    // Prefer normalized inner result if present
    const inner = celeryResult.result || celeryResult;

    // Determine algorithm display: prefer algorithm_display -> inner.algorithm -> provided algorithmName
    const algoDisplay = (inner && (inner.algorithm_display || (typeof inner.algorithm === 'string' && inner.algorithm))) || algorithmName;

    // Ensure iterations and execution_time keys are available at top-level for ResultsDisplay
    const iterations = inner.iterations_completed ?? inner.iterations ?? inner.params?.max_iterations ?? (inner.convergence_curve ? inner.convergence_curve.length : undefined);
    const execTime = inner.execution_time ?? inner.elapsed_time ?? inner.runtime ?? null;

    return {
      algorithm: algoDisplay,
      algorithm_display: algoDisplay,
      iterations: iterations,
      iterations_completed: iterations,
      execution_time: execTime,
      ...inner,
    };
  };

  // Show browser notification when all tasks complete
  const showCompletionNotification = (completedCount, totalCount) => {
    if ('Notification' in window && Notification.permission === 'granted') {
      new Notification('OptimizeHub - Tasks Complete! 🎉', {
        body: `${completedCount} of ${totalCount} algorithm${totalCount > 1 ? 's' : ''} finished running. Click to view results.`,
        icon: '/favicon.ico',
      });
    }
  };

  // Request notification permission on mount
  useEffect(() => {
    if ('Notification' in window && Notification.permission === 'default') {
      Notification.requestPermission();
    }
  }, []);

  // If showing results comparison view
  if (showResults && completedResults.length > 0) {
    return (
      <AlgorithmComparisonView
        results={completedResults}
        onBack={() => setShowResults(false)}
      />
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-6">
        <button
          onClick={onBack}
          className="text-primary hover:underline mb-4 flex items-center gap-2"
        >
          ← Back to Configuration
        </button>

        <h2 className="text-2xl font-semibold text-primary mb-2">
          Async Optimization (Real-time)
        </h2>
        <p className="text-gray-600 text-sm">
          Your optimization tasks are running in the background with real-time updates via SSE.
        </p>
      </div>

      {/* Error Display */}
      {error && (
        <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
          <strong>Error:</strong> {error}
        </div>
      )}

      {/* Submitting State */}
      {isSubmitting && (
        <div className="mb-6 p-6 bg-blue-50 border border-blue-200 rounded-lg text-center">
          <div className="text-4xl mb-3">⏳</div>
          <p className="text-gray-700">Submitting tasks to queue...</p>
        </div>
      )}

      {/* Group ID Display */}
      {groupId && (
        <div className="mb-4 p-4 bg-gray-50 border border-gray-200 rounded-lg">
          <div className="flex items-center justify-between">
            <div>
              <span className="text-sm font-medium text-gray-600">Group ID:</span>
              <code className="ml-2 text-xs bg-white px-2 py-1 rounded border border-gray-300 font-mono">
                {groupId}
              </code>
            </div>
            <button
              onClick={() => copyToClipboard(groupId)}
              className="text-xs text-primary hover:underline"
            >
              Copy
            </button>
          </div>
        </div>
      )}

      {/* Task Status Cards with SSE */}
      {taskIds.length > 0 && (
        <div className="space-y-4 mb-6">
          {taskIds.map((taskId, index) => (
            <TaskCard
              key={taskId}
              taskId={taskId}
              algorithm={algorithms[index]}
              getStatusColor={getStatusColor}
              getStatusIcon={getStatusIcon}
              getAlgorithmDisplayName={getAlgorithmDisplayName}
              copyToClipboard={copyToClipboard}
              transformResult={transformResult}
              onTaskComplete={(result) => {
                // Add to completed results
                setCompletedResults(prev => {
                  const updated = [...prev, result];

                  // Check if all tasks are complete
                  if (updated.length === taskIds.length && !hasShownNotification.current) {
                    hasShownNotification.current = true;
                    showCompletionNotification(updated.length, taskIds.length);
                  }

                  return updated;
                });
              }}
            />
          ))}
        </div>
      )}

      {/* View Results Button (shown when at least one task completes) */}
      {completedResults.length > 0 && (
        <div className="sticky bottom-0 p-4 bg-gradient-to-r from-green-500 to-emerald-600 rounded-lg shadow-lg border-2 border-green-400">
          <div className="flex items-center justify-between">
            <div className="text-white">
              <div className="flex items-center gap-2 mb-1">
                <span className="text-2xl">🎉</span>
                <h3 className="text-lg font-semibold">
                  {completedResults.length === taskIds.length
                    ? 'All Tasks Complete!'
                    : `${completedResults.length} of ${taskIds.length} Tasks Complete`}
                </h3>
              </div>
              <p className="text-sm text-green-50">
                {completedResults.length === 1
                  ? 'Results are ready to view'
                  : 'Results are ready for comparison'}
              </p>
            </div>
            <button
              onClick={() => setShowResults(true)}
              className="px-6 py-3 bg-white text-green-600 font-semibold rounded-lg shadow-md hover:bg-green-50 transition-all duration-200 flex items-center gap-2"
            >
              <span>📊</span>
              <span>View {completedResults.length > 1 ? 'Comparison' : 'Results'}</span>
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

/**
 * Individual Task Card Component with SSE
 *
 * Uses useTaskStream hook to subscribe to real-time updates for a single task.
 */
function TaskCard({
  taskId,
  algorithm,
  getStatusColor,
  getStatusIcon,
  getAlgorithmDisplayName,
  copyToClipboard,
  transformResult,
  onTaskComplete
}) {
  // Subscribe to SSE stream for this task
  const { status, result, error, isConnected } = useTaskStream(taskId);

  // Track if we've already called onTaskComplete for this task
  const hasNotifiedRef = useRef(false);

  // When task completes successfully, transform and notify parent
  useEffect(() => {
    if (status === 'SUCCESS' && result && !hasNotifiedRef.current) {
      hasNotifiedRef.current = true;
      const transformedResult = transformResult(result, algorithm);
      if (transformedResult) {
        onTaskComplete(transformedResult);
      }
    }
  }, [status, result, algorithm, transformResult, onTaskComplete]);

  return (
    <div className="p-4 bg-white border-2 border-gray-200 rounded-lg shadow-sm">
      {/* Task Header */}
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-3">
          <span className="text-2xl">{getStatusIcon(status)}</span>
          <div>
            <h3 className="font-semibold text-gray-800">
              {normalizeDisplay(result?.algorithm_display, result?.algorithm) || getAlgorithmDisplayName(algorithm)}
            </h3>
            <div className="flex items-center gap-2 mt-1">
              <span className="text-xs text-gray-500">Task ID:</span>
              <code className="text-xs bg-gray-100 px-2 py-0.5 rounded font-mono">
                {taskId.substring(0, 8)}...
              </code>
              <button
                onClick={() => copyToClipboard(taskId)}
                className="text-xs text-primary hover:underline"
              >
                Copy Full ID
              </button>
            </div>
          </div>
        </div>

        {/* Status Badge */}
        <div className="flex flex-col items-end gap-1">
          <span
            className={`px-3 py-1 rounded-full text-sm font-medium border ${getStatusColor(
              status
            )}`}
          >
            {status}
          </span>
          {/* Connection Indicator */}
          {isConnected && status !== 'SUCCESS' && status !== 'FAILURE' && (
            <span className="flex items-center gap-1 text-xs text-green-600">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
              Live
            </span>
          )}
        </div>
      </div>

      {/* Loading Spinner for Running Tasks */}
      {(status === 'PENDING' || status === 'STARTED') && (
        <div className="flex items-center gap-2 text-sm text-gray-600">
          <div className="animate-spin h-4 w-4 border-2 border-primary border-t-transparent rounded-full"></div>
          <span>
            {status === 'PENDING' ? 'Waiting in queue...' : 'Running optimization...'}
          </span>
          <span className="text-xs text-gray-500">(real-time updates)</span>
        </div>
      )}

      {/* Success - Show Summary */}
      {status === 'SUCCESS' && result && (
        <div className="mt-3 p-3 bg-green-50 border border-green-200 rounded">
          <div className="flex items-center gap-2 mb-2">
            <span className="text-green-600 font-semibold">✓ Completed Successfully</span>
          </div>
            <div className="text-sm text-gray-700 space-y-1">
            <div className="flex justify-between">
              <span className="text-gray-600">Best Fitness:</span>
              <span className="font-mono font-semibold">
                {(result?.best_fitness)?.toExponential
                  ? (result?.best_fitness).toExponential(4)
                  : ((result?.best_fitness) ?? 'N/A')}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Iterations:</span>
              <span className="font-medium">
                {result?.iterations_completed ?? result?.iterations ?? 'N/A'}
              </span>
            </div>
          </div>
          <p className="text-xs text-gray-500 mt-2 italic">
            Click "View Results" below to see detailed analysis and charts
          </p>
        </div>
      )}

      {/* Failure - Show Error */}
      {status === 'FAILURE' && error && (
        <div className="mt-3 p-3 bg-red-50 border border-red-200 rounded text-sm">
          <strong className="text-red-700">Task Failed:</strong>
          <pre className="mt-2 text-xs text-red-600 whitespace-pre-wrap">
            {typeof error === 'string' ? error : JSON.stringify(error, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}
