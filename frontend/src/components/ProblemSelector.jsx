import React from 'react';

const ProblemSelector = () => {
  return (
    <div>
      <h2 className="text-2xl font-semibold text-gray-800 mb-4">Select Problem</h2>
      <label className="block mb-2 font-medium text-gray-700">Choose an optimization problem:</label>
      <select className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white">
        <option value="sphere">Sphere</option>
        <option value="rastrigin">Rastrigin</option>
        <option value="ackley">Ackley</option>
        <option value="griewank">Griewank</option>
        <option value="rosenbrock">Rosenbrock</option>
      </select>
    </div>
  );
};

export default ProblemSelector;
