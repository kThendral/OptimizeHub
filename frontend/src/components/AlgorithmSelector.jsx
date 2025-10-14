import { useEffect, useState } from 'react';
import { fetchAlgorithms, executeAlgorithm } from '../api';
import ResultsDisplay from './ResultsDisplay';

export default function Dashboard() {
  const [algorithms, setAlgorithms] = useState([]);
  const [selectedAlgorithm, setSelectedAlgorithm] = useState('');
  const [problem, setProblem] = useState('');
  const [result, setResult] = useState(null);

  useEffect(() => {
    fetchAlgorithms().then(setAlgorithms);
  }, []);

  const handleRun = async () => {
    const payload = { algorithm: selectedAlgorithm, problem };
    const res = await executeAlgorithm(payload);
    setResult(res);
  };

  return (
    <div>
      <h2 className="text-2xl font-semibold text-gray-800 mb-4">Algorithm Dashboard</h2>
      <div className="mb-4">
        <label className="block mb-2 font-medium text-gray-700">Select Algorithm:</label>
        <select
          value={selectedAlgorithm}
          onChange={e => setSelectedAlgorithm(e.target.value)}
          className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white"
        >
          <option value="">Select Algorithm</option>
          {algorithms.map(a => <option key={a} value={a}>{a}</option>)}
        </select>
      </div>

      <div className="mb-4">
        <label className="block mb-2 font-medium text-gray-700">Enter Problem:</label>
        <input
          type="text"
          placeholder="Enter problem"
          value={problem}
          onChange={e => setProblem(e.target.value)}
          className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white"
        />
      </div>

      <button
        onClick={handleRun}
        className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg shadow-md transition duration-300 mb-6"
      >
        Run
      </button>

      {result && <ResultsDisplay result={result} />}
    </div>
  );
}
