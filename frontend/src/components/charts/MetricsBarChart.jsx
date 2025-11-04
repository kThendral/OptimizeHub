import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const MetricsBarChart = ({ results, algorithmName }) => {
  if (!results) {
    return (
      <div className="bg-white p-6 rounded-lg shadow-lg border border-gray-200">
        <div className="text-gray-500 text-center py-8">No metrics data available</div>
      </div>
    );
  }

  const { best_fitness, iterations_completed, convergence_curve } = results;
  
  // Calculate additional metrics
  const improvementRate = convergence_curve?.length > 1 
    ? ((convergence_curve[0] - best_fitness) / (convergence_curve[0] || 1) * 100)
    : 0;
  
  const convergenceSpeed = convergence_curve?.findIndex(
    (fitness, index) => index > 0 && Math.abs(fitness - best_fitness) < 0.01 * Math.abs(best_fitness || 1)
  ) || (iterations_completed || 0);

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false
      },
      title: {
        display: true,
        text: `${algorithmName} Performance Metrics`,
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
            const value = context.parsed.y;
            switch(context.label) {
              case 'Best Fitness':
                return `${Math.abs(value) < 0.0001 ? value.toExponential(4) : value.toFixed(6)}`;
              case 'Iterations':
                return `${value} iterations`;
              case 'Improvement':
                return `${value.toFixed(2)}%`;
              case 'Convergence Speed':
                return `${value} iterations to converge`;
              default:
                return value.toString();
            }
          }
        }
      }
    },
    scales: {
      x: {
        ticks: {
          color: '#6B7280',
          font: { weight: 'bold' }
        },
        grid: {
          display: false
        }
      },
      y: {
        beginAtZero: true,
        ticks: {
          color: '#6B7280'
        },
        grid: {
          color: 'rgba(107, 114, 128, 0.2)'
        }
      }
    }
  };

  const data = {
    labels: ['Best Fitness', 'Iterations', 'Improvement %', 'Convergence Speed'],
    datasets: [
      {
        data: [
          Math.abs(best_fitness || 0),
          iterations_completed || 0,
          Math.abs(improvementRate || 0),
          convergenceSpeed || 0
        ],
        backgroundColor: [
          'rgba(91, 33, 182, 0.8)',
          'rgba(0, 212, 255, 0.8)',
          'rgba(34, 197, 94, 0.8)',
          'rgba(251, 146, 60, 0.8)'
        ],
        borderColor: [
          '#5B21B6',
          '#00D4FF',
          '#22C55E',
          '#FB923C'
        ],
        borderWidth: 2,
        borderRadius: 8,
        borderSkipped: false
      }
    ]
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-lg border border-gray-200">
      <div style={{ height: '300px' }}>
        <Bar options={options} data={data} />
      </div>
    </div>
  );
};

export default MetricsBarChart;