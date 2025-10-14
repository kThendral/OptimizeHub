export default function LandingPage({ onStart }) {
  return (
    <div className="min-h-screen flex">
      {/* Left Side - 1/3 width - Dark Purple with Gradient - Brand & Button */}
      <div className="w-full lg:w-1/3 bg-gradient-to-br from-purple-900 via-purple-800 to-indigo-900 flex flex-col items-center justify-center p-8 lg:p-12 relative overflow-hidden">
        {/* Subtle animated gradient overlay */}
        <div className="absolute inset-0 bg-gradient-to-tr from-purple-600/20 via-transparent to-blue-600/20 opacity-50"></div>
        
        <div className="relative z-10 text-center space-y-8">
          {/* Logo */}
          <div className="flex flex-col items-center gap-4">
            <div className="w-16 h-16 bg-gradient-to-br from-blue-400 via-purple-400 to-purple-600 rounded-2xl flex items-center justify-center shadow-lg shadow-purple-500/50">
              <svg className="w-9 h-9 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <h1 className="text-5xl font-bold bg-gradient-to-r from-white via-purple-100 to-blue-100 bg-clip-text text-transparent">
              OptimizeHub
            </h1>
          </div>

          {/* Get Started Button */}
          <button
            onClick={onStart}
            className="bg-gradient-to-r from-blue-500 via-purple-500 to-purple-600 hover:from-blue-600 hover:via-purple-600 hover:to-purple-700 text-white font-semibold py-4 px-12 rounded-xl shadow-xl shadow-purple-500/30 transform transition-all duration-300 hover:scale-105 hover:shadow-2xl hover:shadow-purple-500/50 flex items-center justify-center gap-2 mx-auto"
          >
            <span className="text-lg">Get Started</span>
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
          </button>
        </div>
      </div>

      {/* Right Side - 2/3 width - Light Purple with Gradient - Description & Features */}
      <div className="hidden lg:flex lg:w-2/3 bg-gradient-to-br from-purple-50 via-purple-100 to-blue-50 items-center justify-center p-12 relative overflow-hidden">
        {/* Subtle gradient orbs in background */}
        <div className="absolute top-0 right-0 w-96 h-96 bg-gradient-to-br from-purple-200 to-transparent rounded-full blur-3xl opacity-30"></div>
        <div className="absolute bottom-0 left-0 w-96 h-96 bg-gradient-to-tr from-blue-200 to-transparent rounded-full blur-3xl opacity-30"></div>
        
        <div className="relative z-10 max-w-2xl space-y-8">
          {/* Heading */}
          <div className="space-y-4">
            <h2 className="text-4xl font-bold bg-gradient-to-r from-purple-900 via-purple-800 to-indigo-900 bg-clip-text text-transparent">
              Solve Complex Problems with AI-Powered Optimization
            </h2>
            <p className="text-xl text-purple-800 leading-relaxed">
              Harness the power of advanced algorithms like Particle Swarm Optimization and Genetic Algorithms to tackle real-world challenges.
            </p>
          </div>

          {/* Feature List */}
          <ul className="space-y-4">
            <li className="flex items-start gap-4">
              <div className="flex-shrink-0 w-6 h-6 rounded-full bg-gradient-to-br from-green-400 to-green-600 flex items-center justify-center mt-1 shadow-md">
                <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <span className="text-lg text-purple-900 font-medium">Solve TSP, Knapsack & benchmark functions</span>
            </li>
            <li className="flex items-start gap-4">
              <div className="flex-shrink-0 w-6 h-6 rounded-full bg-gradient-to-br from-green-400 to-green-600 flex items-center justify-center mt-1 shadow-md">
                <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <span className="text-lg text-purple-900 font-medium">Real-time convergence visualization</span>
            </li>
            <li className="flex items-start gap-4">
              <div className="flex-shrink-0 w-6 h-6 rounded-full bg-gradient-to-br from-green-400 to-green-600 flex items-center justify-center mt-1 shadow-md">
                <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <span className="text-lg text-purple-900 font-medium">Compare multiple algorithm performance</span>
            </li>
            <li className="flex items-start gap-4">
              <div className="flex-shrink-0 w-6 h-6 rounded-full bg-gradient-to-br from-green-400 to-green-600 flex items-center justify-center mt-1 shadow-md">
                <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <span className="text-lg text-purple-900 font-medium">Human-readable solution decoding</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
}
