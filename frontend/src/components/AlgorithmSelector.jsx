import { useEffect, useState } from 'react';
import { fetchAlgorithms, executeAlgorithm } from '../api/index.js';
import ResultsDisplay from './ResultsDisplay';
import ProblemDefinitionForm from './forms/ProblemDefinitionForm';
import PSOParametersForm from './forms/PSOParametersForm';
import GAParametersForm from './forms/GAParametersForm';
import KnapsackInputForm from './forms/KnapsackInputForm';
import TSPInputForm from './forms/TSPInputForm';
import PresetSelector from './PresetSelector';
import PresetExplanation from './PresetExplanation';
import DEParametersForm from './forms/DEParametersForm';


export default function AlgorithmSelector() {
  const [algorithms, setAlgorithms] = useState([]);
  const [selectedAlgorithm, setSelectedAlgorithm] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);
  
  // Tab state: 'form' or 'yaml'
  const [inputMode, setInputMode] = useState('form');
  
  // Preset state
  const [selectedPreset, setSelectedPreset] = useState(null);
  
  // YAML upload state
  const [yamlFile, setYamlFile] = useState(null);
  const [yamlContent, setYamlContent] = useState('');

  // Shared problem definition state
  const [problemData, setProblemData] = useState({
    fitnessFunction: 'sphere',
    dimensions: 2,
    lowerBound: -5,
    upperBound: 5,
    objective: 'minimize'
  });

  // PSO-specific state
  const [psoParams, setPsoParams] = useState({
    swarmSize: 30,
    maxIterations: 50,
    w: 0.7,
    c1: 1.5,
    c2: 1.5
  });

  // GA-specific state
  const [gaParams, setGaParams] = useState({
    populationSize: 50,
    maxIterations: 50,
    crossoverRate: 0.8,
    mutationRate: 0.1,
    tournamentSize: 3
  });

  // DE-specific state
  const [deParams, setDeParams] = useState({
    population_size: 50,
    max_iterations: 50,
    F: 0.8,
    CR: 0.9
  });


  // Load available algorithms on mount
  useEffect(() => {
    fetchAlgorithms()
      .then(setAlgorithms)
      .catch(err => setError(`Failed to load algorithms: ${err.message}`));
  }, []);

  // Initialize real-world problem data when fitness function changes
  useEffect(() => {
    if (problemData.fitnessFunction === 'tsp' && !problemData.cities) {
      // Initialize with default cities
      setProblemData(prev => ({
        ...prev,
        cities: [
          { name: 'City A', x: 0, y: 0 },
          { name: 'City B', x: 3, y: 4 },
          { name: 'City C', x: 7, y: 1 },
          { name: 'City D', x: 5, y: 6 }
        ],
        dimensions: 4
      }));
    } else if (problemData.fitnessFunction === 'knapsack' && !problemData.items) {
      // Initialize with default items
      setProblemData(prev => ({
        ...prev,
        items: [
          { name: 'Laptop', weight: 3, value: 500 },
          { name: 'Camera', weight: 2, value: 300 },
          { name: 'Book', weight: 1, value: 50 },
          { name: 'Phone', weight: 1, value: 200 }
        ],
        capacity: 5,
        dimensions: 4
      }));
    }
  }, [problemData.fitnessFunction]);

  // Handle YAML file upload
  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setYamlFile(file);
    const reader = new FileReader();
    reader.onload = (event) => {
      setYamlContent(event.target.result);
    };
    reader.readAsText(file);
  };

  // Parse YAML content (simple parser - you can use js-yaml library for complex YAML)
  const parseYAML = (yamlText) => {
    try {
      // Simple YAML parser (for basic key-value pairs)
      // For production, install and use: npm install js-yaml
      const lines = yamlText.split('\n');
      const config = {};
      let currentSection = null;

      lines.forEach(line => {
        const trimmed = line.trim();
        if (!trimmed || trimmed.startsWith('#')) return;

        // Check if it's a section header (ends with : and has no spaces before :)
        const sectionMatch = trimmed.match(/^(\w+):$/);
        if (sectionMatch) {
          currentSection = sectionMatch[1];
          config[currentSection] = {};
          return;
        }

        // Key-value pair
        const kvMatch = trimmed.match(/^(\w+):\s*(.+)$/);
        if (kvMatch) {
          const [, key, value] = kvMatch;
          
          // Try to parse as number, boolean, or keep as string
          let parsedValue = value.trim();
          if (parsedValue === 'true') parsedValue = true;
          else if (parsedValue === 'false') parsedValue = false;
          else if (!isNaN(parsedValue) && parsedValue !== '') {
            parsedValue = Number(parsedValue);
          } else if (parsedValue.startsWith('[') && parsedValue.endsWith(']')) {
            // Parse array notation: [1, 2, 3]
            try {
              parsedValue = JSON.parse(parsedValue);
            } catch (e) {
              // Keep as string if JSON parse fails
            }
          }
          
          // If we're in a section, add to that section, otherwise add to root
          if (currentSection) {
            config[currentSection][key] = parsedValue;
          } else {
            config[key] = parsedValue;
          }
        }
      });

      return config;
    } catch (err) {
      throw new Error(`YAML parsing error: ${err.message}`);
    }
  };

  const handleRunFromYAML = async () => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const config = parseYAML(yamlContent);
      
      // Validate required sections
      if (!config.algorithm) {
        throw new Error('YAML must contain "algorithm" field');
      }
      if (!config.problem) {
        throw new Error('YAML must contain "problem" section');
      }
      if (!config.params) {
        throw new Error('YAML must contain "params" section');
      }

      // Build payload from YAML
      const payload = {
        algorithm: config.algorithm,
        problem: {
          dimensions: config.problem.dimensions,
          bounds: config.problem.bounds || Array(config.problem.dimensions).fill([
            config.problem.lower_bound || -5,
            config.problem.upper_bound || 5
          ]),
          objective: config.problem.objective || 'minimize'
        },
        params: config.params
      };

      // Handle real-world problems vs benchmark functions  
      if (config.problem.problem_type === 'tsp' && config.problem.cities) {
        payload.problem.problem_type = 'tsp';
        payload.problem.cities = config.problem.cities;
      } else if (config.problem.problem_type === 'knapsack' && config.problem.items) {
        payload.problem.problem_type = 'knapsack';
        payload.problem.items = config.problem.items;
        payload.problem.capacity = config.problem.capacity;
      } else {
        payload.problem.fitness_function_name = config.problem.fitness_function;
      }

      console.log('YAML payload:', payload);

      const res = await executeAlgorithm(payload);
      setResult(res);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleRun = async () => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      // Build the problem object
      const problem = {
        dimensions: parseInt(problemData.dimensions),
        bounds: Array(parseInt(problemData.dimensions)).fill([
          parseFloat(problemData.lowerBound),
          parseFloat(problemData.upperBound)
        ]),
        objective: problemData.objective
      };

      // Handle real-world problems vs benchmark functions
      if (problemData.fitnessFunction === 'tsp' && problemData.cities) {
        problem.problem_type = 'tsp';
        problem.cities = problemData.cities;
        // Don't set fitness_function_name for TSP
      } else if (problemData.fitnessFunction === 'knapsack' && problemData.items) {
        problem.problem_type = 'knapsack';
        problem.items = problemData.items;
        problem.capacity = parseFloat(problemData.capacity);
        // Don't set fitness_function_name for Knapsack
      } else {
        // Benchmark function
        problem.fitness_function_name = problemData.fitnessFunction;
      }

      // Build algorithm-specific params
      let params = {};
      
      if (selectedAlgorithm === 'particle_swarm') {
        params = {
          swarm_size: parseInt(psoParams.swarmSize),
          max_iterations: parseInt(psoParams.maxIterations),
          w: parseFloat(psoParams.w),
          c1: parseFloat(psoParams.c1),
          c2: parseFloat(psoParams.c2)
        };
      } else if (selectedAlgorithm === 'genetic_algorithm') {
        params = {
          population_size: parseInt(gaParams.populationSize),
          max_iterations: parseInt(gaParams.maxIterations),
          crossover_rate: parseFloat(gaParams.crossoverRate),
          mutation_rate: parseFloat(gaParams.mutationRate),
          tournament_size: parseInt(gaParams.tournamentSize)
        };
      } else if (selectedAlgorithm === 'differential_evolution') {
        params = {
          population_size: parseInt(deParams.population_size),
          max_iterations: parseInt(deParams.max_iterations),
          F: parseFloat(deParams.F),
          CR: parseFloat(deParams.CR)
        };
      }


      // Build the full payload
      const payload = {
        algorithm: selectedAlgorithm,
        problem: problem,
        params: params
      };

      const res = await executeAlgorithm(payload);
      setResult(res);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Handle preset selection
  const handlePresetSelect = (preset) => {
    // Save the preset for explanation display
    setSelectedPreset(preset);
    
    // Set algorithm
    setSelectedAlgorithm(preset.algorithm);
    
    // Set problem data
    setProblemData(preset.problemData);
    
    // Set algorithm-specific params
    if (preset.algorithm === 'particle_swarm' && preset.psoParams) {
      setPsoParams(preset.psoParams);
    } else if (preset.algorithm === 'genetic_algorithm' && preset.gaParams) {
      setGaParams(preset.gaParams);
    }
    
    // Switch to form mode to show the applied configuration
    setInputMode('form');
    
    // Clear any previous results
    setResult(null);
    setError(null);
  };

  // Algorithm name mapping for display
  const getAlgorithmDisplayName = (algoKey) => {
    const nameMap = {
      'particle_swarm': 'Particle Swarm Optimization (PSO)',
      'genetic_algorithm': 'Genetic Algorithm (GA)',
      'simulated_annealing': 'Simulated Annealing (SA)',
      'ant_colony': 'Ant Colony Optimization (ACO)',
      'differential_evolution': 'Differential Evolution (DE)'
    };
    return nameMap[algoKey] || algoKey;
  };

  return (
    <div className="max-w-4xl mx-auto">
      <h2 className="text-2xl font-semibold text-primary mb-4">
        Algorithm Dashboard
      </h2>
      
      {/* Error Display */}
      {error && (
        <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
          <strong>Error:</strong> {error}
        </div>
      )}

      {/* Input Mode Tabs */}
      <div className="mb-6 flex border-b border-gray-200">
        <button
          onClick={() => setInputMode('form')}
          className={`px-4 py-2 font-medium transition-colors ${
            inputMode === 'form'
              ? 'border-b-2 border-primary text-primary'
              : 'text-gray-500 hover:text-gray-700'
          }`}
        >
          Manual Input
        </button>
        <button
          onClick={() => setInputMode('yaml')}
          className={`px-4 py-2 font-medium transition-colors ${
            inputMode === 'yaml'
              ? 'border-b-2 border-primary text-primary'
              : 'text-gray-500 hover:text-gray-700'
          }`}
        >
          YAML Upload
        </button>
      </div>

      {/* Form Input Mode */}
      {inputMode === 'form' && (
        <>
          {/* Preset Selector Section */}
          <div className="mb-6">
            <PresetSelector onSelectPreset={handlePresetSelect} />
          </div>

          {/* Preset Explanation (shown when preset is selected) */}
          {selectedPreset && (
            <PresetExplanation preset={selectedPreset} />
          )}

          {/* Configuration Section Header */}
          {/* Configuration Section Header (only shown when preset is selected) */}
          {selectedPreset && (
            <div className="mb-4 p-4 bg-blue-50 border-l-4 border-blue-500 rounded">
              <div className="flex items-center gap-2">
                <span className="text-xl">✏️</span>
                <div>
                  <h4 className="font-semibold text-gray-800">Configuration (Pre-filled from Preset)</h4>
                  <p className="text-sm text-gray-600">
                    These values are already optimized for this scenario. You can run as-is or customize them below.
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* Algorithm Selection */}
          <div className="mb-4">
            <label className="block mb-2 font-medium text-gray-700">
              Select Algorithm:
            </label>
            <select
              value={selectedAlgorithm}
              onChange={e => {
                setSelectedAlgorithm(e.target.value);
                // Clear preset when manually changing algorithm
                if (selectedPreset && e.target.value !== selectedPreset.algorithm) {
                  setSelectedPreset(null);
                }
              }}
              className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[color:var(--color-primary)] focus:border-transparent bg-white"
            >
              <option value="">--Select an algorithm to configure parameters--</option>
              {algorithms.map(algo => (
                <option key={algo} value={algo}>
                  {getAlgorithmDisplayName(algo)}
                </option>
              ))}
            </select>
          </div>

          {/* Helpful message when no algorithm selected */}
          {!selectedAlgorithm && !selectedPreset && (
            <div className="mb-6 p-6 bg-gradient-to-r from-gray-50 to-gray-100 rounded-lg border-2 border-dashed border-gray-300 text-center">
              <div className="text-4xl mb-3">👆</div>
              <h4 className="font-semibold text-gray-700 mb-2">Ready to optimize?</h4>
              <p className="text-sm text-gray-600">
                Choose a <strong>preset</strong> above for a guided experience, or <strong>select an algorithm</strong> to configure manually.
              </p>
            </div>
          )}

          {/* Forms only appear when algorithm is selected */}
          {selectedAlgorithm && (
            <>
              {/* Shared Problem Definition Form (or Real-World Problem Forms) */}
              {problemData.fitnessFunction === 'knapsack' ? (
                <KnapsackInputForm 
                  formData={problemData}
                  onChange={(data) => {
                    setProblemData(data);
                    if (selectedPreset) setSelectedPreset(null);
                  }}
                />
              ) : problemData.fitnessFunction === 'tsp' ? (
                <TSPInputForm 
                  formData={problemData}
                  onChange={(data) => {
                    setProblemData(data);
                    if (selectedPreset) setSelectedPreset(null);
                  }}
                />
              ) : (
                <ProblemDefinitionForm 
                  formData={problemData}
                  onChange={(data) => {
                    setProblemData(data);
                    // Clear preset indicator when manually editing
                    if (selectedPreset) {
                      setSelectedPreset(null);
                    }
                  }}
                />
              )}


              {/* Algorithm-Specific Parameter Forms (Conditional Rendering) */}
              {selectedAlgorithm === 'particle_swarm' && (
                <PSOParametersForm 
                  formData={psoParams}
                  onChange={(params) => {
                    setPsoParams(params);
                    // Clear preset indicator when manually editing
                    if (selectedPreset) {
                      setSelectedPreset(null);
                    }
                  }}
                />
              )}

              {selectedAlgorithm === 'genetic_algorithm' && (
                <GAParametersForm 
                  formData={gaParams}
                  onChange={(params) => {
                    setGaParams(params);
                    // Clear preset indicator when manually editing
                    if (selectedPreset) {
                      setSelectedPreset(null);
                    }
                  }}
                />
              )}

              {/* Run Button - only shown when algorithm is selected */}
              <button
                onClick={handleRun}
                disabled={loading}
                className="w-full btn-primary hover:opacity-95 text-white font-semibold py-3 px-6 rounded-lg shadow-md transition duration-300 mb-6 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? 'Running...' : 'Run Optimization'}
              </button>
            </>
          )}

          {selectedAlgorithm === 'differential_evolution' && (
            <DEParametersForm 
              formData={deParams}
              onChange={setDeParams}
            />
          )}


          {/* Run Button */}
          <button
            onClick={handleRun}
            disabled={!selectedAlgorithm || loading}
            className="w-full btn-primary hover:opacity-95 text-white font-semibold py-3 px-6 rounded-lg shadow-md transition duration-300 mb-6 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? 'Running...' : 'Run Algorithm'}
          </button>

        </>
      )}

      {/* YAML Upload Mode */}
      {inputMode === 'yaml' && (
        <div className="mb-6">
          <div className="mb-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <h3 className="font-semibold text-gray-700 mb-2">YAML Configuration Format</h3>
            <pre className="text-xs bg-white p-3 rounded border border-gray-200 overflow-x-auto">
{`algorithm: particle_swarm
problem:
  dimensions: 2
  fitness_function: sphere
  lower_bound: -5
  upper_bound: 5
  objective: minimize
params:
  swarm_size: 30
  max_iterations: 50
  w: 0.7
  c1: 1.5
  c2: 1.5`}
            </pre>
          </div>

          {/* File Upload */}
          <div className="mb-4">
            <label className="block mb-2 font-medium text-gray-700">
              Upload YAML Configuration:
            </label>
            <input
              type="file"
              accept=".yaml,.yml"
              onChange={handleFileUpload}
              className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[color:var(--color-primary)] bg-white"
            />
            {yamlFile && (
              <p className="mt-2 text-sm text-gray-600">
                Loaded: <span className="font-medium">{yamlFile.name}</span>
              </p>
            )}
          </div>

          {/* YAML Content Preview */}
          {yamlContent && (
            <div className="mb-4">
              <label className="block mb-2 font-medium text-gray-700">
                File Content:
              </label>
              <textarea
                value={yamlContent}
                onChange={e => setYamlContent(e.target.value)}
                rows={12}
                className="w-full p-3 border border-gray-300 rounded-lg font-mono text-sm focus:ring-2 focus:ring-[color:var(--color-primary)] bg-white"
                placeholder="Paste YAML configuration here or upload a file..."
              />
            </div>
          )}

          {/* Run from YAML Button */}
          <button
            onClick={handleRunFromYAML}
            disabled={!yamlContent || loading}
            className="w-full btn-primary hover:opacity-95 text-white font-semibold py-3 px-6 rounded-lg shadow-md transition duration-300 mb-6 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? 'Running...' : 'Run from YAML'}
          </button>
        </div>
      )}

      {/* Results Display */}
      {result && <ResultsDisplay result={result} />}
    </div>
  );
}