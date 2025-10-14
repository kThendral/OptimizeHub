import { useState } from "react";

export default function UploadForm({ onRun, onBack }) {
  const [file, setFile] = useState(null);
  const [algorithm, setAlgorithm] = useState("");
  const [params, setParams] = useState({});

  const algorithms = ["GA", "PSO", "DE"];

  const handleFileChange = e => setFile(e.target.files[0]);

  const handleRun = () => {
    if (!file || !algorithm) {
      alert("Please select a file and an algorithm!");
      return;
    }
    const payload = { fileName: file.name, algorithm, params };
    onRun(payload);
  };

  return (
    <div>
      <h2 className="text-2xl font-semibold text-gray-800 mb-4">Upload Problem</h2>
      <div className="mb-4">
        <label className="block mb-2 font-medium text-gray-700">Select a problem file:</label>
        <input
          type="file"
          onChange={handleFileChange}
          className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white"
        />
      </div>

      <div className="mb-4">
        <label className="block mb-2 font-medium text-gray-700">Select Algorithm:</label>
        <select
          value={algorithm}
          onChange={e => setAlgorithm(e.target.value)}
          className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white"
        >
          <option value="">--Choose Algorithm--</option>
          {algorithms.map(a => (
            <option key={a} value={a}>{a}</option>
          ))}
        </select>
      </div>

      <div className="mb-6">
        <label className="block mb-2 font-medium text-gray-700">Parameters:</label>
        <input
          type="number"
          placeholder="Population Size"
          onChange={e => setParams({ ...params, population: e.target.value })}
          className="w-full p-3 border border-gray-300 rounded-lg mb-3 focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white"
        />
        <input
          type="number"
          placeholder="Iterations"
          onChange={e => setParams({ ...params, iterations: e.target.value })}
          className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white"
        />
      </div>

      <div className="flex gap-3">
        <button
          onClick={handleRun}
          className="flex-1 btn-primary hover:opacity-95 text-white font-semibold py-3 px-6 rounded-lg shadow-md transition duration-300"
          style={{ borderRadius: '0.5rem' }}
        >
          Run Algorithm
        </button>

      </div>
    </div>
  );
}
