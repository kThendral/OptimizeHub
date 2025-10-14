import React, { useState } from "react";
import LandingPage from "./components/LandingPage";
import Dashboard from "./components/AlgorithmSelector";
import ProblemSelector from "./components/ProblemSelector";
import ParameterForm from "./components/ParameterForm";
import UploadForm from "./components/UploadForm";
import ResultsDisplay from "./components/ResultsDisplay";

function App() {
  const [showLanding, setShowLanding] = useState(true);
  const [results, setResults] = useState(null);

  const handleRun = (payload) => {
    // Simulate API call or handle payload
    setResults(payload);
  };

  if (showLanding) {
    return <LandingPage onStart={() => setShowLanding(false)} />;
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold text-blue-600 mb-8 text-center">OptimizeHub</h1>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <div className="bg-white p-6 rounded-lg shadow-md">
            <ProblemSelector />
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <ParameterForm />
          </div>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-md mb-8">
          <UploadForm onRun={handleRun} />
        </div>
        <div className="bg-white p-6 rounded-lg shadow-md mb-8">
          <Dashboard />
        </div>
        {results && (
          <div className="bg-white p-6 rounded-lg shadow-md">
            <ResultsDisplay result={results} />
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
