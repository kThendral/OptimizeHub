import React from 'react';
import {
  Chart as ChartJS,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend,
} from 'chart.js';
import { Radar } from 'react-chartjs-2';

ChartJS.register(
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend
);

const SolutionRadarChart = ({ bestSolution, bounds }) => {
  if (!bestSolution || bestSolution.length === 0) {
    return (
      <div className="bg-white p-6 rounded-lg shadow-lg border border-gray-200">
        <div className="text-gray-500 text-center py-8">No solution data available</div>
      </div>
    );
  }

  // Normalize solution values to 0-100 scale for radar chart
  const normalizedSolution = bestSolution.map((value, index) => {
    const [min, max] = bounds[index] || [-5, 5];
    const range = max - min || 1;
    return ((value - min) / range) * 100;
  });

  const options = {
    responsive: true,
    maintainAspectRatio: false,
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
        text: 'Solution Components Analysis',
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
            const actualValue = bestSolution[context.dataIndex];
            return `Dimension ${context.dataIndex + 1}: ${actualValue?.toFixed(4) || 'N/A'}`;
          }
        }
      }
    },
    scales: {
      r: {
        beginAtZero: true,
        max: 100,
        ticks: {
          color: '#6B7280',
          backdropColor: 'transparent'
        },
        grid: {
          color: 'rgba(107, 114, 128, 0.3)'
        },
        angleLines: {
          color: 'rgba(107, 114, 128, 0.3)'
        },
        pointLabels: {
          color: '#5B21B6',
          font: {
            size: 12,
            weight: 'bold'
          }
        }
      }
    },
    elements: {
      point: {
        radius: 4,
        hoverRadius: 8
      },
      line: {
        borderWidth: 2
      }
    }
  };

  const data = {
    labels: bestSolution.map((_, index) => `Dim ${index + 1}`),
    datasets: [
      {
        label: 'Solution Values (Normalized)',
        data: normalizedSolution,
        backgroundColor: 'rgba(91, 33, 182, 0.2)',
        borderColor: '#5B21B6',
        borderWidth: 2,
        pointBackgroundColor: '#5B21B6',
        pointBorderColor: '#ffffff',
        pointBorderWidth: 2
      }
    ]
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-lg border border-gray-200">
      <div style={{ height: '400px' }}>
        <Radar options={options} data={data} />
      </div>
    </div>
  );
};

export default SolutionRadarChart;