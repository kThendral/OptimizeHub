// Minimal API client for OptimizeHub frontend
const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export async function fetchAlgorithms() {
  try {
    console.log('Fetching algorithms from:', `${API_BASE}/api/algorithms`);
    const res = await fetch(`${API_BASE}/api/algorithms`);
    console.log('Response status:', res.status, res.statusText);
    
    if (!res.ok) {
      throw new Error(`Failed to fetch algorithms: ${res.status}`);
    }
    const data = await res.json();
    console.log('Algorithms data:', data);
    // Return full algorithm objects with status information
    return data.algorithms;
  } catch (error) {
    console.error('Fetch algorithms error:', error);
    throw error;
  }
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

export default {
  fetchAlgorithms,
  fetchAlgorithmDetails,
  executeAlgorithm
};
