import { useState, useEffect } from 'react';
import { submitAsyncOptimization } from '../api/index.js';
import { useTaskStream } from '../hooks/useTaskStream.js';
import ResultsDisplay from './ResultsDisplay';

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
      'differential_evolution': 'Differential Evolution (DE)'
    };
    return nameMap[algoKey] || algoKey;
  };

  // Copy task ID to clipboard
  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
  };

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
            />
          ))}
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
  copyToClipboard
}) {
  // Subscribe to SSE stream for this task
  const { status, result, error, isConnected } = useTaskStream(taskId);

  return (
    <div className="p-4 bg-white border-2 border-gray-200 rounded-lg shadow-sm">
      {/* Task Header */}
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-3">
          <span className="text-2xl">{getStatusIcon(status)}</span>
          <div>
            <h3 className="font-semibold text-gray-800">
              {getAlgorithmDisplayName(algorithm)}
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

      {/* Success - Show Results */}
      {status === 'SUCCESS' && result && (
        <div className="mt-3">
          <ResultsDisplay result={result} compact={true} />
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
