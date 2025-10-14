import React from 'react';

const ParameterForm = () => {
  return (
    <div>
      <h2 className="text-2xl font-semibold text-primary mb-4">Algorithm Parameters</h2>
      <label className="block mb-2 font-medium text-gray-700">Configure parameters:</label>
      <input
        type="number"
        placeholder="Population Size"
        className="w-full p-3 border border-gray-300 rounded-lg mb-3 focus:ring-2 focus:ring-[color:var(--color-primary)] focus:border-transparent bg-white"
      />
      <input
        type="number"
        placeholder="Iterations"
        className="w-full p-3 border border-gray-300 rounded-lg mb-3 focus:ring-2 focus:ring-[color:var(--color-primary)] focus:border-transparent bg-white"
      />
      <input
        type="number"
        placeholder="Mutation Rate"
        className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[color:var(--color-primary)] focus:border-transparent bg-white"
      />
    </div>
  );
};

export default ParameterForm;
