import { useState, useEffect } from 'react';
import { submitAsyncOptimization, getTaskStatus } from '../api/index.js';
import ResultsDisplay from './ResultsDisplay';

/**
 * AsyncOptimization Component
 *
 * Handles async optimization workflow:
 * 1. Submit job to Celery queue
 * 2. Poll task status every 2 seconds
 * 3. Display results when complete
 * 4. Show errors if task fails
 */
export default function AsyncOptimization({
  problem,
  algorithms,
  params,
  onBack
}) {
  // Task state
  const [taskIds, setTaskIds] = useState([]);
  const [groupId, setGroupId] = useState(null);
  const [taskStatuses, setTaskStatuses] = useState({});
  const [isPolling, setIsPolling] = useState(false);
  const [error, setError] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Track which tasks have completed
  const [completedTasks, setCompletedTasks] = useState(new Set());

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

      // Initialize task statuses
      const initialStatuses = {};
      response.task_ids.forEach((id, index) => {
        initialStatuses[id] = {
          algorithm: algorithms[index],
          state: 'PENDING',
          result: null,
          error: null
        };
      });
      setTaskStatuses(initialStatuses);

      // Start polling
      setIsPolling(true);
    } catch (err) {
      setError(`Failed to submit async job: ${err.message}`);
    } finally {
      setIsSubmitting(false);
    }
  };

  // Polling logic - check status every 2 seconds
  useEffect(() => {
    if (!isPolling || taskIds.length === 0) return;

    const interval = setInterval(async () => {
      // Check if all tasks are complete
      if (completedTasks.size === taskIds.length) {
        setIsPolling(false);
        clearInterval(interval);
        return;
      }

      // Poll each task that hasn't completed
      const updates = {};

      for (const taskId of taskIds) {
        if (completedTasks.has(taskId)) continue;

        try {
          const status = await getTaskStatus(taskId);

          updates[taskId] = {
            ...taskStatuses[taskId],
            state: status.state,
            result: status.result || null,
            error: status.result || null // Error details in result field when FAILURE
          };

          // Mark as completed if SUCCESS or FAILURE
          if (status.state === 'SUCCESS' || status.state === 'FAILURE') {
            setCompletedTasks(prev => new Set([...prev, taskId]));
          }
        } catch (err) {
          console.error(`Error polling task ${taskId}:`, err);
          updates[taskId] = {
            ...taskStatuses[taskId],
            state: 'FAILURE',
            error: `Polling error: ${err.message}`
          };
          setCompletedTasks(prev => new Set([...prev, taskId]));
        }
      }

      // Update all statuses at once
      setTaskStatuses(prev => ({ ...prev, ...updates }));
    }, 2000); // Poll every 2 seconds

    return () => clearInterval(interval);
  }, [isPolling, taskIds, completedTasks, taskStatuses]);

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

  // Check if all tasks are complete
  const allTasksComplete = completedTasks.size === taskIds.length && taskIds.length > 0;

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
          Async Optimization
        </h2>
        <p className="text-gray-600 text-sm">
          Your optimization tasks are running in the background. You can monitor progress below.
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

      {/* Task Status Cards */}
      {taskIds.length > 0 && (
        <div className="space-y-4 mb-6">
          {taskIds.map((taskId, index) => {
            const status = taskStatuses[taskId];
            if (!status) return null;

            return (
              <div
                key={taskId}
                className="p-4 bg-white border-2 border-gray-200 rounded-lg shadow-sm"
              >
                {/* Task Header */}
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-3">
                    <span className="text-2xl">{getStatusIcon(status.state)}</span>
                    <div>
                      <h3 className="font-semibold text-gray-800">
                        {getAlgorithmDisplayName(status.algorithm)}
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
                  <span
                    className={`px-3 py-1 rounded-full text-sm font-medium border ${getStatusColor(
                      status.state
                    )}`}
                  >
                    {status.state}
                  </span>
                </div>

                {/* Loading Spinner for Running Tasks */}
                {(status.state === 'PENDING' || status.state === 'STARTED') && (
                  <div className="flex items-center gap-2 text-sm text-gray-600">
                    <div className="animate-spin h-4 w-4 border-2 border-primary border-t-transparent rounded-full"></div>
                    <span>
                      {status.state === 'PENDING' ? 'Waiting in queue...' : 'Running optimization...'}
                    </span>
                  </div>
                )}

                {/* Success - Show Results */}
                {status.state === 'SUCCESS' && status.result && (
                  <div className="mt-3">
                    <ResultsDisplay result={status.result} compact={true} />
                  </div>
                )}

                {/* Failure - Show Error */}
                {status.state === 'FAILURE' && (
                  <div className="mt-3 p-3 bg-red-50 border border-red-200 rounded text-sm">
                    <strong className="text-red-700">Task Failed:</strong>
                    <pre className="mt-2 text-xs text-red-600 whitespace-pre-wrap">
                      {typeof status.error === 'string'
                        ? status.error
                        : JSON.stringify(status.error, null, 2)}
                    </pre>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}

      {/* All Tasks Complete Message */}
      {allTasksComplete && (
        <div className="p-6 bg-green-50 border border-green-200 rounded-lg text-center">
          <div className="text-4xl mb-3">🎉</div>
          <h3 className="text-lg font-semibold text-green-800 mb-2">
            All Tasks Completed!
          </h3>
          <p className="text-sm text-green-700">
            {completedTasks.size} of {taskIds.length} tasks finished successfully.
          </p>
        </div>
      )}

      {/* Polling Indicator */}
      {isPolling && !allTasksComplete && (
        <div className="mt-4 text-center text-sm text-gray-500">
          <div className="flex items-center justify-center gap-2">
            <div className="animate-pulse h-2 w-2 bg-primary rounded-full"></div>
            <span>Polling for updates every 2 seconds...</span>
          </div>
        </div>
      )}
    </div>
  );
}
