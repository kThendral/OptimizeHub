import React, { useState } from 'react';
import HamburgerMenu from '../components/HamburgerMenu';
import AlgorithmInfoSection from '../components/AlgorithmInfoSection';

export default function LearnPage({ onBack, onStartOptimizing }) {
  const [activeSection, setActiveSection] = useState('about');
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const menuSections = [
    { id: 'about', label: 'About', icon: '🏠' },
    { id: 'algorithms', label: 'Evolutionary Algorithms', icon: '🧬' },
    { id: 'guide', label: 'Site Guide', icon: '📖' }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-blue-50 to-indigo-50">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-sm border-b border-purple-100 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            {/* Logo */}
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-br from-blue-500 via-purple-500 to-purple-600 rounded-xl flex items-center justify-center">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-purple-900 to-indigo-900 bg-clip-text text-transparent">
                OptimizeHub
              </h1>
            </div>

            {/* Desktop Navigation */}
            <nav className="hidden md:flex space-x-8">
              {menuSections.map((section) => (
                <button
                  key={section.id}
                  onClick={() => setActiveSection(section.id)}
                  className={`px-4 py-2 rounded-lg font-medium transition-all ${
                    activeSection === section.id
                      ? 'bg-purple-100 text-purple-800'
                      : 'text-gray-600 hover:text-purple-800 hover:bg-purple-50'
                  }`}
                >
                  <span className="mr-2">{section.icon}</span>
                  {section.label}
                </button>
              ))}
            </nav>

            {/* Mobile Menu Button & Action Buttons */}
            <div className="flex items-center gap-3">
              <button
                onClick={onStartOptimizing}
                className="bg-gradient-to-r from-blue-500 via-purple-500 to-purple-600 hover:from-blue-600 hover:via-purple-600 hover:to-purple-700 text-white font-medium py-2 px-4 rounded-lg transition-all duration-300 hover:scale-105 shadow-lg"
              >
                Try Now
              </button>
              
              <button
                onClick={onBack}
                className="text-gray-600 hover:text-purple-800 p-2 rounded-lg hover:bg-purple-50 transition-all"
                title="Back to Home"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
                </svg>
              </button>

              {/* Mobile hamburger button */}
              <button
                className="md:hidden p-2 rounded-lg hover:bg-purple-50 transition-all"
                onClick={() => setIsMenuOpen(!isMenuOpen)}
              >
                <svg className="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              </button>
            </div>
          </div>

          {/* Mobile Navigation */}
          {isMenuOpen && (
            <div className="md:hidden py-4 border-t border-purple-100">
              <nav className="space-y-2">
                {menuSections.map((section) => (
                  <button
                    key={section.id}
                    onClick={() => {
                      setActiveSection(section.id);
                      setIsMenuOpen(false);
                    }}
                    className={`w-full text-left px-4 py-3 rounded-lg font-medium transition-all ${
                      activeSection === section.id
                        ? 'bg-purple-100 text-purple-800'
                        : 'text-gray-600 hover:text-purple-800 hover:bg-purple-50'
                    }`}
                  >
                    <span className="mr-3">{section.icon}</span>
                    {section.label}
                  </button>
                ))}
              </nav>
            </div>
          )}
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeSection === 'about' && <AboutSection />}
        {activeSection === 'algorithms' && <AlgorithmInfoSection onStartOptimizing={onStartOptimizing} />}
        {activeSection === 'guide' && <GuideSection />}
      </main>
    </div>
  );
}

// About Section Component
function AboutSection() {
  return (
    <div className="space-y-8">
      <div className="text-center space-y-4">
        <h2 className="text-4xl font-bold bg-gradient-to-r from-purple-900 via-purple-800 to-indigo-900 bg-clip-text text-transparent">
          About OptimizeHub
        </h2>
        <p className="text-xl text-gray-600 max-w-3xl mx-auto">
          Your gateway to solving complex optimization problems with state-of-the-art evolutionary algorithms
        </p>
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
        {/* Who We Are */}
        <div className="bg-white/70 backdrop-blur-sm rounded-2xl p-6 shadow-lg hover:shadow-xl transition-all duration-300 border border-purple-100">
          <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center mb-4">
            <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
          </div>
          <h3 className="text-xl font-bold text-purple-900 mb-3">Who We Are</h3>
          <p className="text-gray-600 leading-relaxed">
            OptimizeHub is a cutting-edge platform that democratizes access to powerful optimization algorithms. 
            We bridge the gap between complex mathematical concepts and practical problem-solving tools.
          </p>
        </div>

        {/* What We Do */}
        <div className="bg-white/70 backdrop-blur-sm rounded-2xl p-6 shadow-lg hover:shadow-xl transition-all duration-300 border border-purple-100">
          <div className="w-12 h-12 bg-gradient-to-br from-green-500 to-blue-600 rounded-xl flex items-center justify-center mb-4">
            <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
          </div>
          <h3 className="text-xl font-bold text-purple-900 mb-3">What We Do</h3>
          <p className="text-gray-600 leading-relaxed">
            We provide an intuitive interface for running sophisticated optimization algorithms on real-world problems. 
            From logistics optimization to neural network training, we make complex algorithms accessible to everyone.
          </p>
        </div>

        {/* How We Help */}
        <div className="bg-white/70 backdrop-blur-sm rounded-2xl p-6 shadow-lg hover:shadow-xl transition-all duration-300 border border-purple-100 md:col-span-2 lg:col-span-1">
          <div className="w-12 h-12 bg-gradient-to-br from-purple-500 to-pink-600 rounded-xl flex items-center justify-center mb-4">
            <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
            </svg>
          </div>
          <h3 className="text-xl font-bold text-purple-900 mb-3">How We Help You</h3>
          <p className="text-gray-600 leading-relaxed">
            Whether you're a researcher, student, or industry professional, OptimizeHub provides the tools and insights 
            you need to solve optimization challenges efficiently and understand the underlying algorithms.
          </p>
        </div>
      </div>

      {/* Key Benefits */}
      <div className="bg-gradient-to-r from-purple-100 via-blue-100 to-indigo-100 rounded-2xl p-8 mt-8">
        <h3 className="text-2xl font-bold text-purple-900 mb-6 text-center">Why Choose OptimizeHub?</h3>
        <div className="grid md:grid-cols-2 gap-6">
          <div className="space-y-4">
            <div className="flex items-start gap-3">
              <div className="w-6 h-6 rounded-full bg-green-500 flex items-center justify-center flex-shrink-0 mt-1">
                <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <span className="text-gray-700 font-medium">Interactive visualizations for real-time insights</span>
            </div>
            <div className="flex items-start gap-3">
              <div className="w-6 h-6 rounded-full bg-green-500 flex items-center justify-center flex-shrink-0 mt-1">
                <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <span className="text-gray-700 font-medium">No coding required - intuitive web interface</span>
            </div>
            <div className="flex items-start gap-3">
              <div className="w-6 h-6 rounded-full bg-green-500 flex items-center justify-center flex-shrink-0 mt-1">
                <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <span className="text-gray-700 font-medium">Compare multiple algorithms side-by-side</span>
            </div>
          </div>
          <div className="space-y-4">
            <div className="flex items-start gap-3">
              <div className="w-6 h-6 rounded-full bg-green-500 flex items-center justify-center flex-shrink-0 mt-1">
                <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <span className="text-gray-700 font-medium">Educational resources and algorithm explanations</span>
            </div>
            <div className="flex items-start gap-3">
              <div className="w-6 h-6 rounded-full bg-green-500 flex items-center justify-center flex-shrink-0 mt-1">
                <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <span className="text-gray-700 font-medium">Secure custom fitness function execution</span>
            </div>
            <div className="flex items-start gap-3">
              <div className="w-6 h-6 rounded-full bg-green-500 flex items-center justify-center flex-shrink-0 mt-1">
                <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <span className="text-gray-700 font-medium">Export results for further analysis</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// Guide Section Component  
function GuideSection() {
  return (
    <div className="space-y-8">
      <div className="text-center space-y-4">
        <h2 className="text-4xl font-bold bg-gradient-to-r from-purple-900 via-purple-800 to-indigo-900 bg-clip-text text-transparent">
          Site Guide
        </h2>
        <p className="text-xl text-gray-600 max-w-3xl mx-auto">
          Learn how to navigate OptimizeHub and make the most of our optimization tools
        </p>
      </div>

      {/* Three Tab Explanation */}
      <div className="grid lg:grid-cols-3 gap-6">
        {/* Preset Tab */}
        <div className="bg-white/70 backdrop-blur-sm rounded-2xl p-6 shadow-lg border border-blue-100">
          <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl flex items-center justify-center mb-4">
            <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
            </svg>
          </div>
          <h3 className="text-xl font-bold text-blue-900 mb-3">📋 Preset Problems</h3>
          <p className="text-gray-600 mb-4 leading-relaxed">
            Start here if you're new! Choose from classic optimization problems like:
          </p>
          <ul className="space-y-2 text-sm text-gray-600">
            <li className="flex items-center gap-2">
              <span className="w-1.5 h-1.5 bg-blue-500 rounded-full"></span>
              Traveling Salesman Problem (TSP)
            </li>
            <li className="flex items-center gap-2">
              <span className="w-1.5 h-1.5 bg-blue-500 rounded-full"></span>
              Knapsack Problem
            </li>
            <li className="flex items-center gap-2">
              <span className="w-1.5 h-1.5 bg-blue-500 rounded-full"></span>
              Mathematical Functions (Sphere, Rosenbrock)
            </li>
          </ul>
          <div className="mt-4 p-3 bg-blue-50 rounded-lg">
            <p className="text-xs text-blue-800 font-medium">💡 Perfect for learning and quick experimentation</p>
          </div>
        </div>

        {/* YAML Tab */}
        <div className="bg-white/70 backdrop-blur-sm rounded-2xl p-6 shadow-lg border border-green-100">
          <div className="w-12 h-12 bg-gradient-to-br from-green-500 to-green-600 rounded-xl flex items-center justify-center mb-4">
            <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <h3 className="text-xl font-bold text-green-900 mb-3">⚙️ YAML Configuration</h3>
          <p className="text-gray-600 mb-4 leading-relaxed">
            For advanced users who want precise control over algorithm parameters and problem definitions.
          </p>
          <div className="space-y-3 text-sm text-gray-600">
            <div className="flex items-start gap-2">
              <span className="w-1.5 h-1.5 bg-green-500 rounded-full mt-2"></span>
              <div>
                <span className="font-medium">Upload YAML files</span>
                <br />
                <span className="text-xs">Define custom problems and parameters</span>
              </div>
            </div>
            <div className="flex items-start gap-2">
              <span className="w-1.5 h-1.5 bg-green-500 rounded-full mt-2"></span>
              <div>
                <span className="font-medium">Batch processing</span>
                <br />
                <span className="text-xs">Run multiple configurations at once</span>
              </div>
            </div>
          </div>
          <div className="mt-4 p-3 bg-green-50 rounded-lg">
            <p className="text-xs text-green-800 font-medium">⚡ Best for reproducible research and automation</p>
          </div>
        </div>

        {/* Custom Fitness Tab */}
        <div className="bg-white/70 backdrop-blur-sm rounded-2xl p-6 shadow-lg border border-purple-100">
          <div className="w-12 h-12 bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl flex items-center justify-center mb-4">
            <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
            </svg>
          </div>
          <h3 className="text-xl font-bold text-purple-900 mb-3">🔧 Custom Fitness</h3>
          <p className="text-gray-600 mb-4 leading-relaxed">
            Upload your own Python fitness functions for completely custom optimization problems.
          </p>
          <div className="space-y-3 text-sm text-gray-600">
            <div className="flex items-start gap-2">
              <span className="w-1.5 h-1.5 bg-purple-500 rounded-full mt-2"></span>
              <div>
                <span className="font-medium">Python functions</span>
                <br />
                <span className="text-xs">Write custom objective functions</span>
              </div>
            </div>
            <div className="flex items-start gap-2">
              <span className="w-1.5 h-1.5 bg-purple-500 rounded-full mt-2"></span>
              <div>
                <span className="font-medium">Secure execution</span>
                <br />
                <span className="text-xs">Runs in isolated Docker containers</span>
              </div>
            </div>
          </div>
          <div className="mt-4 p-3 bg-purple-50 rounded-lg">
            <p className="text-xs text-purple-800 font-medium">🚀 Unlimited possibilities for real-world problems</p>
          </div>
        </div>
      </div>

      {/* Site Flow */}
      <div className="bg-gradient-to-r from-blue-100 via-purple-100 to-indigo-100 rounded-2xl p-8">
        <h3 className="text-2xl font-bold text-purple-900 mb-6 text-center">🔄 How to Use OptimizeHub</h3>
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="text-center">
            <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl text-white font-bold">1</span>
            </div>
            <h4 className="font-bold text-purple-900 mb-2">Choose Your Problem</h4>
            <p className="text-sm text-gray-600">Select from presets or upload custom configurations</p>
          </div>
          <div className="text-center">
            <div className="w-16 h-16 bg-gradient-to-br from-purple-500 to-pink-600 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl text-white font-bold">2</span>
            </div>
            <h4 className="font-bold text-purple-900 mb-2">Pick Algorithm</h4>
            <p className="text-sm text-gray-600">Choose the best algorithm for your problem type</p>
          </div>
          <div className="text-center">
            <div className="w-16 h-16 bg-gradient-to-br from-pink-500 to-red-600 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl text-white font-bold">3</span>
            </div>
            <h4 className="font-bold text-purple-900 mb-2">Tune Parameters</h4>
            <p className="text-sm text-gray-600">Adjust algorithm settings for optimal performance</p>
          </div>
          <div className="text-center">
            <div className="w-16 h-16 bg-gradient-to-br from-green-500 to-blue-600 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl text-white font-bold">4</span>
            </div>
            <h4 className="font-bold text-purple-900 mb-2">Analyze Results</h4>
            <p className="text-sm text-gray-600">View visualizations and export your solutions</p>
          </div>
        </div>
      </div>

      {/* References Section */}
      <div className="bg-white/70 backdrop-blur-sm rounded-2xl p-8 border border-gray-200">
        <h3 className="text-2xl font-bold text-purple-900 mb-6 text-center">📚 References & Further Reading</h3>
        <div className="grid md:grid-cols-2 gap-6">
          <div>
            <h4 className="font-bold text-gray-800 mb-3">Books & Papers</h4>
            <ul className="space-y-2 text-sm text-gray-600">
              <li>• Eiben & Smith - "Introduction to Evolutionary Computing"</li>
              <li>• Kennedy & Eberhart - "Particle Swarm Optimization" (1995)</li>
              <li>• Dorigo & Stützle - "Ant Colony Optimization"</li>
              <li>• Kirkpatrick et al. - "Simulated Annealing" (1983)</li>
            </ul>
          </div>
          <div>
            <h4 className="font-bold text-gray-800 mb-3">Online Resources</h4>
            <ul className="space-y-2 text-sm text-gray-600">
              <li>• IEEE CIS Evolutionary Computation</li>
              <li>• GECCO Conference Proceedings</li>
              <li>• Swarm Intelligence Research Group</li>
              <li>• OptimizationHub Documentation</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}