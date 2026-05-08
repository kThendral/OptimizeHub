//Frontend API client for persistence features
import axios from 'axios';

// Same base as index.js — VITE_API_URL is the backend root, no /api suffix
const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Token is stored in localStorage by AuthModal after login/signup
const getAuthToken = () => localStorage.getItem('token');

// Create axios instance with auth header
const createAuthClient = () => {
  const token = getAuthToken();
  return axios.create({
    baseURL: `${API_BASE}/api`,
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  });
};

export const persistenceAPI = {
  // ==== RUNS ====
  async saveRun(runData) {
    const client = createAuthClient();
    return client.post('/persistence/runs/save', runData);
  },

  async getRunHistory(limit = 50, offset = 0) {
    const client = createAuthClient();
    return client.get(`/persistence/runs/history?limit=${limit}&offset=${offset}`);
  },

  async getPublicRuns(algorithm = null) {
    return axios.get(`${API_BASE}/api/persistence/runs/public`, {
      params: { algorithm, limit: 50 }
    });
  },

  async shareRun(runId, sharedBy) {
    const client = createAuthClient();
    return client.post(`/persistence/runs/${runId}/share`, { shared_by: sharedBy });
  },

  // ==== CONFIGURATIONS ====
  async saveConfiguration(configData) {
    const client = createAuthClient();
    return client.post('/persistence/configs/save', configData);
  },

  async getMyConfigurations(limit = 50) {
    const client = createAuthClient();
    return client.get(`/persistence/configs/my?limit=${limit}`);
  },

  async getPublicConfigurations(algorithm = null, tags = null) {
    return axios.get(`${API_BASE}/api/persistence/configs/public`, {
      params: { algorithm, tags: tags?.join(','), limit: 50 }
    });
  },

  async deleteConfiguration(configId) {
    const client = createAuthClient();
    return client.delete(`/persistence/configs/${configId}`);
  },

  // ==== STATS ====
  async getUserStats() {
    const client = createAuthClient();
    return client.get('/persistence/stats');
  }
};