// Location: frontend/src/data/presets.js

/**
 * Pre-configured optimization scenarios for beginners.
 * Each preset includes algorithm selection, problem definition, and parameters.
 */

export const OPTIMIZATION_PRESETS = {
  'quick-2d': {
    id: 'quick-2d',
    name: '🎯 Quick 2D Test (Sphere)',
    description: 'Simple 2D optimization using PSO on sphere function. Great for testing!',
    difficulty: 'beginner',
    algorithm: 'particle_swarm',
    problemData: {
      fitnessFunction: 'sphere',
      dimensions: 2,
      lowerBound: -5,
      upperBound: 5,
      objective: 'minimize'
    },
    psoParams: {
      swarmSize: 30,
      maxIterations: 50,
      w: 0.7,
      c1: 1.5,
      c2: 1.5
    },
    expectedTime: '< 1 second',
    expectedFitness: '< 0.01',
    explanation: {
      problem: 'The Sphere function is the simplest optimization benchmark. In 2D, it\'s like a smooth bowl shape with a single minimum at the origin (0,0). There are no local minima to trap the algorithm.',
      expectedResults: 'PSO should quickly converge to the global minimum near (0,0) with a fitness value close to 0. The swarm of particles will start scattered across the search space and gradually collapse toward the center.',
      why: 'This preset uses a small swarm (30 particles) and only 50 iterations because the problem is simple. The balanced inertia weight (w=0.7) and cognitive/social coefficients (c1=c2=1.5) provide good exploration without overshooting.'
    }
  },

  'multimodal-rastrigin': {
    id: 'multimodal-rastrigin',
    name: '⚡ Multi-Modal Challenge (Rastrigin)',
    description: 'Genetic Algorithm on Rastrigin - a function with many local minima',
    difficulty: 'intermediate',
    algorithm: 'genetic_algorithm',
    problemData: {
      fitnessFunction: 'rastrigin',
      dimensions: 3,
      lowerBound: -5.12,
      upperBound: 5.12,
      objective: 'minimize'
    },
    gaParams: {
      populationSize: 60,
      maxIterations: 80,
      crossoverRate: 0.85,
      mutationRate: 0.15,
      tournamentSize: 4
    },
    expectedTime: '1-2 seconds',
    expectedFitness: '< 10',
    explanation: {
      problem: 'The Rastrigin function is highly multi-modal, meaning it has many local minima (valleys) that look like the global minimum. It\'s like a wavy surface with countless small dips. This makes it easy for algorithms to get "stuck" in suboptimal solutions.',
      expectedResults: 'GA should find a solution relatively close to the global minimum (0,0,0), with fitness under 10. You might see the fitness decrease rapidly at first, then slow down as the population explores different valleys.',
      why: 'Genetic Algorithms excel at this because crossover creates diverse offspring that can "jump" between valleys, while mutation prevents premature convergence. Higher crossover rate (0.85) ensures good mixing, while moderate mutation (0.15) provides escape from local minima.'
    }
  },

  'rosenbrock-valley': {
    id: 'rosenbrock-valley',
    name: '🏔️ Narrow Valley (Rosenbrock)',
    description: 'PSO navigating the narrow Rosenbrock valley - tests convergence',
    difficulty: 'intermediate',
    algorithm: 'particle_swarm',
    problemData: {
      fitnessFunction: 'rosenbrock',
      dimensions: 2,
      lowerBound: -5,
      upperBound: 10,
      objective: 'minimize'
    },
    psoParams: {
      swarmSize: 40,
      maxIterations: 100,
      w: 0.6,
      c1: 2.0,
      c2: 2.0
    },
    expectedTime: '1-2 seconds',
    expectedFitness: '< 1',
    explanation: {
      problem: 'The Rosenbrock function features a narrow, curved valley. While the global minimum is easy to find in theory (at point [1,1]), the valley is extremely narrow and curved like a banana. Algorithms must carefully navigate along this valley.',
      expectedResults: 'PSO will initially find the valley quickly but will take time to converge along it to the minimum at (1,1). You\'ll see fitness drop rapidly at first, then slowly improve as particles slide down the narrow valley.',
      why: 'We use higher cognitive and social coefficients (c1=c2=2.0) to help particles communicate and follow the best path along the valley. Lower inertia (w=0.6) prevents overshooting the narrow channel. More iterations (100) give time for fine-tuning.'
    }
  },

  'high-dimensional': {
    id: 'high-dimensional',
    name: '🌌 High Dimensional (10D Sphere)',
    description: 'GA on 10-dimensional sphere function - tests scalability',
    difficulty: 'advanced',
    algorithm: 'genetic_algorithm',
    problemData: {
      fitnessFunction: 'sphere',
      dimensions: 10,
      lowerBound: -10,
      upperBound: 10,
      objective: 'minimize'
    },
    gaParams: {
      populationSize: 100,
      maxIterations: 100,
      crossoverRate: 0.8,
      mutationRate: 0.1,
      tournamentSize: 5
    },
    expectedTime: '2-3 seconds',
    expectedFitness: '< 0.1',
    explanation: {
      problem: 'This is the same simple Sphere function, but in 10 dimensions instead of 2. While still unimodal (one minimum), the search space is exponentially larger: 20^10 possible combinations! This tests whether algorithms scale well with dimensionality.',
      expectedResults: 'GA should find solutions near the 10-dimensional origin with low fitness (< 0.1). The algorithm may take longer to converge due to the vast search space, and you might observe step-wise fitness improvements as better individuals are discovered.',
      why: 'High-dimensional problems require larger populations (100) to maintain diversity and explore the space effectively. We use more iterations (100) and a larger tournament size (5) for stronger selection pressure, while keeping mutation low (0.1) to avoid disrupting good solutions.'
    }
  },

  'ackley-exploration': {
    id: 'ackley-exploration',
    name: '🔍 Exploration Test (Ackley)',
    description: 'PSO on Ackley function - nearly flat outer region with central peak',
    difficulty: 'intermediate',
    algorithm: 'particle_swarm',
    problemData: {
      fitnessFunction: 'ackley',
      dimensions: 2,
      lowerBound: -5,
      upperBound: 5,
      objective: 'minimize'
    },
    psoParams: {
      swarmSize: 50,
      maxIterations: 75,
      w: 0.8,
      c1: 1.8,
      c2: 1.8
    },
    expectedTime: '1-2 seconds',
    expectedFitness: '< 0.5',
    explanation: {
      problem: 'The Ackley function has an almost flat outer region with many small ripples, and a sharp central peak. From far away, particles see little gradient (nearly flat), making it hard to determine which direction improves fitness. Only near the center does the landscape become clear.',
      expectedResults: 'PSO needs strong exploration to escape the flat outer region. You\'ll see fitness remain relatively high initially as particles wander, then rapidly decrease once they find the central basin. Final fitness should be under 0.5.',
      why: 'Higher inertia (w=0.8) helps particles explore the flat region more aggressively before converging. A larger swarm (50 particles) increases the chance that at least some particles will discover the promising central area early.'
    }
  },

  'griewank-hybrid': {
    id: 'griewank-hybrid',
    name: '🧬 Hybrid Challenge (Griewank)',
    description: 'GA on Griewank - combines sum and product components',
    difficulty: 'advanced',
    algorithm: 'genetic_algorithm',
    problemData: {
      fitnessFunction: 'griewank',
      dimensions: 5,
      lowerBound: -600,
      upperBound: 600,
      objective: 'minimize'
    },
    gaParams: {
      populationSize: 80,
      maxIterations: 100,
      crossoverRate: 0.9,
      mutationRate: 0.12,
      tournamentSize: 4
    },
    expectedTime: '2-3 seconds',
    expectedFitness: '< 0.5',
    explanation: {
      problem: 'Griewank combines two components: a sum (like Sphere) and a product (creates local minima). At large distances, it behaves like a simple parabola, but near the origin, many local minima appear. The extremely wide bounds (±600) create a huge search space.',
      expectedResults: 'GA should navigate the wide initial landscape and locate the central basin, then carefully explore the local minima to find the global minimum. Expect fitness to decrease in stages as the population zones in on better regions.',
      why: 'Very high crossover (0.9) creates many candidate solutions to explore the vast space. Moderate mutation (0.12) provides diversity needed to escape local minima. The large population (80) and many iterations (100) are essential given the problem complexity and scale.'
    }
  }
};

/**
 * Get presets filtered by difficulty level
 */
export function getPresetsByDifficulty(difficulty) {
  return Object.values(OPTIMIZATION_PRESETS).filter(
    preset => preset.difficulty === difficulty
  );
}

/**
 * Get preset by ID
 */
export function getPresetById(id) {
  return OPTIMIZATION_PRESETS[id];
}

/**
 * Get all preset IDs
 */
export function getAllPresetIds() {
  return Object.keys(OPTIMIZATION_PRESETS);
}

/**
 * Get difficulty badge color
 */
export function getDifficultyColor(difficulty) {
  const colors = {
    beginner: 'bg-green-100 text-green-800 border-green-300',
    intermediate: 'bg-yellow-100 text-yellow-800 border-yellow-300',
    advanced: 'bg-red-100 text-red-800 border-red-300'
  };
  return colors[difficulty] || colors.beginner;
}
