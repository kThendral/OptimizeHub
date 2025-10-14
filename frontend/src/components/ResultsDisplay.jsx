export default function ResultsDisplay({ result }) {
  return (
    <div>
      <h3 className="text-2xl font-semibold text-gray-800 mb-4">Results</h3>
      <div className="bg-gray-100 p-4 rounded-lg border border-gray-300">
        <pre className="text-sm text-gray-800 font-mono whitespace-pre-wrap">{JSON.stringify(result, null, 2)}</pre>
      </div>
    </div>
  );
}
