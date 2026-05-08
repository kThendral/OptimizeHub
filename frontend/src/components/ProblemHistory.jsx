import { useState, useEffect } from 'react';
import { persistenceAPI } from '../api/persistence';

export default function ProblemHistory({ user }) {
  const [runs, setRuns] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

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
          {runs.map((run) => (
            <div
              key={run.id}
              className="bg-slate-800 border border-slate-700 rounded-lg p-4 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2"
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
              <div className="text-right">
                <p className="text-sm text-white">
                  Best fitness: <span className="font-mono text-green-400">{run.best_fitness?.toFixed(6)}</span>
                </p>
                <p className="text-xs text-gray-400">
                  {run.iterations_completed} iterations · {run.execution_time?.toFixed(2)}s
                </p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
