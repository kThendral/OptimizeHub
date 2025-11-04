import React from 'react';
import {
  Chart as ChartJS,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
} from 'chart.js';
import { Scatter } from 'react-chartjs-2';

ChartJS.register(LinearScale, PointElement, LineElement, Tooltip, Legend);

const SolutionSpaceChart = ({ bestSolution, bounds, fitnessFunction }) => {
  if (!bestSolution || bestSolution.length < 2) {
    return (
      <div className="bg-white p-6 rounded-lg shadow-lg border border-gray-200">
        <div className="text-gray-500 text-center py-8">
          Solution space visualization requires 2+ dimensions
        </div>
      </div>
    );
  }

  // Generate contour data for 2D visualization
  const generateContourData = () => {
    const points = [];
    const resolution = 15; // Reduced for performance
    const [xMin, xMax] = bounds[0] || [-5, 5];
    const [yMin, yMax] = bounds[1] || [-5, 5];
    
    for (let i = 0; i <= resolution; i++) {
      for (let j = 0; j <= resolution; j++) {
        const x = xMin + (xMax - xMin) * (i / resolution);
        const y = yMin + (yMax - yMin) * (j / resolution);
        
        // Simple fitness calculation for visualization
        let fitness;
        const funcName = fitnessFunction?.toLowerCase() || 'sphere';
        
        switch (funcName) {
          case 'sphere':
            fitness = x*x + y*y;
            break;
          case 'rastrigin':
            fitness = 20 + x*x - 10*Math.cos(2*Math.PI*x) + y*y - 10*Math.cos(2*Math.PI*y);
            break;
          case 'rosenbrock':
            fitness = (1 - x)**2 + 100*(y - x**2)**2;
            break;
          case 'ackley':
            fitness = -20*Math.exp(-0.2*Math.sqrt(0.5*(x*x + y*y))) - Math.exp(0.5*(Math.cos(2*Math.PI*x) + Math.cos(2*Math.PI*y))) + 20 + Math.E;
            break;
          case 'griewank':
            fitness = 1 + (x*x + y*y)/4000 - Math.cos(x)*Math.cos(y/Math.sqrt(2));
            break;
          default:
            fitness = x*x + y*y;
        }
        
        points.push({ x, y, fitness });
      }
    }
    return points;
  };

  const contourData = generateContourData();
  const maxFitness = Math.max(...contourData.map(p => p.fitness));
  const minFitness = Math.min(...contourData.map(p => p.fitness));

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    interaction: {
      intersect: false,
    },
    plugins: {
      legend: {
        position: 'top',
        labels: {
          color: '#5B21B6',
          font: {
            size: 12,
            weight: 'bold'
          }
        }
      },
      title: {
        display: true,
        text: `Solution Space - ${fitnessFunction || 'Unknown'} Function`,
        color: '#5B21B6',
        font: {
          size: 16,
          weight: 'bold'
        }
      },
      tooltip: {
        backgroundColor: 'rgba(91, 33, 182, 0.9)',
        titleColor: '#ffffff',
        bodyColor: '#ffffff',
        callbacks: {
          label: function(context) {
            if (context.datasetIndex === 0) {
              return `Best Solution: (${context.parsed.x.toFixed(4)}, ${context.parsed.y.toFixed(4)})`;
            }
            return `Coordinates: (${context.parsed.x.toFixed(2)}, ${context.parsed.y.toFixed(2)})`;
          }
        }
      }
    },
    scales: {
      x: {
        display: true,
        title: {
          display: true,
          text: 'Dimension 1',
          color: '#5B21B6',
          font: { size: 14, weight: 'bold' }
        },
        ticks: { color: '#6B7280' },
        grid: { color: 'rgba(107, 114, 128, 0.2)' }
      },
      y: {
        display: true,
        title: {
          display: true,
          text: 'Dimension 2',
          color: '#5B21B6',
          font: { size: 14, weight: 'bold' }
        },
        ticks: { color: '#6B7280' },
        grid: { color: 'rgba(107, 114, 128, 0.2)' }
      }
    }
  };

  const data = {
    datasets: [
      {
        label: 'Best Solution',
        data: [{ x: bestSolution[0], y: bestSolution[1] }],
        backgroundColor: '#EF4444',
        borderColor: '#DC2626',
        pointRadius: 8,
        pointHoverRadius: 12,
        borderWidth: 3
      },
      {
        label: 'Fitness Landscape',
        data: contourData.map(p => ({
          x: p.x,
          y: p.y
        })),
        backgroundColor: contourData.map(p => {
          const intensity = (p.fitness - minFitness) / (maxFitness - minFitness || 1);
          return `rgba(91, 33, 182, ${0.1 + intensity * 0.3})`;
        }),
        borderColor: 'rgba(91, 33, 182, 0.6)',
        pointRadius: 3,
        pointHoverRadius: 5
      }
    ]
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-lg border border-gray-200">
      <div style={{ height: '400px' }}>
        <Scatter options={options} data={data} />
      </div>
    </div>
  );
};

export default SolutionSpaceChart;