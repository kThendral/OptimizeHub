import { useState } from 'react';

/**
 * Custom input form for Knapsack Problem.
 * Allows users to define items with weights/values and set capacity.
 */
export default function KnapsackInputForm({ formData, onChange }) {
  const [items, setItems] = useState(formData.items || [
    { name: 'Item 1', weight: 2, value: 3 },
    { name: 'Item 2', weight: 3, value: 4 },
    { name: 'Item 3', weight: 4, value: 5 },
    { name: 'Item 4', weight: 5, value: 6 }
  ]);
  const [capacity, setCapacity] = useState(formData.capacity || 10);

  const handleItemChange = (index, field, value) => {
    const newItems = [...items];
    newItems[index][field] = field === 'name' ? value : parseFloat(value) || 0;
    setItems(newItems);
    updateFormData(newItems, capacity);
  };

  const addItem = () => {
    const newItems = [...items, { name: `Item ${items.length + 1}`, weight: 1, value: 1 }];
    setItems(newItems);
    updateFormData(newItems, capacity);
  };

  const removeItem = (index) => {
    const newItems = items.filter((_, i) => i !== index);
    setItems(newItems);
    updateFormData(newItems, capacity);
  };

  const handleCapacityChange = (value) => {
    setCapacity(parseFloat(value) || 0);
    updateFormData(items, parseFloat(value) || 0);
  };

  const updateFormData = (itemsList, cap) => {
    onChange({
      ...formData,
      items: itemsList,
      capacity: cap,
      dimensions: itemsList.length,
      problemType: 'knapsack'
    });
  };

  const totalWeight = items.reduce((sum, item) => sum + item.weight, 0);
  const totalValue = items.reduce((sum, item) => sum + item.value, 0);

  return (
    <div className="mb-4 p-5 bg-gradient-to-br from-orange-50 to-yellow-50 rounded-xl border-2 border-orange-300 shadow-sm">
      <div className="flex items-center gap-2 mb-4">
        <span className="text-2xl">🎒</span>
        <h3 className="font-bold text-gray-800 text-lg">Knapsack Problem Configuration</h3>
      </div>

      {/* Capacity Input */}
      <div className="mb-4 p-4 bg-white rounded-lg border-2 border-orange-200">
        <label className="block text-sm font-semibold text-gray-700 mb-2">
          Knapsack Capacity (Maximum Weight):
        </label>
        <input
          type="number"
          step="0.1"
          min="0"
          value={capacity}
          onChange={e => handleCapacityChange(e.target.value)}
          className="w-full p-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500 text-lg font-semibold"
        />
        <p className="text-xs text-gray-500 mt-1">
          Maximum total weight the knapsack can hold
        </p>
      </div>

      {/* Items Table */}
      <div className="bg-white rounded-lg border-2 border-orange-200 overflow-hidden">
        <div className="bg-gradient-to-r from-orange-500 to-yellow-500 px-4 py-2">
          <h4 className="font-bold text-white text-sm">Items Available</h4>
        </div>
        
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="bg-gray-100 border-b-2 border-orange-200">
              <tr>
                <th className="px-4 py-2 text-left font-semibold text-gray-700">Item Name</th>
                <th className="px-4 py-2 text-left font-semibold text-gray-700">Weight</th>
                <th className="px-4 py-2 text-left font-semibold text-gray-700">Value</th>
                <th className="px-4 py-2 text-left font-semibold text-gray-700">Value/Weight</th>
                <th className="px-4 py-2 text-center font-semibold text-gray-700">Action</th>
              </tr>
            </thead>
            <tbody>
              {items.map((item, index) => (
                <tr key={index} className="border-b border-gray-200 hover:bg-orange-50">
                  <td className="px-4 py-2">
                    <input
                      type="text"
                      value={item.name}
                      onChange={e => handleItemChange(index, 'name', e.target.value)}
                      className="w-full p-2 border border-gray-300 rounded focus:ring-1 focus:ring-orange-500"
                    />
                  </td>
                  <td className="px-4 py-2">
                    <input
                      type="number"
                      step="0.1"
                      min="0"
                      value={item.weight}
                      onChange={e => handleItemChange(index, 'weight', e.target.value)}
                      className="w-24 p-2 border border-gray-300 rounded focus:ring-1 focus:ring-orange-500"
                    />
                  </td>
                  <td className="px-4 py-2">
                    <input
                      type="number"
                      step="0.1"
                      min="0"
                      value={item.value}
                      onChange={e => handleItemChange(index, 'value', e.target.value)}
                      className="w-24 p-2 border border-gray-300 rounded focus:ring-1 focus:ring-orange-500"
                    />
                  </td>
                  <td className="px-4 py-2 text-gray-600 font-mono">
                    {item.weight > 0 ? (item.value / item.weight).toFixed(2) : '0.00'}
                  </td>
                  <td className="px-4 py-2 text-center">
                    <button
                      onClick={() => removeItem(index)}
                      disabled={items.length <= 1}
                      className="text-red-600 hover:text-red-800 disabled:text-gray-300 disabled:cursor-not-allowed font-bold"
                      title="Remove item"
                    >
                      ✕
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
            <tfoot className="bg-orange-50 border-t-2 border-orange-300">
              <tr className="font-semibold">
                <td className="px-4 py-2">Total if all selected:</td>
                <td className="px-4 py-2 text-orange-700">{totalWeight.toFixed(1)}</td>
                <td className="px-4 py-2 text-green-700">{totalValue.toFixed(1)}</td>
                <td className="px-4 py-2"></td>
                <td className="px-4 py-2"></td>
              </tr>
            </tfoot>
          </table>
        </div>

        <div className="p-3 bg-gray-50 border-t border-gray-200">
          <button
            onClick={addItem}
            className="w-full bg-gradient-to-r from-orange-500 to-yellow-500 hover:from-orange-600 hover:to-yellow-600 text-white font-semibold py-2 px-4 rounded-lg transition-all duration-200 shadow-md"
          >
            + Add Item
          </button>
        </div>
      </div>

      {/* Statistics */}
      <div className="mt-4 grid grid-cols-3 gap-3">
        <div className="bg-white p-3 rounded-lg border border-orange-200">
          <p className="text-xs text-gray-500 uppercase font-semibold">Total Items</p>
          <p className="text-xl font-bold text-gray-800">{items.length}</p>
        </div>
        <div className="bg-white p-3 rounded-lg border border-orange-200">
          <p className="text-xs text-gray-500 uppercase font-semibold">Capacity</p>
          <p className="text-xl font-bold text-orange-600">{capacity.toFixed(1)}</p>
        </div>
        <div className="bg-white p-3 rounded-lg border border-orange-200">
          <p className="text-xs text-gray-500 uppercase font-semibold">Utilization</p>
          <p className="text-xl font-bold text-purple-600">
            {capacity > 0 ? Math.min(100, (totalWeight / capacity * 100)).toFixed(0) : 0}%
          </p>
        </div>
      </div>

      {totalWeight > capacity && (
        <div className="mt-3 p-3 bg-yellow-50 border-2 border-yellow-300 rounded-lg">
          <p className="text-sm text-yellow-800">
            ⚠️ <strong>Note:</strong> Total weight ({totalWeight.toFixed(1)}) exceeds capacity ({capacity.toFixed(1)}). 
            The algorithm will find the best combination that fits.
          </p>
        </div>
      )}
    </div>
  );
}
