export default function LandingPage({ onStart }) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-gray-100 flex items-center justify-center px-4">
      <div className="text-center max-w-2xl">
        <h1 className="text-5xl font-bold text-blue-600 mb-6">OptimizeHub</h1>
        <p className="text-xl text-gray-700 mb-8 leading-relaxed">
          Visualize and compare optimization algorithms like PSO, GA, and DE. Upload a problem, configure parameters, and view performance results.
        </p>
        <button
          onClick={onStart}
          className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-8 rounded-lg shadow-md transition duration-300"
        >
          Get Started
        </button>
      </div>
    </div>
  );
}
