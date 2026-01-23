import React, { useState, useEffect } from 'react';
import './LandingPage.css';

export default function LandingPage({ onStart, onLearn }) {
  const [scrollProgress, setScrollProgress] = useState(0);

  useEffect(() => {
    const handleScroll = () => {
      const windowHeight = window.innerHeight;
      const fullHeight = document.documentElement.scrollHeight - windowHeight;
      const scrolled = window.scrollY;
      setScrollProgress(scrolled / fullHeight);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <div className="w-full overflow-hidden">
      {/* ========== HERO SECTION ========== */}
      <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
        {/* Animated gradient background */}
        <div className="absolute inset-0 bg-gradient-to-br from-purple-900 via-indigo-900 to-blue-900 -z-20"></div>
        
        {/* Animated gradient orbs */}
        <div className="absolute top-20 left-10 w-72 h-72 bg-blue-500/20 rounded-full blur-3xl animate-float"></div>
        <div className="absolute bottom-20 right-10 w-96 h-96 bg-purple-500/20 rounded-full blur-3xl animate-float-delayed"></div>
        <div className="absolute top-1/2 left-1/2 w-80 h-80 bg-cyan-500/10 rounded-full blur-3xl animate-float-slow"></div>

        {/* Grid pattern overlay */}
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_80%_80%_at_50%_-20%,rgba(120,119,198,0.3),rgba(255,255,255,0))] -z-10"></div>

        <div className="relative z-10 max-w-6xl mx-auto px-6 lg:px-12 py-20">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            {/* Left Content */}
            <div className="space-y-8">
              {/* Logo & Brand */}
              <div className="flex items-center gap-4 animate-fade-in" style={{ animationDelay: '0.1s' }}>
                <div className="w-14 h-14 bg-gradient-to-br from-cyan-400 via-blue-500 to-purple-600 rounded-2xl flex items-center justify-center shadow-lg shadow-purple-500/50 hover:shadow-purple-500/80 transition-all duration-300 transform hover:scale-110">
                  <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                </div>
                <span className="text-sm font-semibold text-cyan-300 uppercase tracking-widest">Advanced Optimization</span>
              </div>

              {/* Main Headline */}
              <div className="space-y-4 animate-fade-in" style={{ animationDelay: '0.2s' }}>
                <h1 className="text-5xl lg:text-6xl font-bold leading-tight">
                  <span className="bg-gradient-to-r from-white via-blue-100 to-cyan-200 bg-clip-text text-transparent">
                    Solve Complex Problems with
                  </span>
                  <br />
                  <span className="bg-gradient-to-r from-cyan-300 via-blue-400 to-purple-400 bg-clip-text text-transparent animate-gradient">
                    AI-Powered Algorithms
                  </span>
                </h1>
              </div>

              {/* Subheading */}
              <p className="text-lg text-gray-300 leading-relaxed max-w-xl animate-fade-in" style={{ animationDelay: '0.3s' }}>
                OptimizeHub brings cutting-edge metaheuristic algorithms to your fingertips. Visualize, compare, and master optimization techniques that solve real-world challenges.
              </p>

              {/* CTA Buttons */}
              <div className="flex flex-col sm:flex-row gap-4 pt-4 animate-fade-in" style={{ animationDelay: '0.4s' }}>
                <button
                  onClick={onStart}
                  className="group relative px-8 py-4 text-lg font-semibold text-white rounded-xl overflow-hidden shadow-2xl shadow-purple-500/30 hover:shadow-purple-500/60 transition-all duration-300 transform hover:scale-105"
                >
                  {/* Animated background gradient */}
                  <div className="absolute inset-0 bg-gradient-to-r from-cyan-500 via-blue-500 to-purple-600 -z-10 group-hover:from-cyan-600 group-hover:via-blue-600 group-hover:to-purple-700 transition-all duration-300"></div>
                  
                  <div className="flex items-center justify-center gap-2">
                    <span>Start Optimizing</span>
                    <svg className="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                    </svg>
                  </div>
                </button>

                <button
                  onClick={onLearn}
                  className="group px-8 py-4 text-lg font-semibold text-white rounded-xl border-2 border-white/30 hover:border-white/60 backdrop-blur-sm bg-white/5 hover:bg-white/10 transition-all duration-300 transform hover:scale-105 flex items-center justify-center gap-2"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                  </svg>
                  <span>Learn Algorithms</span>
                </button>
              </div>

              {/* Trust badges */}
              <div className="flex flex-wrap gap-6 pt-8 text-sm text-gray-400 animate-fade-in" style={{ animationDelay: '0.5s' }}>
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 rounded-full bg-cyan-400"></div>
                  <span>6+ Algorithms</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 rounded-full bg-cyan-400"></div>
                  <span>Real-time Visualization</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 rounded-full bg-cyan-400"></div>
                  <span>Custom Problems</span>
                </div>
              </div>
            </div>

            {/* Right Side - Animated Illustration */}
            <div className="hidden lg:flex items-center justify-center relative h-96 animate-fade-in-right" style={{ animationDelay: '0.3s' }}>
              {/* Floating animated shapes */}
              <div className="absolute inset-0 flex items-center justify-center">
                {/* Center glowing circle */}
                <div className="absolute w-32 h-32 rounded-full bg-gradient-to-br from-cyan-400 to-blue-600 opacity-20 blur-2xl animate-pulse"></div>
                
                {/* Animated nodes */}
                <svg className="w-full h-full max-w-xs" viewBox="0 0 300 300" fill="none" xmlns="http://www.w3.org/2000/svg">
                  {/* Central node */}
                  <circle cx="150" cy="150" r="12" fill="url(#gradientMain)" className="animate-glow-pulse" />
                  
                  {/* Orbiting nodes */}
                  {[0, 1, 2, 3, 4].map((i) => {
                    const angle = (i * 72) * Math.PI / 180;
                    const radius = 90;
                    const x = 150 + radius * Math.cos(angle);
                    const y = 150 + radius * Math.sin(angle);
                    return (
                      <g key={i}>
                        {/* Connection line */}
                        <line x1="150" y1="150" x2={x} y2={y} stroke="url(#gradientLine)" strokeWidth="2" opacity="0.6" />
                        {/* Node */}
                        <circle cx={x} cy={y} r="8" fill="url(#gradientNode)" className="animate-float" style={{ animationDelay: `${i * 0.1}s` }} />
                      </g>
                    );
                  })}

                  <defs>
                    <linearGradient id="gradientMain" x1="0%" y1="0%" x2="100%" y2="100%">
                      <stop offset="0%" stopColor="#06B6D4" />
                      <stop offset="100%" stopColor="#8B5CF6" />
                    </linearGradient>
                    <linearGradient id="gradientNode" x1="0%" y1="0%" x2="100%" y2="100%">
                      <stop offset="0%" stopColor="#3B82F6" />
                      <stop offset="100%" stopColor="#EC4899" />
                    </linearGradient>
                    <linearGradient id="gradientLine" x1="0%" y1="0%" x2="100%" y2="100%">
                      <stop offset="0%" stopColor="#06B6D4" opacity="0.8" />
                      <stop offset="100%" stopColor="#8B5CF6" opacity="0.4" />
                    </linearGradient>
                  </defs>
                </svg>
              </div>
            </div>
          </div>
        </div>

        {/* Scroll indicator */}
        <div className="absolute bottom-8 left-1/2 -translate-x-1/2 animate-bounce">
          <svg className="w-6 h-6 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 14l-7 7m0 0l-7-7m7 7V3" />
          </svg>
        </div>
      </section>

      {/* ========== FEATURES SECTION ========== */}
      <section className="py-20 lg:py-32 px-6 lg:px-12 relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-slate-950 via-slate-900 to-slate-900/90 -z-10"></div>
        
        {/* Floating orbs */}
        <div className="absolute -top-20 -right-20 w-80 h-80 bg-cyan-500/10 rounded-full blur-3xl"></div>
        <div className="absolute -bottom-20 -left-20 w-80 h-80 bg-purple-500/10 rounded-full blur-3xl"></div>

        <div className="max-w-6xl mx-auto">
          {/* Section Header */}
          <div className="text-center mb-16 space-y-4">
            <h2 className="text-4xl lg:text-5xl font-bold">
              <span className="bg-gradient-to-r from-white via-blue-100 to-cyan-200 bg-clip-text text-transparent">
                Powerful Features Built for
              </span>
              <br />
              <span className="bg-gradient-to-r from-cyan-300 to-purple-400 bg-clip-text text-transparent">
                Optimization Success
              </span>
            </h2>
            <p className="text-lg text-gray-400 max-w-2xl mx-auto">
              Everything you need to understand and apply advanced optimization algorithms to real-world problems.
            </p>
          </div>

          {/* Features Grid */}
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 lg:gap-8">
            {/* Feature 1 */}
            <div className="group relative h-full">
              <div className="absolute inset-0 bg-gradient-to-r from-cyan-500/25 to-blue-500/25 rounded-2xl blur-xl group-hover:blur-2xl transition-all duration-300 opacity-70 group-hover:opacity-100"></div>
              <div className="relative h-full p-8 rounded-2xl bg-slate-900/85 border border-slate-700 hover:border-cyan-300/70 transition-all duration-300 hover:bg-slate-900/95 flex flex-col gap-6 shadow-xl shadow-black/30">
                <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-cyan-400 to-blue-600 flex items-center justify-center group-hover:scale-110 transition-transform">
                  <svg className="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                </div>
                <div>
                  <h3 className="text-xl font-bold text-white mb-2">Algorithm Comparison</h3>
                  <p className="text-gray-100 leading-relaxed">
                    Run and compare 6+ algorithms side-by-side. Visualize convergence patterns and performance metrics in real-time.
                  </p>
                </div>
                <div className="flex gap-2 flex-wrap">
                  <span className="text-xs px-3 py-1 rounded-full bg-cyan-600/30 text-cyan-50 border border-cyan-400/70">PSO</span>
                  <span className="text-xs px-3 py-1 rounded-full bg-blue-600/30 text-blue-50 border border-blue-400/70">GA</span>
                  <span className="text-xs px-3 py-1 rounded-full bg-purple-600/30 text-purple-50 border border-purple-400/70">DE</span>
                </div>
              </div>
            </div>

            {/* Feature 2 */}
            <div className="group relative h-full">
              <div className="absolute inset-0 bg-gradient-to-r from-purple-500/25 to-pink-500/25 rounded-2xl blur-xl group-hover:blur-2xl transition-all duration-300 opacity-70 group-hover:opacity-100"></div>
              <div className="relative h-full p-8 rounded-2xl bg-slate-900/85 border border-slate-700 hover:border-purple-300/70 transition-all duration-300 hover:bg-slate-900/95 flex flex-col gap-6 shadow-xl shadow-black/30">
                <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-purple-400 to-pink-600 flex items-center justify-center group-hover:scale-110 transition-transform">
                  <svg className="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
                  </svg>
                </div>
                <div>
                  <h3 className="text-xl font-bold text-white mb-2">Problem Solving</h3>
                  <p className="text-gray-100 leading-relaxed">
                    Solve TSP, Knapsack, benchmark functions, and custom problems. Upload your own fitness functions easily.
                  </p>
                </div>
                <div className="flex gap-2 flex-wrap">
                  <span className="text-xs px-3 py-1 rounded-full bg-purple-600/30 text-purple-50 border border-purple-400/70">TSP</span>
                  <span className="text-xs px-3 py-1 rounded-full bg-pink-600/30 text-pink-50 border border-pink-400/70">Custom</span>
                </div>
              </div>
            </div>

            {/* Feature 3 */}
            <div className="group relative h-full">
              <div className="absolute inset-0 bg-gradient-to-r from-green-500/25 to-teal-500/25 rounded-2xl blur-xl group-hover:blur-2xl transition-all duration-300 opacity-70 group-hover:opacity-100"></div>
              <div className="relative h-full p-8 rounded-2xl bg-slate-900/85 border border-slate-700 hover:border-green-300/70 transition-all duration-300 hover:bg-slate-900/95 flex flex-col gap-6 shadow-xl shadow-black/30">
                <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-green-400 to-teal-600 flex items-center justify-center group-hover:scale-110 transition-transform">
                  <svg className="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                </div>
                <div>
                  <h3 className="text-xl font-bold text-white mb-2">Live Convergence</h3>
                  <p className="text-gray-100 leading-relaxed">
                    Watch algorithms converge in real-time with beautiful interactive charts showing fitness progression and diversity.
                  </p>
                </div>
                <div className="flex gap-2 flex-wrap">
                  <span className="text-xs px-3 py-1 rounded-full bg-green-600/30 text-green-50 border border-green-400/70">Charts</span>
                  <span className="text-xs px-3 py-1 rounded-full bg-teal-600/30 text-teal-50 border border-teal-400/70">Live</span>
                </div>
              </div>
            </div>

            {/* Feature 4 */}
            <div className="group relative h-full">
              <div className="absolute inset-0 bg-gradient-to-r from-blue-500/25 to-cyan-500/25 rounded-2xl blur-xl group-hover:blur-2xl transition-all duration-300 opacity-70 group-hover:opacity-100"></div>
              <div className="relative h-full p-8 rounded-2xl bg-slate-900/85 border border-slate-700 hover:border-blue-300/70 transition-all duration-300 hover:bg-slate-900/95 flex flex-col gap-6 shadow-xl shadow-black/30">
                <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-blue-400 to-indigo-600 flex items-center justify-center group-hover:scale-110 transition-transform">
                  <svg className="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4" />
                  </svg>
                </div>
                <div>
                  <h3 className="text-xl font-bold text-white mb-2">Fine-Tune Parameters</h3>
                  <p className="text-gray-100 leading-relaxed">
                    Adjust algorithm parameters and see instant feedback. Experiment with different configurations to optimize performance.
                  </p>
                </div>
                <div className="flex gap-2 flex-wrap">
                  <span className="text-xs px-3 py-1 rounded-full bg-blue-600/30 text-blue-50 border border-blue-400/70">Tuning</span>
                  <span className="text-xs px-3 py-1 rounded-full bg-indigo-600/30 text-indigo-50 border border-indigo-400/70">Flexible</span>
                </div>
              </div>
            </div>

            {/* Feature 5 */}
            <div className="group relative h-full">
              <div className="absolute inset-0 bg-gradient-to-r from-orange-500/25 to-yellow-500/25 rounded-2xl blur-xl group-hover:blur-2xl transition-all duration-300 opacity-70 group-hover:opacity-100"></div>
              <div className="relative h-full p-8 rounded-2xl bg-slate-900/85 border border-slate-700 hover:border-orange-300/70 transition-all duration-300 hover:bg-slate-900/95 flex flex-col gap-6 shadow-xl shadow-black/30">
                <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-orange-400 to-yellow-600 flex items-center justify-center group-hover:scale-110 transition-transform">
                  <svg className="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                </div>
                <div>
                  <h3 className="text-xl font-bold text-white mb-2">Solution Decoding</h3>
                  <p className="text-gray-100 leading-relaxed">
                    Get human-readable solutions with clear explanations of how algorithms solved your problem.
                  </p>
                </div>
                <div className="flex gap-2 flex-wrap">
                  <span className="text-xs px-3 py-1 rounded-full bg-orange-600/30 text-orange-50 border border-orange-400/70">Results</span>
                  <span className="text-xs px-3 py-1 rounded-full bg-yellow-600/30 text-yellow-50 border border-yellow-400/70">Clear</span>
                </div>
              </div>
            </div>

            {/* Feature 6 */}
            <div className="group relative h-full">
              <div className="absolute inset-0 bg-gradient-to-r from-red-500/25 to-pink-500/25 rounded-2xl blur-xl group-hover:blur-2xl transition-all duration-300 opacity-70 group-hover:opacity-100"></div>
              <div className="relative h-full p-8 rounded-2xl bg-slate-900/85 border border-slate-700 hover:border-red-300/70 transition-all duration-300 hover:bg-slate-900/95 flex flex-col gap-6 shadow-xl shadow-black/30">
                <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-red-400 to-pink-600 flex items-center justify-center group-hover:scale-110 transition-transform">
                  <svg className="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                  </svg>
                </div>
                <div>
                  <h3 className="text-xl font-bold text-white mb-2">Learn & Master</h3>
                  <p className="text-gray-100 leading-relaxed">
                    Interactive educational section to understand how each algorithm works and when to use them.
                  </p>
                </div>
                <div className="flex gap-2 flex-wrap">
                  <span className="text-xs px-3 py-1 rounded-full bg-red-600/30 text-red-50 border border-red-400/70">Education</span>
                  <span className="text-xs px-3 py-1 rounded-full bg-pink-600/30 text-pink-50 border border-pink-400/70">Learning</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ========== WHY IT MATTERS SECTION ========== */}
      <section className="py-20 lg:py-32 px-6 lg:px-12 relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-slate-950/95 via-slate-900/90 to-slate-950/95 -z-10"></div>

        <div className="max-w-6xl mx-auto">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            {/* Left Content */}
            <div className="space-y-8">
              <h2 className="text-4xl lg:text-5xl font-bold leading-tight">
                <span className="bg-gradient-to-r from-white via-blue-100 to-cyan-200 bg-clip-text text-transparent">
                  Why Optimization Matters
                </span>
              </h2>

              <p className="text-lg text-gray-100 leading-relaxed">
                In today's complex world, finding the best solution quickly is critical. Whether you're optimizing delivery routes, resource allocation, or machine learning parameters, the right algorithm makes all the difference.
              </p>

              <ul className="space-y-4">
                {[
                  { title: 'Save Time & Resources', desc: 'Find near-optimal solutions faster than brute force methods' },
                  { title: 'Scale to Complexity', desc: 'Handle problems with thousands of variables efficiently' },
                  { title: 'Learn by Doing', desc: 'Understand algorithm behavior through hands-on experimentation' },
                  { title: 'Make Better Decisions', desc: 'Compare different approaches to choose the best fit' }
                ].map((item, i) => (
                  <li key={i} className="flex gap-4">
                    <div className="flex-shrink-0 w-6 h-6 rounded-full bg-gradient-to-br from-cyan-400 to-blue-600 flex items-center justify-center mt-1">
                      <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M5 13l4 4L19 7" />
                      </svg>
                    </div>
                    <div>
                      <h4 className="font-bold text-white">{item.title}</h4>
                      <p className="text-gray-200 text-sm">{item.desc}</p>
                    </div>
                  </li>
                ))}
              </ul>

              <button
                onClick={onStart}
                className="inline-flex items-center gap-2 px-8 py-4 mt-4 text-white font-semibold rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700 transition-all duration-300 transform hover:scale-105 shadow-lg shadow-cyan-500/30 hover:shadow-cyan-500/60"
              >
                <span>Start Experimenting</span>
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                </svg>
              </button>
            </div>

            {/* Right Side - Illustration */}
            <div className="relative h-96 hidden lg:flex items-center justify-center">
              {/* Animated graph */}
              <svg className="w-full h-full max-w-sm" viewBox="0 0 300 300" fill="none" xmlns="http://www.w3.org/2000/svg">
                {/* Grid lines */}
                <defs>
                  <linearGradient id="barGradient1" x1="0%" y1="0%" x2="0%" y2="100%">
                    <stop offset="0%" stopColor="#06B6D4" />
                    <stop offset="100%" stopColor="#0891B2" />
                  </linearGradient>
                  <linearGradient id="barGradient2" x1="0%" y1="0%" x2="0%" y2="100%">
                    <stop offset="0%" stopColor="#3B82F6" />
                    <stop offset="100%" stopColor="#1E40AF" />
                  </linearGradient>
                  <linearGradient id="barGradient3" x1="0%" y1="0%" x2="0%" y2="100%">
                    <stop offset="0%" stopColor="#8B5CF6" />
                    <stop offset="100%" stopColor="#6D28D9" />
                  </linearGradient>
                </defs>

                {/* Background grid */}
                <line x1="30" y1="250" x2="280" y2="250" stroke="#6B7280" strokeWidth="2" />
                <line x1="30" y1="250" x2="30" y2="30" stroke="#6B7280" strokeWidth="2" />

                {/* Grid helper lines */}
                {[1, 2, 3, 4].map((i) => (
                  <line key={`h${i}`} x1="30" y1={250 - (i * 50)} x2="280" y2={250 - (i * 50)} stroke="#6B7280" strokeWidth="1" opacity="0.4" />
                ))}

                {/* Bars with animation */}
                <rect x="60" y="150" width="40" height="100" fill="url(#barGradient1)" rx="4" className="animate-bar-grow" style={{ animationDelay: '0s' }} />
                <rect x="120" y="100" width="40" height="150" fill="url(#barGradient2)" rx="4" className="animate-bar-grow" style={{ animationDelay: '0.2s' }} />
                <rect x="180" y="80" width="40" height="170" fill="url(#barGradient3)" rx="4" className="animate-bar-grow" style={{ animationDelay: '0.4s' }} />

                {/* Labels */}
                <text x="80" y="270" fill="#E5E7EB" fontSize="12" textAnchor="middle">PSO</text>
                <text x="140" y="270" fill="#E5E7EB" fontSize="12" textAnchor="middle">GA</text>
                <text x="200" y="270" fill="#E5E7EB" fontSize="12" textAnchor="middle">DE</text>
              </svg>
            </div>
          </div>
        </div>
      </section>

      {/* ========== CTA SECTION ========== */}
      <section className="py-20 lg:py-32 px-6 lg:px-12 relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-purple-900 via-indigo-900 to-blue-900 -z-20"></div>
        
        {/* Animated orbs */}
        <div className="absolute top-0 left-1/4 w-80 h-80 bg-cyan-500/20 rounded-full blur-3xl animate-float-slow"></div>
        <div className="absolute bottom-0 right-1/4 w-80 h-80 bg-purple-500/20 rounded-full blur-3xl animate-float-delayed"></div>

        <div className="max-w-4xl mx-auto text-center space-y-8 relative z-10">
          <h2 className="text-4xl lg:text-5xl font-bold leading-tight">
            <span className="bg-gradient-to-r from-white via-blue-100 to-cyan-200 bg-clip-text text-transparent">
              Ready to Master Optimization?
            </span>
          </h2>

          <p className="text-xl text-gray-300 max-w-2xl mx-auto">
            Join thousands of students and professionals learning advanced optimization techniques. Start with pre-built problems or upload your own.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center pt-8">
            <button
              onClick={onStart}
              className="group relative px-10 py-5 text-lg font-semibold text-white rounded-xl overflow-hidden shadow-2xl shadow-cyan-500/40 hover:shadow-cyan-500/70 transition-all duration-300 transform hover:scale-105"
            >
              <div className="absolute inset-0 bg-gradient-to-r from-cyan-500 via-blue-500 to-purple-600 -z-10 group-hover:from-cyan-600 group-hover:via-blue-600 group-hover:to-purple-700 transition-all duration-300"></div>
              <div className="flex items-center justify-center gap-2">
                <span>Start Now</span>
                <svg className="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                </svg>
              </div>
            </button>

            <button
              onClick={onLearn}
              className="px-10 py-5 text-lg font-semibold text-white rounded-xl border-2 border-white/30 hover:border-white/60 backdrop-blur-sm bg-white/5 hover:bg-white/10 transition-all duration-300 transform hover:scale-105"
            >
              Explore Algorithms
            </button>
          </div>
        </div>
      </section>

      {/* ========== FOOTER ========== */}
      <footer className="py-12 px-6 lg:px-12 border-t border-slate-800 bg-slate-950/95">
        <div className="max-w-6xl mx-auto">
          <div className="grid md:grid-cols-4 gap-8 mb-8">
            {/* Brand */}
            <div className="space-y-4">
              <div className="flex items-center gap-2">
                <div className="w-10 h-10 bg-gradient-to-br from-cyan-400 to-purple-600 rounded-lg flex items-center justify-center">
                  <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                </div>
                <span className="font-bold text-white">OptimizeHub</span>
              </div>
              <p className="text-sm text-gray-200">Master optimization algorithms with hands-on experimentation.</p>
            </div>

            {/* Quick Links */}
            <div>
              <h4 className="font-semibold text-white mb-4">Explore</h4>
              <ul className="space-y-2 text-sm text-gray-200">
                <li><button onClick={onStart} className="hover:text-cyan-400 transition-colors">Get Started</button></li>
                <li><button onClick={onLearn} className="hover:text-cyan-400 transition-colors">Learn</button></li>
                <li><a href="#algorithms" className="hover:text-cyan-400 transition-colors">Algorithms</a></li>
              </ul>
            </div>

            {/* Resources */}
            <div>
              <h4 className="font-semibold text-white mb-4">Resources</h4>
              <ul className="space-y-2 text-sm text-gray-200">
                <li><a href="#" className="hover:text-cyan-400 transition-colors">Documentation</a></li>
                <li><a href="#" className="hover:text-cyan-400 transition-colors">Examples</a></li>
                <li><a href="#" className="hover:text-cyan-400 transition-colors">GitHub</a></li>
              </ul>
            </div>

            {/* Social */}
            <div>
              <h4 className="font-semibold text-white mb-4">Connect</h4>
              <div className="flex gap-3">
                <button className="w-10 h-10 rounded-full bg-slate-800/70 hover:bg-slate-700/80 flex items-center justify-center text-gray-100 hover:text-cyan-300 transition-all transform hover:scale-110">
                  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M23 3a10.9 10.9 0 01-3.14 1.53 4.48 4.48 0 00-7.86 3v1A10.66 10.66 0 013 4s-4 9 5 13a11.64 11.64 0 01-7 2s9 5 20 5a9.5 9.5 0 00-9-5.5c4.75 2.25 7-7 7-7z" />
                  </svg>
                </button>
                <button className="w-10 h-10 rounded-full bg-slate-800/70 hover:bg-slate-700/80 flex items-center justify-center text-gray-100 hover:text-cyan-300 transition-all transform hover:scale-110">
                  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v 3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" />
                  </svg>
                </button>
              </div>
            </div>
          </div>

          {/* Divider */}
          <div className="border-t border-slate-800 pt-8">
            <p className="text-center text-sm text-gray-300">
              © 2025 OptimizeHub. Built with passion for optimization enthusiasts.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
