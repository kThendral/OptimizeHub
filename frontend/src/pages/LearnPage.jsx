import React, { useState } from 'react';

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
        {activeSection === 'algorithms' && <AlgorithmLearningSection onStartOptimizing={onStartOptimizing} />}
        {activeSection === 'guide' && <GuideSection />}
      </main>
    </div>
  );
}

function AlgorithmLearningSection({ onStartOptimizing }) {
  const [activeTab, setActiveTab] = useState('pso');

  const algorithms = {
    pso: {
      name: 'Particle Swarm Optimization (PSO)',
      blurb:
        'PSO models flocking behavior from the mid-1990s and remains a core metaheuristic; surveys highlight how neighborhood topologies, inertia control, and hybrid variants balance exploration and convergence.',
      howItWorks: [
        'Start with a swarm of particles (candidate solutions) spread across the search space.',
        'Evaluate fitness; each particle tracks its personal best and the swarm tracks a global (or neighborhood) best.',
        'Update velocity with inertia plus cognitive (self-best) and social (swarm-best) pulls; topology choice controls information flow.',
        'Move particles, clamp velocities if needed, and re-evaluate; repeat until the swarm stabilizes or a budget is reached.'
      ],
      parameters: [
        { name: 'Swarm size', role: 'How many particles explore in parallel.', starter: '20-40 for demos', tip: '50-80 for harder, multi-modal spaces.' },
        { name: 'Inertia (w)', role: 'Momentum term controlling exploration vs. exploitation.', starter: '0.7-0.9', tip: 'Use decay toward 0.4 to tighten near the end.' },
        { name: 'Cognitive (c1)', role: 'Pull toward personal best.', starter: '1.2-1.6', tip: 'Balance with c2 to avoid oscillation.' },
        { name: 'Social (c2)', role: 'Pull toward global/neighborhood best.', starter: '1.2-1.6', tip: 'Higher c2 speeds convergence but risks premature clustering.' },
        { name: 'Velocity clamp', role: 'Caps step size to prevent runaway jumps.', starter: '10-30% of variable range', tip: 'Tighten if particles overshoot good regions.' }
      ],
      applications: [
        'Engineering design: truss sizing and power systems tuning where gradient info is scarce.',
        'Neural network and controller parameter search with modest dimensionality.',
        'Scheduling and route planning when quick, good-enough solutions are acceptable.'
      ],
      researchInsights: [
        'Recent reviews show ring or von Neumann topologies improve diversity early, then switching to global best accelerates convergence.',
        'Hybrid PSO-DE variants often outperform vanilla PSO on continuous benchmarks by injecting mutation-like jumps.',
        'Constriction or time-varying inertia factors are recommended to reduce stagnation in later iterations.'
      ],
      advantages: ['Few parameters and simple updates.', 'Good first-choice for smooth, moderately sized spaces.', 'Parallel-friendly and cheap per iteration.'],
      limitations: ['Can stagnate without diversity controls.', 'Performance drops in very high dimensions.', 'Constraint handling needs custom repairs or penalties.'],
      comparison: 'Balances exploration and speed; compared with GA it converges faster but may need diversity boosts; compared with DE it is smoother but sometimes less global.'
    },
    ga: {
      name: 'Genetic Algorithms (GA)',
      blurb:
        'GA evolves a population via selection, crossover, and mutation; broad surveys note strong versatility across discrete and mixed problems when diversity is preserved.',
      howItWorks: [
        'Initialize a population of candidate solutions encoded as vectors or chromosomes.',
        'Select parents via tournament or roulette based on fitness.',
        'Recombine parents (crossover) to mix building blocks; mutate to add fresh variation.',
        'Keep best elites; iterate selection-crossover-mutation until convergence or budget.'
      ],
      parameters: [
        { name: 'Population size', role: 'Number of candidates per generation.', starter: '30-60', tip: '80-120 for combinatorial problems.' },
        { name: 'Crossover rate', role: 'How often parents recombine.', starter: '0.7-0.9', tip: 'Lower if schema disruption hurts structure.' },
        { name: 'Mutation rate', role: 'Random tweaks to maintain diversity.', starter: '0.5-2% per gene', tip: '3-5% if population converges early.' },
        { name: 'Selection pressure', role: 'How strongly the best are favored.', starter: 'Tournament size 2-3', tip: 'Higher pressure speeds convergence but risks premature loss of diversity.' },
        { name: 'Elitism', role: 'Copies of top solutions kept each generation.', starter: '1-2 elites', tip: '3-5 if fitness is noisy to avoid losing good solutions.' }
      ],
      applications: [
        'Timetabling, vehicle routing, and layout problems where solutions are discrete.',
        'Feature selection in machine learning to trade accuracy vs. subset size.',
        'Hyperparameter search when parameter interactions matter.'
      ],
      researchInsights: [
        'Comparative studies show GA is competitive on combinatorial problems when crossover respects problem structure (e.g., order crossover for TSP).',
        'Diversity-preserving operators (crowding, fitness sharing) delay premature convergence in deceptive landscapes.',
        'Hybrid GA with local search (memetic GA) often wins on benchmarks with rugged fitness surfaces.'
      ],
      advantages: ['Flexible representation for discrete or mixed variables.', 'Good at escaping local minima through crossover.', 'Large operator library to fit problem structure.'],
      limitations: ['Can be slow to fine-tune continuous variables.', 'Schema disruption if crossover is not aligned to problem encoding.', 'Requires careful parameter tuning to avoid premature convergence.'],
      comparison: 'Versatile for combinatorial tasks; slower per iteration than PSO/DE but better at maintaining global diversity.'
    },
    de: {
      name: 'Differential Evolution (DE)',
      blurb:
        'DE perturbs candidates with scaled vector differences; surveys report strong performance on continuous, non-convex functions with few control parameters.',
      howItWorks: [
        'Maintain a population of real-valued vectors.',
        'For each target vector, create a mutant by adding a scaled difference between two or more other vectors.',
        'Mix mutant and target via crossover to form a trial vector.',
        'Selection keeps the better of trial vs. target; repeat across generations.'
      ],
      parameters: [
        { name: 'Population size', role: 'Number of candidate vectors.', starter: '5-10x problem dimension', tip: 'Use larger sizes for rugged landscapes.' },
        { name: 'Scale factor (F)', role: 'Magnitude of differential perturbation.', starter: '0.5-0.8', tip: 'Increase toward 0.9 for more exploration early.' },
        { name: 'Crossover rate (CR)', role: 'Portion of components inherited from mutant.', starter: '0.6-0.9', tip: 'Lower CR favors coordinate-wise search; higher mixes more aggressively.' },
        { name: 'Mutation strategy', role: 'Choice of base vector and differences (e.g., rand/1, best/2).', starter: 'rand/1', tip: 'best/1 accelerates but may reduce diversity; switch when close to optimum.' }
      ],
      applications: [
        'Continuous engineering design (aerodynamics, antenna arrays).',
        'Control tuning and parameter estimation with noisy objectives.',
        'Benchmark suites (Rosenbrock, Rastrigin) where DE often ranks highly in comparative studies.'
      ],
      researchInsights: [
        'Comparative experiments show DE excels on smooth but multi-modal functions and benefits from adaptive F and CR schedules.',
        'Hybrid DE with local search or PSO-like velocity terms improves late-stage convergence.',
        'Smaller populations with self-adaptive parameters reduce runtime without large accuracy loss.'
      ],
      advantages: ['Strong global search with minimal parameters.', 'Works well on continuous, non-separable problems.', 'Simple to implement and parallelize.'],
      limitations: ['Performance sensitive to F/CR choices.', 'May require many evaluations for high-dimensional tasks.', 'Constraint handling needs tailored repair or penalty schemes.'],
      comparison: 'Often outperforms GA on continuous tasks; more exploratory than PSO but can be slower to fine-tune unless parameters adapt.'
    },
    sa: {
      name: 'Simulated Annealing (SA)',
      blurb:
        'SA uses a temperature-controlled acceptance rule inspired by annealing; classic studies show it escapes local minima well on discrete problems when cooling is calibrated.',
      howItWorks: [
        'Start from one solution and a high temperature.',
        'Propose a neighbor by a small random change; compute fitness difference.',
        'Accept better moves always; accept worse moves with probability exp(-delta/T) to escape traps.',
        'Cool temperature over time (geometric or adaptive); stop when temperature or improvements stall.'
      ],
      parameters: [
        { name: 'Initial temperature', role: 'Sets early acceptance of uphill moves.', starter: 'Estimate so ~60-80% of uphill moves are accepted', tip: 'Higher if landscape is rugged.' },
        { name: 'Cooling rate', role: 'Speed of temperature decrease.', starter: '0.90-0.99 geometric', tip: 'Slower cooling for high-quality solutions; faster for quick heuristics.' },
        { name: 'Steps per temperature', role: 'Moves attempted at each temperature level.', starter: '10-50', tip: 'Increase when acceptance drops too quickly.' },
        { name: 'Restart/ reheating', role: 'Occasional temperature boosts to regain diversity.', starter: 'Optional off', tip: 'Enable if search freezes early.' }
      ],
      applications: [
        'Scheduling and timetabling where a single-solution heuristic is effective.',
        'VLSI layout and network design from early SA literature.',
        'Baseline solver for TSP-style neighborhoods with modest problem sizes.'
      ],
      researchInsights: [
        'Classical proofs show convergence to global optimum with slow cooling, but practical runs use faster schedules for efficiency.',
        'Comparisons find SA competitive on discrete problems with well-designed neighborhoods and reheating.',
        'Hybrid SA-local search (e.g., 2-opt with annealing) often improves early solution quality.'
      ],
      advantages: ['Easy to implement with few parameters.', 'Strong escape from local minima via probabilistic acceptance.', 'Great baseline for discrete neighborhoods.'],
      limitations: ['Can be slow if cooled too cautiously.', 'Performance hinges on neighbor design.', 'Single-solution search lacks population diversity.'],
      comparison: 'Slower but steadier than greedy heuristics; complements GA/PSO by providing local diversification.'
    },
    acor: {
      name: 'Ant Colony Optimization (ACOR)',
      blurb:
        'ACOR extends ant colony ideas to continuous or ordered spaces; research highlights pheromone-guided sampling and multi-objective path planning gains.',
      howItWorks: [
        'Maintain pheromone-like weights over solution components or continuous kernels.',
        'Sample new solutions biased by pheromone; add heuristic desirability if available.',
        'Evaluate solutions, then reinforce pheromone around better samples while evaporating older trails.',
        'Iterate sampling-update until pheromone converges or a time limit hits.'
      ],
      parameters: [
        { name: 'Ants per iteration', role: 'Number of samples/ants generated.', starter: '10-30', tip: 'Increase for rugged or large spaces.' },
        { name: 'Pheromone evaporation', role: 'Controls forgetting vs. exploitation.', starter: '0.4-0.6', tip: 'Lower values keep more history; higher encourages exploration.' },
        { name: 'Pheromone spread', role: 'Kernel width around elite solutions (σ).', starter: '5-20% of variable range', tip: 'Shrink over time to focus search.' },
        { name: 'Elite archive size', role: 'How many best solutions influence pheromone.', starter: '5-10', tip: 'Larger archives improve robustness for multi-modal tasks.' }
      ],
      applications: [
        'Robot and UAV path planning with dynamic obstacles using pheromone-guided navigation.',
        'Routing and logistics (TSP, VRP) where pheromone trails encode promising tours.',
        'Continuous design tasks via ACOR kernels for real-valued variables.'
      ],
      researchInsights: [
        'Studies report that adaptive evaporation stabilizes performance in changing environments.',
        'Hybrid ACO with local search (2-opt, gradient steps) markedly improves solution quality on routing benchmarks.',
        'Multi-objective ACO variants balance trail reinforcement across competing criteria.'
      ],
      advantages: ['Excels at constructive/path problems.', 'Implicit memory via pheromone helps in dynamic settings.', 'Naturally parallel across ants.'],
      limitations: ['Trail stagnation if evaporation is too low.', 'More parameters than PSO/DE.', 'Can be slower on high-dimensional continuous spaces.'],
      comparison: 'Great for path construction compared to GA/PSO; needs careful evaporation tuning to avoid early lock-in.'
    }
  };

  const comparisonRows = [
    { alg: 'PSO', strengths: 'Fast convergence, simple parameters', cautions: 'May stagnate; tune inertia/social terms', best: 'Smooth continuous spaces, medium dims' },
    { alg: 'GA', strengths: 'Flexible for discrete encodings', cautions: 'Risk of premature convergence', best: 'Combinatorial and mixed-variable tasks' },
    { alg: 'DE', strengths: 'Strong global search on continuous problems', cautions: 'Sensitive to F/CR; many evaluations', best: 'Non-convex continuous with moderate dims' },
    { alg: 'SA', strengths: 'Good local escape with minimal setup', cautions: 'Cooling choice critical; single-solution', best: 'Discrete neighborhoods, baseline heuristics' },
    { alg: 'ACOR', strengths: 'Great for paths/constructive solutions', cautions: 'Trail stagnation; more knobs', best: 'Routing, path planning, continuous-with-kernels' }
  ];

  const current = algorithms[activeTab];

  return (
    <div className="space-y-8">
      <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
          <h2 className="text-3xl font-bold bg-gradient-to-r from-purple-900 to-indigo-900 bg-clip-text text-transparent">Learning Lab</h2>
          <p className="text-gray-600">Research-grounded primers with beginner-friendly parameter tips.</p>
        </div>
        <button
          onClick={onStartOptimizing}
          className="self-start md:self-auto bg-gradient-to-r from-blue-500 via-purple-500 to-purple-600 text-white px-4 py-2 rounded-lg font-medium shadow hover:scale-105 transition-all"
        >
          Try these algorithms
        </button>
      </div>

      {/* Tabs */}
      <div className="overflow-x-auto">
        <div className="inline-flex min-w-full gap-2 bg-white/70 backdrop-blur-sm p-2 rounded-2xl shadow border border-purple-100">
          {Object.entries(algorithms).map(([key, alg]) => (
            <button
              key={key}
              onClick={() => setActiveTab(key)}
              className={`whitespace-nowrap px-4 py-2 rounded-xl text-sm font-semibold transition-all ${
                activeTab === key
                  ? 'bg-gradient-to-r from-purple-600 to-indigo-600 text-white shadow'
                  : 'text-purple-800 hover:bg-purple-50'
              }`}
            >
              {alg.name}
            </button>
          ))}
        </div>
      </div>

      {/* Active tab content */}
      <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-lg border border-purple-100 p-6 space-y-6">
        <div className="space-y-2">
          <div className="inline-flex items-center gap-2 rounded-full bg-purple-50 px-3 py-1 text-xs font-semibold text-purple-800">Research grounded</div>
          <h3 className="text-2xl font-bold text-purple-900">{current.name}</h3>
          <p className="text-gray-700 leading-relaxed">{current.blurb}</p>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          <div className="space-y-3">
            <h4 className="text-lg font-semibold text-purple-800">How it works</h4>
            <ul className="space-y-2 text-sm text-gray-700">
              {current.howItWorks.map((step, idx) => (
                <li key={idx} className="flex gap-2">
                  <span className="mt-1 inline-flex h-6 w-6 items-center justify-center rounded-full bg-purple-100 text-purple-700 text-xs font-bold">{idx + 1}</span>
                  <span>{step}</span>
                </li>
              ))}
            </ul>
          </div>
          <div className="space-y-3">
            <h4 className="text-lg font-semibold text-purple-800">Real-world uses</h4>
            <div className="space-y-2 text-sm text-gray-700">
              {current.applications.map((item, idx) => (
                <div key={idx} className="flex gap-2">
                  <span className="mt-1 h-2 w-2 rounded-full bg-green-500"></span>
                  <span>{item}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="grid md:grid-cols-3 gap-4">
          <div className="md:col-span-2">
            <h4 className="text-lg font-semibold text-purple-800 mb-2">Key parameters explained</h4>
            <div className="overflow-x-auto">
              <table className="min-w-full text-sm text-left text-gray-700">
                <thead className="bg-purple-50 text-purple-900">
                  <tr>
                    <th className="px-3 py-2">Parameter</th>
                    <th className="px-3 py-2">Why it matters</th>
                    <th className="px-3 py-2">Start here</th>
                    <th className="px-3 py-2">When to adjust</th>
                  </tr>
                </thead>
                <tbody>
                  {current.parameters.map((p) => (
                    <tr key={p.name} className="border-t border-purple-50">
                      <td className="px-3 py-2 font-semibold text-purple-900">{p.name}</td>
                      <td className="px-3 py-2">{p.role}</td>
                      <td className="px-3 py-2 text-gray-600">{p.starter}</td>
                      <td className="px-3 py-2 text-gray-600">{p.tip}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          <div className="bg-gradient-to-br from-purple-50 to-indigo-50 border border-purple-100 rounded-xl p-4 space-y-2">
            <h4 className="text-lg font-semibold text-purple-800">Research insights</h4>
            <ul className="space-y-2 text-sm text-gray-700">
              {current.researchInsights.map((item, idx) => (
                <li key={idx} className="flex gap-2">
                  <span className="mt-1 h-2 w-2 rounded-full bg-indigo-500"></span>
                  <span>{item}</span>
                </li>
              ))}
            </ul>
            <div className="text-xs text-purple-700 mt-2">Summaries based on surveys and comparative studies across metaheuristics.</div>
          </div>
        </div>

        <div className="grid md:grid-cols-3 gap-4">
          <div className="bg-white border border-gray-100 rounded-xl p-4 shadow-sm">
            <h4 className="font-semibold text-purple-800 mb-2">Visual aids (planned)</h4>
            <p className="text-sm text-gray-700">Placeholder for a chart showing how parameter tuning changes convergence speed.</p>
            <div className="mt-3 h-24 rounded-lg bg-gradient-to-r from-gray-100 to-gray-50 border border-dashed border-gray-300 flex items-center justify-center text-xs text-gray-500">Coming soon: interactive slider</div>
          </div>
          <div className="bg-white border border-gray-100 rounded-xl p-4 shadow-sm">
            <h4 className="font-semibold text-purple-800 mb-2">Strengths</h4>
            <ul className="space-y-2 text-sm text-gray-700">
              {current.advantages.map((item, idx) => (
                <li key={idx} className="flex gap-2">
                  <span className="mt-1 h-2 w-2 rounded-full bg-green-500"></span>
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          </div>
          <div className="bg-white border border-gray-100 rounded-xl p-4 shadow-sm">
            <h4 className="font-semibold text-purple-800 mb-2">Limitations</h4>
            <ul className="space-y-2 text-sm text-gray-700">
              {current.limitations.map((item, idx) => (
                <li key={idx} className="flex gap-2">
                  <span className="mt-1 h-2 w-2 rounded-full bg-red-500"></span>
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>

        <div className="bg-gradient-to-r from-blue-50 via-purple-50 to-indigo-50 border border-purple-100 rounded-xl p-4 text-sm text-gray-800">
          <div className="font-semibold text-purple-900 mb-1">Comparison snapshot</div>
          <p>{current.comparison}</p>
        </div>
      </div>

      <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow border border-purple-100 p-6 space-y-4">
        <div className="flex items-center justify-between flex-wrap gap-2">
          <h4 className="text-lg font-semibold text-purple-900">Algorithm comparison (high level)</h4>
          <span className="text-xs text-gray-500">Quick selection guide based on survey takeaways</span>
        </div>
        <div className="overflow-x-auto">
          <table className="min-w-full text-sm text-left text-gray-700">
            <thead className="bg-purple-50 text-purple-900">
              <tr>
                <th className="px-3 py-2">Algorithm</th>
                <th className="px-3 py-2">Strengths</th>
                <th className="px-3 py-2">Watch-outs</th>
                <th className="px-3 py-2">Best suited for</th>
              </tr>
            </thead>
            <tbody>
              {comparisonRows.map((row) => (
                <tr key={row.alg} className="border-t border-purple-50">
                  <td className="px-3 py-2 font-semibold text-purple-900">{row.alg}</td>
                  <td className="px-3 py-2">{row.strengths}</td>
                  <td className="px-3 py-2">{row.cautions}</td>
                  <td className="px-3 py-2">{row.best}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
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