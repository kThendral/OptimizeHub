// Minimal API client for OptimizeHub frontend
const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export async function fetchAlgorithms() {
  const MAX_ATTEMPTS = 3;
  const TIMEOUT_MS = 60000; // 60s — enough for Render cold start

  for (let attempt = 1; attempt <= MAX_ATTEMPTS; attempt++) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), TIMEOUT_MS);

    try {
      console.log(`Fetching algorithms (attempt ${attempt}/${MAX_ATTEMPTS}):`, `${API_BASE}/api/algorithms`);
      const res = await fetch(`${API_BASE}/api/algorithms`, { signal: controller.signal });
      clearTimeout(timeoutId);
      console.log('Response status:', res.status, res.statusText);

      if (!res.ok) throw new Error(`Failed to fetch algorithms: ${res.status}`);

      const data = await res.json();
      console.log('Algorithms data:', data);
      return data.algorithms;
    } catch (error) {
      clearTimeout(timeoutId);
      const isRetryable =
        error.name === 'AbortError' ||
        error.message.includes('Failed to fetch') ||
        error.message.includes('timeout');

      if (isRetryable && attempt < MAX_ATTEMPTS) {
        console.warn(`Backend not responding, retrying in 5s... (${attempt}/${MAX_ATTEMPTS})`);
        await new Promise(r => setTimeout(r, 5000));
        continue;
      }

      console.warn('Backend not available. Algorithms will load when backend is running.');
      return [];
    }
  }
  return [];
}

export async function fetchAlgorithmDetails(name) {
  const res = await fetch(`${API_BASE}/api/algorithms/${encodeURIComponent(name)}`);
  if (!res.ok) {
    throw new Error(`Failed to fetch algorithm details: ${res.status}`);
  }
  return res.json();
}

/**
 * Execute an algorithm on the backend.
 * Expected payload shape:
 * {
 *   algorithm: 'particle_swarm' | 'genetic_algorithm' | ...,
 *   problem: { dimensions, bounds, objective, fitness_function_name },
 *   params: { ... }
 * }
 */
export async function executeAlgorithm(payload) {
  const res = await fetch(`${API_BASE}/api/optimize`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  const data = await res.json();
  if (!res.ok) {
    // The backend returns 400/422 with JSON detail; forward it as error
    const msg = data.detail || data.error || JSON.stringify(data);
    throw new Error(msg);
  }
  return data;
}

/**
 * Submit async optimization job to Celery queue.
 * @param {Object} problem - Problem definition with dimensions, bounds, objective, fitness_function_name
 * @param {Array<string>} algorithms - Array of algorithm names (e.g., ["particle_swarm", "genetic_algorithm"])
 * @param {Object} params - Optional algorithm-specific parameters
 * @returns {Promise<{group_id: string, task_ids: Array<string>}>}
 */
export async function submitAsyncOptimization(problem, algorithms, params = null) {
  const payload = {
    problem,
    algorithms
  };

  // Add params if provided
  if (params) {
    payload.params = params;
  }

  const res = await fetch(`${API_BASE}/async/optimize`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });

  if (!res.ok) {
    const data = await res.json();
    const msg = data.detail || data.error || JSON.stringify(data);
    throw new Error(msg);
  }

  return res.json(); // Returns: { group_id, task_ids }
}

/**
 * Poll task status from Celery.
 * @param {string} taskId - Task ID returned from submitAsyncOptimization
 * @returns {Promise<{task_id: string, state: string, result?: any, error?: any}>}
 */
export async function getTaskStatus(taskId) {
  const res = await fetch(`${API_BASE}/async/tasks/${taskId}`);

  if (!res.ok) {
    throw new Error(`Failed to fetch task status: ${res.status}`);
  }

  return res.json(); // Returns: { task_id, state: "PENDING|STARTED|SUCCESS|FAILURE", result?, error? }
}

export default {
  fetchAlgorithms,
  fetchAlgorithmDetails,
  executeAlgorithm,
  submitAsyncOptimization,
  getTaskStatus
};
