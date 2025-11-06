import React, { useState } from 'react';

export default function AlgorithmInfoSection({ onStartOptimizing }) {
  const [expandedAlgorithm, setExpandedAlgorithm] = useState(null);

  const algorithms = [
    {
      id: 'genetic',
      name: 'Genetic Algorithm (GA)',
      icon: '🧬',
      color: 'from-green-500 to-emerald-600',
      description: 'Inspired by natural evolution and Darwin\'s theory of survival of the fittest',
      whatItIs: 'A search heuristic that mimics the process of natural selection where the fittest individuals are selected for reproduction to produce offspring for the next generation.',
      howItWorks: [
        'Creates an initial population of candidate solutions',
        'Evaluates fitness of each individual',
        'Selects parents based on fitness scores',
        'Applies crossover (recombination) to create offspring',
        'Applies mutation to introduce genetic diversity',
        'Replaces old population with new generation',
        'Repeats until convergence or maximum generations'
      ],
      idealUseCases: [
        'Combinatorial optimization problems',
        'Multi-objective optimization',
        'Neural network training',
        'Scheduling and timetabling',
        'Feature selection in machine learning'
      ],
      example: 'Finding the optimal route for a traveling salesman visiting 20 cities. GA evolves a population of route permutations, crossing successful routes and mutating to explore new possibilities.',
      parameters: [
        { name: 'Population Size', description: 'Number of individuals in each generation (30-100)' },
        { name: 'Crossover Rate', description: 'Probability of recombination between parents (0.7-0.9)' },
        { name: 'Mutation Rate', description: 'Probability of random changes (0.01-0.1)' },
        { name: 'Selection Method', description: 'Tournament, roulette wheel, or rank-based selection' },
        { name: 'Generations', description: 'Maximum number of evolution cycles (50-500)' }
      ],
      links: [
        { title: 'Introduction to Genetic Algorithms', url: 'https://towardsdatascience.com/introduction-to-genetic-algorithms-including-example-code-e396e98d8bf3' },
        { title: 'GA Tutorial', url: 'https://www.tutorialspoint.com/genetic_algorithms/index.htm' }
      ]
    },
    {
      id: 'particle_swarm',
      name: 'Particle Swarm Optimization (PSO)',
      icon: '🐦',
      color: 'from-blue-500 to-cyan-600',
      description: 'Inspired by the social behavior of bird flocking and fish schooling',
      whatItIs: 'A computational method that optimizes a problem by iteratively improving candidate solutions with regard to a given measure of quality, based on social behavior patterns.',
      howItWorks: [
        'Initialize a swarm of particles with random positions and velocities',
        'Evaluate fitness of each particle\'s position',
        'Update personal best position for each particle',
        'Update global best position across all particles',
        'Calculate new velocity based on personal and global bests',
        'Update particle positions using the new velocities',
        'Repeat until convergence or maximum iterations'
      ],
      idealUseCases: [
        'Continuous optimization problems',
        'Neural network training',
        'Function optimization',
        'Engineering design optimization',
        'Clustering and data mining'
      ],
      example: 'Optimizing the parameters of a neural network. Each particle represents a set of weights and biases, moving through the parameter space guided by successful configurations.',
      parameters: [
        { name: 'Swarm Size', description: 'Number of particles in the swarm (20-50)' },
        { name: 'Inertia Weight (w)', description: 'Controls exploration vs exploitation (0.4-0.9)' },
        { name: 'Cognitive Coefficient (c1)', description: 'Attraction to personal best (1.5-2.0)' },
        { name: 'Social Coefficient (c2)', description: 'Attraction to global best (1.5-2.0)' },
        { name: 'Max Velocity', description: 'Limits particle movement speed' }
      ],
      links: [
        { title: 'PSO Explained', url: 'https://nathanrooy.github.io/posts/2016-08-17/simple-particle-swarm-optimization-with-python/' },
        { title: 'PSO Tutorial', url: 'https://www.mathworks.com/help/gads/particle-swarm-optimization-algorithm.html' }
      ]
    },
    {
      id: 'simulated_annealing',
      name: 'Simulated Annealing (SA)',
      icon: '🔥',
      color: 'from-red-500 to-orange-600',
      description: 'Inspired by the annealing process in metallurgy for cooling and crystallization',
      whatItIs: 'A probabilistic technique that approximates the global optimum by allowing occasional moves to worse solutions to escape local optima, with decreasing probability over time.',
      howItWorks: [
        'Start with an initial solution and high temperature',
        'Generate a random neighboring solution',
        'Calculate the change in objective function',
        'Accept better solutions automatically',
        'Accept worse solutions with probability based on temperature',
        'Decrease temperature according to cooling schedule',
        'Repeat until temperature reaches minimum or convergence'
      ],
      idealUseCases: [
        'Traveling Salesman Problem',
        'Job scheduling optimization',
        'Circuit design and VLSI layout',
        'Image processing and computer vision',
        'Protein folding prediction'
      ],
      example: 'Solving a 100-city TSP. SA starts with a random tour and iteratively swaps cities, accepting improvements and occasionally accepting worse tours when temperature is high.',
      parameters: [
        { name: 'Initial Temperature', description: 'Starting temperature for the process (high value)' },
        { name: 'Cooling Rate', description: 'Rate of temperature decrease (0.85-0.99)' },
        { name: 'Final Temperature', description: 'Stopping criterion temperature (near zero)' },
        { name: 'Iterations per Temperature', description: 'Number of attempts at each temperature' },
        { name: 'Neighborhood Function', description: 'Method for generating new solutions' }
      ],
      links: [
        { title: 'SA Algorithm Guide', url: 'https://www.geeksforgeeks.org/simulated-annealing/' },
        { title: 'Understanding SA', url: 'https://machinelearningmastery.com/simulated-annealing-optimization-with-python/' }
      ]
    },
    {
      id: 'differential_evolution',
      name: 'Differential Evolution (DE)',
      icon: '🧮',
      color: 'from-purple-500 to-indigo-600',
      description: 'A method that optimizes by maintaining a population and creating new candidates by combining existing ones',
      whatItIs: 'An evolutionary algorithm that uses differences between randomly selected population members to create new candidate solutions, particularly effective for real-valued optimization.',
      howItWorks: [
        'Initialize population with random solutions',
        'For each target individual, select three random individuals',
        'Create mutant vector by adding weighted difference',
        'Perform crossover between target and mutant vectors',
        'Evaluate fitness of trial vector',
        'Select better solution between target and trial',
        'Repeat until convergence criteria met'
      ],
      idealUseCases: [
        'Global optimization of real-valued functions',
        'Parameter estimation in engineering',
        'Machine learning hyperparameter tuning',
        'Economic optimization models',
        'Signal processing applications'
      ],
      example: 'Optimizing the design of a suspension system. DE evolves spring constants and damping coefficients by combining successful parameter sets from the population.',
      parameters: [
        { name: 'Population Size', description: 'Number of individuals (5-10 × problem dimension)' },
        { name: 'Mutation Factor (F)', description: 'Scaling factor for difference vectors (0.5-1.0)' },
        { name: 'Crossover Rate (CR)', description: 'Probability of parameter inheritance (0.1-0.9)' },
        { name: 'Strategy', description: 'DE variant (rand/1/bin, best/1/bin, etc.)' },
        { name: 'Generations', description: 'Maximum number of iterations' }
      ],
      links: [
        { title: 'DE Tutorial', url: 'https://pablormier.github.io/2017/09/05/a-tutorial-on-differential-evolution-with-python/' },
        { title: 'DE Explained', url: 'https://www.mathworks.com/help/gads/how-the-genetic-algorithm-works.html' }
      ]
    },
    {
      id: 'ant_colony',
      name: 'Ant Colony Optimization (ACO)',
      icon: '🐜',
      color: 'from-amber-500 to-yellow-600',
      description: 'Inspired by the foraging behavior of ants and their ability to find shortest paths',
      whatItIs: 'A probabilistic technique for solving computational problems which can be reduced to finding good paths through graphs, based on the behavior of ants seeking paths between their colony and food.',
      howItWorks: [
        'Initialize pheromone trails on graph edges',
        'Deploy artificial ants to construct solutions',
        'Ants choose paths probabilistically based on pheromones and heuristics',
        'Update pheromone trails based on solution quality',
        'Evaporate pheromones to prevent premature convergence',
        'Reinforce trails of better solutions',
        'Repeat until optimal solution emerges'
      ],
      idealUseCases: [
        'Traveling Salesman Problem',
        'Vehicle routing problems',
        'Network routing optimization',
        'Scheduling problems',
        'Graph coloring and partitioning'
      ],
      example: 'Optimizing delivery routes for a logistics company. Virtual ants explore different route combinations, leaving stronger pheromone trails on efficient paths that other ants are more likely to follow.',
      parameters: [
        { name: 'Number of Ants', description: 'Size of ant colony (10-50)' },
        { name: 'Pheromone Evaporation', description: 'Rate of pheromone decay (0.1-0.3)' },
        { name: 'Alpha (α)', description: 'Influence of pheromone trails (1-2)' },
        { name: 'Beta (β)', description: 'Influence of heuristic information (2-5)' },
        { name: 'Pheromone Deposit', description: 'Amount of pheromone deposited by ants' }
      ],
      links: [
        { title: 'ACO Introduction', url: 'https://www.researchgate.net/publication/220704910_Ant_Colony_Optimization' },
        { title: 'ACO Algorithm', url: 'https://www.geeksforgeeks.org/ant-colony-optimization-aco/' }
      ]
    }
  ];

  const toggleExpansion = (algorithmId) => {
    setExpandedAlgorithm(expandedAlgorithm === algorithmId ? null : algorithmId);
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="text-center space-y-4">
        <h2 className="text-4xl font-bold bg-gradient-to-r from-purple-900 via-purple-800 to-indigo-900 bg-clip-text text-transparent">
          Evolutionary Algorithms
        </h2>
        <p className="text-xl text-gray-600 max-w-4xl mx-auto">
          Discover the power of nature-inspired optimization algorithms that solve complex problems by mimicking biological processes
        </p>
      </div>

      {/* What are Evolutionary Algorithms */}
      <div className="bg-gradient-to-r from-blue-100 via-purple-100 to-indigo-100 rounded-2xl p-8">
        <h3 className="text-2xl font-bold text-purple-900 mb-4 text-center">🌟 What are Evolutionary Algorithms?</h3>
        <div className="grid md:grid-cols-3 gap-6">
          <div className="text-center">
            <div className="w-16 h-16 bg-gradient-to-br from-green-500 to-blue-600 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
              </svg>
            </div>
            <h4 className="font-bold text-purple-900 mb-2">Nature-Inspired</h4>
            <p className="text-gray-600 text-sm">
              These algorithms mimic natural processes like evolution, flocking, and foraging to solve optimization problems
            </p>
          </div>
          <div className="text-center">
            <div className="w-16 h-16 bg-gradient-to-br from-purple-500 to-pink-600 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
            <h4 className="font-bold text-purple-900 mb-2">Population-Based</h4>
            <p className="text-gray-600 text-sm">
              Work with multiple candidate solutions simultaneously, improving them through iterative processes
            </p>
          </div>
          <div className="text-center">
            <div className="w-16 h-16 bg-gradient-to-br from-orange-500 to-red-600 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <h4 className="font-bold text-purple-900 mb-2">Powerful & Versatile</h4>
            <p className="text-gray-600 text-sm">
              Handle complex, non-linear problems where traditional methods fail, finding near-optimal solutions
            </p>
          </div>
        </div>
      </div>

      {/* Why Use Them */}
      <div className="bg-white/70 backdrop-blur-sm rounded-2xl p-8 border border-gray-200">
        <h3 className="text-2xl font-bold text-purple-900 mb-6 text-center">🎯 Why Choose Evolutionary Algorithms?</h3>
        <div className="grid md:grid-cols-2 gap-8">
          <div className="space-y-4">
            <div className="flex items-start gap-3">
              <div className="w-8 h-8 rounded-full bg-green-100 flex items-center justify-center flex-shrink-0">
                <svg className="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <div>
                <h4 className="font-bold text-gray-800">No Gradient Required</h4>
                <p className="text-gray-600 text-sm">Work with black-box functions and discontinuous search spaces</p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center flex-shrink-0">
                <svg className="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <div>
                <h4 className="font-bold text-gray-800">Global Optimization</h4>
                <p className="text-gray-600 text-sm">Avoid local optima and find globally optimal or near-optimal solutions</p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <div className="w-8 h-8 rounded-full bg-purple-100 flex items-center justify-center flex-shrink-0">
                <svg className="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4" />
                </svg>
              </div>
              <div>
                <h4 className="font-bold text-gray-800">Highly Flexible</h4>
                <p className="text-gray-600 text-sm">Adaptable to various problem types and constraint systems</p>
              </div>
            </div>
          </div>
          <div className="space-y-4">
            <div className="flex items-start gap-3">
              <div className="w-8 h-8 rounded-full bg-orange-100 flex items-center justify-center flex-shrink-0">
                <svg className="w-5 h-5 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
              </div>
              <div>
                <h4 className="font-bold text-gray-800">Parallel Processing</h4>
                <p className="text-gray-600 text-sm">Naturally parallelizable for faster computation on multiple cores</p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <div className="w-8 h-8 rounded-full bg-red-100 flex items-center justify-center flex-shrink-0">
                <svg className="w-5 h-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div>
                <h4 className="font-bold text-gray-800">Robust & Reliable</h4>
                <p className="text-gray-600 text-sm">Less sensitive to noise and can handle imperfect fitness evaluations</p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <div className="w-8 h-8 rounded-full bg-pink-100 flex items-center justify-center flex-shrink-0">
                <svg className="w-5 h-5 text-pink-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                </svg>
              </div>
              <div>
                <h4 className="font-bold text-gray-800">Multi-Objective</h4>
                <p className="text-gray-600 text-sm">Can optimize multiple conflicting objectives simultaneously</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Algorithm Cards */}
      <div className="space-y-6">
        <h3 className="text-3xl font-bold text-center text-purple-900">🔬 Explore Our 5 Algorithms</h3>
        
        {algorithms.map((algorithm) => (
          <div key={algorithm.id} className="bg-white/70 backdrop-blur-sm rounded-2xl shadow-lg border border-gray-200 overflow-hidden">
            {/* Header */}
            <div 
              className={`bg-gradient-to-r ${algorithm.color} p-6 cursor-pointer transition-all duration-300 hover:shadow-lg`}
              onClick={() => toggleExpansion(algorithm.id)}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <span className="text-4xl">{algorithm.icon}</span>
                  <div>
                    <h4 className="text-2xl font-bold text-white">{algorithm.name}</h4>
                    <p className="text-white/90">{algorithm.description}</p>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      onStartOptimizing();
                    }}
                    className="bg-white/20 hover:bg-white/30 text-white font-medium py-2 px-4 rounded-lg transition-all duration-300 backdrop-blur-sm"
                  >
                    Try {algorithm.id}
                  </button>
                  <svg 
                    className={`w-6 h-6 text-white transition-transform duration-300 ${
                      expandedAlgorithm === algorithm.id ? 'rotate-180' : ''
                    }`} 
                    fill="none" 
                    stroke="currentColor" 
                    viewBox="0 0 24 24"
                  >
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                  </svg>
                </div>
              </div>
            </div>

            {/* Expanded Content */}
            {expandedAlgorithm === algorithm.id && (
              <div className="p-6 space-y-6">
                {/* What It Is */}
                <div>
                  <h5 className="text-lg font-bold text-purple-900 mb-3 flex items-center gap-2">
                    <span className="w-6 h-6 bg-purple-100 rounded-full flex items-center justify-center">
                      <span className="text-purple-600 text-sm">?</span>
                    </span>
                    What It Is
                  </h5>
                  <p className="text-gray-700 leading-relaxed">{algorithm.whatItIs}</p>
                </div>

                {/* How It Works */}
                <div>
                  <h5 className="text-lg font-bold text-purple-900 mb-3 flex items-center gap-2">
                    <span className="w-6 h-6 bg-blue-100 rounded-full flex items-center justify-center">
                      <svg className="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                      </svg>
                    </span>
                    How It Works
                  </h5>
                  <ol className="space-y-2">
                    {algorithm.howItWorks.map((step, index) => (
                      <li key={index} className="flex items-start gap-3 text-gray-700">
                        <span className="w-6 h-6 bg-gradient-to-br from-blue-500 to-purple-600 text-white rounded-full flex items-center justify-center text-sm font-bold flex-shrink-0 mt-0.5">
                          {index + 1}
                        </span>
                        <span>{step}</span>
                      </li>
                    ))}
                  </ol>
                </div>

                {/* Grid Layout for Remaining Sections */}
                <div className="grid lg:grid-cols-2 gap-6">
                  {/* Ideal Use Cases */}
                  <div>
                    <h5 className="text-lg font-bold text-purple-900 mb-3 flex items-center gap-2">
                      <span className="w-6 h-6 bg-green-100 rounded-full flex items-center justify-center">
                        <svg className="w-4 h-4 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                      </span>
                      Ideal Use Cases
                    </h5>
                    <ul className="space-y-2">
                      {algorithm.idealUseCases.map((useCase, index) => (
                        <li key={index} className="flex items-start gap-2 text-gray-700">
                          <span className="w-2 h-2 bg-green-500 rounded-full mt-2 flex-shrink-0"></span>
                          <span>{useCase}</span>
                        </li>
                      ))}
                    </ul>
                  </div>

                  {/* Parameters */}
                  <div>
                    <h5 className="text-lg font-bold text-purple-900 mb-3 flex items-center gap-2">
                      <span className="w-6 h-6 bg-orange-100 rounded-full flex items-center justify-center">
                        <svg className="w-4 h-4 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4" />
                        </svg>
                      </span>
                      Key Parameters
                    </h5>
                    <div className="space-y-3">
                      {algorithm.parameters.map((param, index) => (
                        <div key={index} className="bg-gray-50 rounded-lg p-3">
                          <h6 className="font-medium text-gray-800">{param.name}</h6>
                          <p className="text-sm text-gray-600">{param.description}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>

                {/* Example */}
                <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl p-6">
                  <h5 className="text-lg font-bold text-purple-900 mb-3 flex items-center gap-2">
                    <span className="w-6 h-6 bg-yellow-100 rounded-full flex items-center justify-center">
                      <svg className="w-4 h-4 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                      </svg>
                    </span>
                    Real-World Example
                  </h5>
                  <p className="text-gray-700 leading-relaxed">{algorithm.example}</p>
                </div>

                {/* Links & Try Button */}
                <div className="flex flex-wrap items-center justify-between gap-4 pt-4 border-t border-gray-200">
                  <div className="space-x-4">
                    {algorithm.links.map((link, index) => (
                      <a
                        key={index}
                        href={link.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-blue-600 hover:text-blue-800 font-medium text-sm transition-colors"
                      >
                        📖 {link.title}
                      </a>
                    ))}
                  </div>
                  <button
                    onClick={onStartOptimizing}
                    className={`bg-gradient-to-r ${algorithm.color} hover:shadow-lg text-white font-medium py-2 px-6 rounded-lg transition-all duration-300 hover:scale-105`}
                  >
                    🚀 Try {algorithm.name} Now
                  </button>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Call to Action */}
      <div className="bg-gradient-to-r from-purple-600 via-blue-600 to-indigo-600 rounded-2xl p-8 text-center text-white">
        <h3 className="text-2xl font-bold mb-4">Ready to Solve Your Optimization Problem?</h3>
        <p className="text-lg text-white/90 mb-6 max-w-2xl mx-auto">
          Choose from our collection of powerful algorithms or upload your custom fitness function to get started.
        </p>
        <button
          onClick={onStartOptimizing}
          className="bg-white text-purple-600 hover:bg-gray-100 font-bold py-3 px-8 rounded-xl transition-all duration-300 hover:scale-105 shadow-lg"
        >
          🎯 Start Optimizing Now
        </button>
      </div>
    </div>
  );
}