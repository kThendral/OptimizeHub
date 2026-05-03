//Frontend API client for persistence features
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

// Helper to get token from Supabase session
const getAuthToken = async () => {
  const { data: { session } } = await supabaseClient.auth.getSession();
  return session?.access_token || null;
};

// Create axios instance with auth header
const createAuthClient = async () => {
  const token = await getAuthToken();
  return axios.create({
    baseURL: API_URL,
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  });
};

export const persistenceAPI = {
  // ==== RUNS ====
  async saveRun(runData) {
    const client = await createAuthClient();
    return client.post('/persistence/runs/save', runData);
  },

  async getRunHistory(limit = 50, offset = 0) {
    const client = await createAuthClient();
    return client.get(`/persistence/runs/history?limit=${limit}&offset=${offset}`);
  },

  async getPublicRuns(algorithm = null) {
    return axios.get(`${API_URL}/persistence/runs/public`, {
      params: { algorithm, limit: 50 }
    });
  },

  async shareRun(runId, sharedBy) {
    const client = await createAuthClient();
    return client.post(`/persistence/runs/${runId}/share`, { shared_by: sharedBy });
  },

  // ==== CONFIGURATIONS ====
  async saveConfiguration(configData) {
    const client = await createAuthClient();
    return client.post('/persistence/configs/save', configData);
  },

  async getMyConfigurations(limit = 50) {
    const client = await createAuthClient();
    return client.get(`/persistence/configs/my?limit=${limit}`);
  },

  async getPublicConfigurations(algorithm = null, tags = null) {
    return axios.get(`${API_URL}/persistence/configs/public`, {
      params: { algorithm, tags: tags?.join(','), limit: 50 }
    });
  },

  async deleteConfiguration(configId) {
    const client = await createAuthClient();
    return client.delete(`/persistence/configs/${configId}`);
  },

  // ==== STATS ====
  async getUserStats() {
    const client = await createAuthClient();
    return client.get('/persistence/stats');
  }
};