import { useState } from 'react';

/**
 * Custom input form for Traveling Salesman Problem (TSP).
 * Allows users to define city coordinates.
 */
export default function TSPInputForm({ formData, onChange }) {
  const [cities, setCities] = useState(formData.cities || [
    { name: 'City A', x: 0, y: 0 },
    { name: 'City B', x: 3, y: 4 },
    { name: 'City C', x: 7, y: 1 },
    { name: 'City D', x: 5, y: 6 }
  ]);

  const handleCityChange = (index, field, value) => {
    const newCities = [...cities];
    newCities[index][field] = field === 'name' ? value : parseFloat(value) || 0;
    setCities(newCities);
    updateFormData(newCities);
  };

  const addCity = () => {
    const newCities = [...cities, { 
      name: `City ${String.fromCharCode(65 + cities.length)}`, 
      x: Math.random() * 10, 
      y: Math.random() * 10 
    }];
    setCities(newCities);
    updateFormData(newCities);
  };

  const removeCity = (index) => {
    const newCities = cities.filter((_, i) => i !== index);
    setCities(newCities);
    updateFormData(newCities);
  };

  const updateFormData = (citiesList) => {
    onChange({
      ...formData,
      cities: citiesList,
      dimensions: citiesList.length,
      problemType: 'tsp'
    });
  };

  // Calculate distance between two cities
  const distance = (city1, city2) => {
    const dx = city1.x - city2.x;
    const dy = city1.y - city2.y;
    return Math.sqrt(dx * dx + dy * dy);
  };

  // Calculate bounds for visualization
  const getMapBounds = () => {
    if (cities.length === 0) return { minX: 0, maxX: 10, minY: 0, maxY: 10 };
    const xs = cities.map(c => c.x);
    const ys = cities.map(c => c.y);
    return {
      minX: Math.min(...xs) - 1,
      maxX: Math.max(...xs) + 1,
      minY: Math.min(...ys) - 1,
      maxY: Math.max(...ys) + 1
    };
  };

  const bounds = getMapBounds();
  const mapWidth = bounds.maxX - bounds.minX;
  const mapHeight = bounds.maxY - bounds.minY;

  return (
    <div className="mb-4 p-5 bg-gradient-to-br from-blue-50 to-cyan-50 rounded-xl border-2 border-blue-300 shadow-sm">
      <div className="flex items-center gap-2 mb-4">
        <span className="text-2xl">🗺️</span>
        <h3 className="font-bold text-gray-800 text-lg">Traveling Salesman Problem Configuration</h3>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {/* Cities Table */}
        <div className="bg-white rounded-lg border-2 border-blue-200 overflow-hidden">
          <div className="bg-gradient-to-r from-blue-500 to-cyan-500 px-4 py-2">
            <h4 className="font-bold text-white text-sm">Cities to Visit</h4>
          </div>
          
          <div className="overflow-x-auto max-h-96">
            <table className="w-full text-sm">
              <thead className="bg-gray-100 border-b-2 border-blue-200 sticky top-0">
                <tr>
                  <th className="px-4 py-2 text-left font-semibold text-gray-700">City</th>
                  <th className="px-4 py-2 text-left font-semibold text-gray-700">X</th>
                  <th className="px-4 py-2 text-left font-semibold text-gray-700">Y</th>
                  <th className="px-4 py-2 text-center font-semibold text-gray-700">Action</th>
                </tr>
              </thead>
              <tbody>
                {cities.map((city, index) => (
                  <tr key={index} className="border-b border-gray-200 hover:bg-blue-50">
                    <td className="px-4 py-2">
                      <input
                        type="text"
                        value={city.name}
                        onChange={e => handleCityChange(index, 'name', e.target.value)}
                        className="w-full p-2 border border-gray-300 rounded focus:ring-1 focus:ring-blue-500"
                      />
                    </td>
                    <td className="px-4 py-2">
                      <input
                        type="number"
                        step="0.1"
                        value={city.x}
                        onChange={e => handleCityChange(index, 'x', e.target.value)}
                        className="w-20 p-2 border border-gray-300 rounded focus:ring-1 focus:ring-blue-500"
                      />
                    </td>
                    <td className="px-4 py-2">
                      <input
                        type="number"
                        step="0.1"
                        value={city.y}
                        onChange={e => handleCityChange(index, 'y', e.target.value)}
                        className="w-20 p-2 border border-gray-300 rounded focus:ring-1 focus:ring-blue-500"
                      />
                    </td>
                    <td className="px-4 py-2 text-center">
                      <button
                        onClick={() => removeCity(index)}
                        disabled={cities.length <= 3}
                        className="text-red-600 hover:text-red-800 disabled:text-gray-300 disabled:cursor-not-allowed font-bold"
                        title="Remove city"
                      >
                        ✕
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="p-3 bg-gray-50 border-t border-gray-200">
            <button
              onClick={addCity}
              className="w-full bg-gradient-to-r from-blue-500 to-cyan-500 hover:from-blue-600 hover:to-cyan-600 text-white font-semibold py-2 px-4 rounded-lg transition-all duration-200 shadow-md"
            >
              + Add City
            </button>
          </div>
        </div>

        {/* City Map Visualization */}
        <div className="bg-white rounded-lg border-2 border-blue-200 p-4">
          <h4 className="font-bold text-gray-700 text-sm mb-3">City Map Preview</h4>
          <div className="relative bg-gray-50 rounded-lg border border-gray-300" style={{ aspectRatio: '1' }}>
            <svg width="100%" height="100%" viewBox={`${bounds.minX} ${bounds.minY} ${mapWidth} ${mapHeight}`} preserveAspectRatio="xMidYMid meet">
              {/* Grid */}
              <defs>
                <pattern id="grid" width="1" height="1" patternUnits="userSpaceOnUse">
                  <path d="M 1 0 L 0 0 0 1" fill="none" stroke="gray" strokeWidth="0.05" opacity="0.3"/>
                </pattern>
              </defs>
              <rect x={bounds.minX} y={bounds.minY} width={mapWidth} height={mapHeight} fill="url(#grid)" />
              
              {/* Cities */}
              {cities.map((city, index) => (
                <g key={index}>
                  <circle
                    cx={city.x}
                    cy={city.y}
                    r="0.3"
                    fill="#3b82f6"
                    stroke="white"
                    strokeWidth="0.1"
                  />
                  <text
                    x={city.x}
                    y={city.y - 0.5}
                    textAnchor="middle"
                    fontSize="0.6"
                    fill="#1f2937"
                    fontWeight="bold"
                  >
                    {city.name}
                  </text>
                </g>
              ))}
            </svg>
          </div>
          <p className="text-xs text-gray-500 mt-2 text-center">
            {cities.length} cities on the map
          </p>
        </div>
      </div>

      {/* Statistics */}
      <div className="mt-4 grid grid-cols-3 gap-3">
        <div className="bg-white p-3 rounded-lg border border-blue-200">
          <p className="text-xs text-gray-500 uppercase font-semibold">Total Cities</p>
          <p className="text-xl font-bold text-gray-800">{cities.length}</p>
        </div>
        <div className="bg-white p-3 rounded-lg border border-blue-200">
          <p className="text-xs text-gray-500 uppercase font-semibold">Possible Routes</p>
          <p className="text-xl font-bold text-blue-600">
            {cities.length > 10 ? '> 1M' : Math.floor(factorial(cities.length - 1) / 2).toLocaleString()}
          </p>
        </div>
        <div className="bg-white p-3 rounded-lg border border-blue-200">
          <p className="text-xs text-gray-500 uppercase font-semibold">Map Size</p>
          <p className="text-xl font-bold text-purple-600">
            {mapWidth.toFixed(1)} × {mapHeight.toFixed(1)}
          </p>
        </div>
      </div>

      <div className="mt-3 p-3 bg-blue-50 border-2 border-blue-300 rounded-lg">
        <p className="text-sm text-blue-800">
          💡 <strong>Tip:</strong> The algorithm will find the shortest route that visits all cities exactly once and returns to the start.
        </p>
      </div>
    </div>
  );
}

// Helper function
function factorial(n) {
  if (n <= 1) return 1;
  return n * factorial(n - 1);
}
