import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  LogarithmicScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from 'chart.js';
import { Line } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  LogarithmicScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

const ConvergenceChart = ({ convergenceData, algorithmName }) => {
  if (!convergenceData || convergenceData.length === 0) {
    return (
      <div className="bg-white p-6 rounded-lg shadow-lg border border-gray-200">
        <div className="text-gray-500 text-center py-8">No convergence data available</div>
      </div>
    );
  }

  // Determine if we should use log scale
  const maxValue = Math.max(...convergenceData);
  const minValue = Math.min(...convergenceData);
  const useLogScale = maxValue > 0 && minValue > 0 && (maxValue / minValue) > 100;

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    interaction: {
      intersect: false,
      mode: 'index',
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
        text: `${algorithmName} Convergence Curve`,
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
        borderColor: '#5B21B6',
        borderWidth: 1,
        callbacks: {
          label: function(context) {
            const value = context.parsed.y;
            return `Fitness: ${Math.abs(value) < 0.0001 ? value.toExponential(4) : value.toFixed(6)}`;
          }
        }
      }
    },
    scales: {
      x: {
        display: true,
        title: {
          display: true,
          text: 'Iteration',
          color: '#5B21B6',
          font: {
            size: 14,
            weight: 'bold'
          }
        },
        ticks: {
          color: '#6B7280'
        },
        grid: {
          color: 'rgba(107, 114, 128, 0.2)'
        }
      },
      y: {
        display: true,
        type: useLogScale ? 'logarithmic' : 'linear',
        title: {
          display: true,
          text: useLogScale ? 'Best Fitness Value (log scale)' : 'Best Fitness Value',
          color: '#5B21B6',
          font: {
            size: 14,
            weight: 'bold'
          }
        },
        ticks: {
          color: '#6B7280',
          callback: function(value) {
            if (useLogScale) {
              return value.toExponential(2);
            } else {
              return Math.abs(value) < 0.0001 ? value.toExponential(2) : value.toFixed(4);
            }
          }
        },
        grid: {
          color: 'rgba(107, 114, 128, 0.2)'
        }
      }
    },
    elements: {
      point: {
        radius: 2,
        hoverRadius: 6
      },
      line: {
        tension: 0.1
      }
    }
  };

  const data = {
    labels: convergenceData.map((_, index) => index + 1),
    datasets: [
      {
        label: 'Best Fitness',
        data: convergenceData,
        borderColor: '#5B21B6',
        backgroundColor: 'rgba(91, 33, 182, 0.1)',
        borderWidth: 2,
        fill: true,
        pointBackgroundColor: '#5B21B6',
        pointBorderColor: '#ffffff',
        pointBorderWidth: 2
      }
    ]
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-lg border border-gray-200">
      <div style={{ height: '400px' }}>
        <Line options={options} data={data} />
      </div>
    </div>
  );
};

export default ConvergenceChart;