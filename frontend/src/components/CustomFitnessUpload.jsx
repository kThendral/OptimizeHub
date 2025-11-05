import React, { useState } from 'react';
import axios from 'axios';
import Chart from 'chart.js/auto';
import './CustomFitnessUpload.css';

const CustomFitnessUpload = () => {
  const [fitnessFile, setFitnessFile] = useState(null);
  const [configFile, setConfigFile] = useState(null);
  const [fitnessCode, setFitnessCode] = useState('');
  const [configContent, setConfigContent] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [chartInstance, setChartInstance] = useState(null);

  // Handle fitness file selection
  const handleFitnessFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setFitnessFile(file);
      setError(null);

      // Read file content for preview
      const reader = new FileReader();
      reader.onload = (e) => {
        setFitnessCode(e.target.result);
      };
      reader.readAsText(file);
    }
  };

  // Handle config file selection
  const handleConfigFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setConfigFile(file);
      setError(null);

      // Read file content for preview
      const reader = new FileReader();
      reader.onload = (e) => {
        setConfigContent(e.target.result);
      };
      reader.readAsText(file);
    }
  };

  // Handle form submission
  const handleSubmit = async (event) => {
    event.preventDefault();

    // Validation
    if (!fitnessFile) {
      setError('Please select a fitness function file (.py)');
      return;
    }

    if (!configFile) {
      setError('Please select a configuration file (.yaml)');
      return;
    }

    setIsLoading(true);
    setError(null);
    setResult(null);

    // Destroy previous chart if exists
    if (chartInstance) {
      chartInstance.destroy();
      setChartInstance(null);
    }

    try {
      // Create form data
      const formData = new FormData();
      formData.append('fitness_file', fitnessFile);
      formData.append('config_file', configFile);

      // Send request to backend
      const response = await axios.post(
        'http://localhost:8000/api/optimize/custom',
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
          timeout: 35000, // 35 seconds (slightly more than backend timeout)
        }
      );

      console.log('Received response data:', response.data);
      setResult(response.data);

      // Draw convergence chart
      setTimeout(() => drawConvergenceChart(response.data), 100);
    } catch (err) {
      console.error('Optimization error:', err);

      if (err.response) {
        // Server responded with error
        const detail = err.response.data.detail;
        if (typeof detail === 'object') {
          setError(detail.message || detail.error || 'Optimization failed');
        } else {
          setError(detail || 'Optimization failed');
        }
      } else if (err.code === 'ECONNABORTED') {
        setError('Request timeout. The optimization is taking too long.');
      } else if (err.request) {
        setError('No response from server. Please check if the backend is running.');
      } else {
        setError(err.message || 'An unexpected error occurred');
      }
    } finally {
      setIsLoading(false);
    }
  };

  // Draw convergence chart
  const drawConvergenceChart = (data) => {
    const canvas = document.getElementById('convergenceChart');
    if (!canvas) return;

    // Check if convergence_curve exists
    if (!data.convergence_curve || !Array.isArray(data.convergence_curve)) {
      console.error('Convergence curve not available:', data);
      return;
    }

    const ctx = canvas.getContext('2d');

    // Destroy previous chart
    if (chartInstance) {
      chartInstance.destroy();
    }

    // Create new chart
    const newChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: data.convergence_curve.map((_, i) => i),
        datasets: [
          {
            label: 'Best Fitness',
            data: data.convergence_curve,
            borderColor: 'rgb(75, 192, 192)',
            backgroundColor: 'rgba(75, 192, 192, 0.1)',
            tension: 0.1,
            fill: true,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          title: {
            display: true,
            text: `Convergence History - ${data.algorithm}`,
            font: {
              size: 16,
            },
          },
          legend: {
            display: true,
            position: 'top',
          },
        },
        scales: {
          x: {
            title: {
              display: true,
              text: 'Iteration',
            },
          },
          y: {
            title: {
              display: true,
              text: 'Fitness Value',
            },
            beginAtZero: false,
          },
        },
      },
    });

    setChartInstance(newChart);
  };

  // Reset form
  const handleReset = () => {
    setFitnessFile(null);
    setConfigFile(null);
    setFitnessCode('');
    setConfigContent('');
    setResult(null);
    setError(null);

    if (chartInstance) {
      chartInstance.destroy();
      setChartInstance(null);
    }

    // Reset file inputs
    document.getElementById('fitnessFileInput').value = '';
    document.getElementById('configFileInput').value = '';
  };

  return (
    <div className="custom-fitness-upload">
      <div className="upload-header">
        <h2>Custom Fitness Function Optimization</h2>
        <p>Upload your own fitness function and run it in a secure Docker sandbox</p>
      </div>

      <form onSubmit={handleSubmit} className="upload-form">
        <div className="form-section">
          <div className="file-upload-group">
            <label htmlFor="fitnessFileInput">
              <strong>1. Fitness Function (.py)</strong>
            </label>
            <p className="file-description">
              Python file containing a function named <code>fitness(x)</code> that returns a numeric value.
              Only <code>math</code> and <code>numpy</code> imports are allowed.
            </p>
            <input
              id="fitnessFileInput"
              type="file"
              accept=".py"
              onChange={handleFitnessFileChange}
              disabled={isLoading}
              className="file-input"
            />
            {fitnessFile && (
              <div className="file-selected">
                Selected: {fitnessFile.name} ({(fitnessFile.size / 1024).toFixed(2)} KB)
              </div>
            )}
          </div>

          {fitnessCode && (
            <div className="code-preview">
              <strong>Fitness Function Preview:</strong>
              <pre>{fitnessCode}</pre>
            </div>
          )}
        </div>

        <div className="form-section">
          <div className="file-upload-group">
            <label htmlFor="configFileInput">
              <strong>2. Configuration (.yaml)</strong>
            </label>
            <p className="file-description">
              YAML file with algorithm, parameters, and problem configuration.
              Supported algorithms: PSO, GA, DE, SA, ACOR
            </p>
            <input
              id="configFileInput"
              type="file"
              accept=".yaml,.yml"
              onChange={handleConfigFileChange}
              disabled={isLoading}
              className="file-input"
            />
            {configFile && (
              <div className="file-selected">
                Selected: {configFile.name} ({(configFile.size / 1024).toFixed(2)} KB)
              </div>
            )}
          </div>

          {configContent && (
            <div className="code-preview">
              <strong>Configuration Preview:</strong>
              <pre>{configContent}</pre>
            </div>
          )}
        </div>

        <div className="form-actions">
          <button
            type="submit"
            disabled={isLoading || !fitnessFile || !configFile}
            className="btn-primary"
          >
            {isLoading ? 'Optimizing...' : 'Run Optimization'}
          </button>
          <button
            type="button"
            onClick={handleReset}
            disabled={isLoading}
            className="btn-secondary"
          >
            Reset
          </button>
        </div>
      </form>

      {error && (
        <div className="error-message">
          <strong>Error:</strong> {error}
        </div>
      )}

      {isLoading && (
        <div className="loading-indicator">
          <div className="spinner"></div>
          <p>Running optimization in secure Docker container...</p>
          <p className="loading-subtext">This may take up to 30 seconds</p>
        </div>
      )}

      {result && (
        <div className="results-section">
          <h3>Optimization Results</h3>

          <div className="results-grid">
            <div className="result-card">
              <div className="result-label">Algorithm</div>
              <div className="result-value">{result.algorithm}</div>
            </div>

            <div className="result-card">
              <div className="result-label">Best Fitness</div>
              <div className="result-value">{result.best_fitness.toExponential(6)}</div>
            </div>

            <div className="result-card">
              <div className="result-label">Iterations</div>
              <div className="result-value">{result.iterations_completed}</div>
            </div>

            <div className="result-card">
              <div className="result-label">Execution Time</div>
              <div className="result-value">{result.execution_time.toFixed(2)}s</div>
            </div>
          </div>

          <div className="result-card full-width">
            <div className="result-label">Best Solution</div>
            <div className="result-value solution-array">
              [{result.best_solution.map(v => v.toFixed(6)).join(', ')}]
            </div>
          </div>

          <div className="chart-container">
            <canvas id="convergenceChart"></canvas>
          </div>

          <div className="success-message">
            Optimization completed successfully using custom fitness function!
          </div>
        </div>
      )}

      <div className="help-section">
        <h4>Example Fitness Function</h4>
        <pre className="example-code">{`import numpy as np

def fitness(x):
    """Sphere function"""
    return np.sum(x**2)`}</pre>

        <h4>Example Configuration</h4>
        <pre className="example-code">{`algorithm: PSO
parameters:
  num_particles: 30
  max_iterations: 100
  w: 0.7
  c1: 1.5
  c2: 1.5
problem:
  dimensions: 10
  lower_bound: -5.0
  upper_bound: 5.0`}</pre>
      </div>
    </div>
  );
};

export default CustomFitnessUpload;
