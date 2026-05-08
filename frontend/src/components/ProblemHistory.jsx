import { useState, useEffect } from 'react';
import { persistenceAPI } from '../api/persistence';

function RunDetail({ run }) {
  const formatNum = (n) => {
    if (n === null || n === undefined) return 'N/A';
    if (Math.abs(n) < 0.0001) return n.toExponential(4);
    return n.toFixed(6);
  };

  const objective = run.problem_definition?.objective || 'minimize';

  return (
    <div className="mt-3 pt-3 border-t border-slate-600 space-y-3 text-sm">
      {/* Best solution coordinates */}
      {run.best_solution && run.best_solution.length > 0 && (
        <div>
          <p className="text-gray-400 text-xs uppercase font-semibold mb-1">Solution Coordinates</p>
          <div className="flex flex-wrap gap-2">
            {run.best_solution.map((val, i) => (
              <span key={i} className="bg-slate-700 px-2 py-1 rounded text-xs font-mono text-gray-200">
                x[{i}] = {formatNum(val)}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Problem definition */}
      {run.problem_definition && (
        <div>
          <p className="text-gray-400 text-xs uppercase font-semibold mb-1">Problem</p>
          <div className="flex flex-wrap gap-3 text-xs text-gray-300">
            {run.problem_definition.dimensions && (
              <span>Dimensions: <span className="text-cyan-400">{run.problem_definition.dimensions}</span></span>
            )}
            <span>Objective: <span className={objective === 'maximize' ? 'text-green-400' : 'text-yellow-400'}>{objective}</span></span>
            {run.problem_definition.fitness_function_name && (
              <span>Function: <span className="text-cyan-400">{run.problem_definition.fitness_function_name}</span></span>
            )}
          </div>
        </div>
      )}

      {/* Algorithm parameters */}
      {run.algorithm_parameters && Object.keys(run.algorithm_parameters).length > 0 && (
        <div>
          <p className="text-gray-400 text-xs uppercase font-semibold mb-1">Parameters</p>
          <div className="flex flex-wrap gap-2">
            {Object.entries(run.algorithm_parameters).map(([k, v]) => (
              <span key={k} className="bg-slate-700 px-2 py-1 rounded text-xs text-gray-300">
                {k}: <span className="text-cyan-400">{String(v)}</span>
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Convergence summary */}
      {run.convergence_curve && run.convergence_curve.length > 0 && (
        <div>
          <p className="text-gray-400 text-xs uppercase font-semibold mb-1">Convergence</p>
          <div className="flex gap-4 text-xs text-gray-300">
            <span>Start: <span className="font-mono text-yellow-400">{formatNum(run.convergence_curve[0])}</span></span>
            <span>End: <span className="font-mono text-green-400">{formatNum(run.convergence_curve[run.convergence_curve.length - 1])}</span></span>
            <span>Points: <span className="text-gray-400">{run.convergence_curve.length}</span></span>
          </div>
        </div>
      )}
    </div>
  );
}

export default function ProblemHistory({ user }) {
  const [runs, setRuns] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [expandedId, setExpandedId] = useState(null);

  useEffect(() => {
    if (!user) return;
    fetchHistory();
  }, [user]);

  const fetchHistory = async () => {
    setLoading(true);
    setError('');
    try {
      const res = await persistenceAPI.getRunHistory(20);
      setRuns(res.data);
    } catch (e) {
      setError(e.response?.data?.detail || 'Failed to load history');
    } finally {
      setLoading(false);
    }
  };

  if (!user) return null;

  return (
    <div className="card p-6 rounded-lg shadow-md mt-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-bold text-primary">Problem History</h2>
        <button
          onClick={fetchHistory}
          className="text-sm text-cyan-400 hover:text-cyan-300 transition-colors"
        >
          Refresh
        </button>
      </div>

      {loading && (
        <p className="text-gray-400 text-sm">Loading history...</p>
      )}

      {error && (
        <div className="p-3 bg-red-500/20 border border-red-500/50 rounded-lg text-red-300 text-sm">
          {error}
        </div>
      )}

      {!loading && !error && runs.length === 0 && (
        <p className="text-gray-400 text-sm">
          No runs yet. Run an optimization to see your history here.
        </p>
      )}

      {!loading && runs.length > 0 && (
        <div className="space-y-3">
          {runs.map((run) => {
            const isExpanded = expandedId === run.id;
            return (
              <div
                key={run.id}
                className="bg-slate-800 border border-slate-700 rounded-lg p-4"
              >
                <button
                  onClick={() => setExpandedId(isExpanded ? null : run.id)}
                  className="w-full text-left flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2"
                >
                  <div>
                    <span className="font-semibold text-cyan-400">{run.algorithm}</span>
                    {run.problem_name && (
                      <span className="ml-2 text-gray-300 text-sm">— {run.problem_name}</span>
                    )}
                    <p className="text-gray-400 text-xs mt-1">
                      {new Date(run.created_at).toLocaleString()}
                    </p>
                  </div>
                  <div className="flex items-center gap-3">
                    <div className="text-right">
                      <p className="text-sm text-white">
                        Best fitness: <span className="font-mono text-green-400">{run.best_fitness?.toFixed(6)}</span>
                      </p>
                      <p className="text-xs text-gray-400">
                        {run.iterations_completed} iterations · {run.execution_time?.toFixed(2)}s
                      </p>
                    </div>
                    <span className="text-gray-400 text-lg">{isExpanded ? '▲' : '▼'}</span>
                  </div>
                </button>

                {isExpanded && <RunDetail run={run} />}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
