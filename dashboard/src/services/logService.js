import { createApi } from './api';

// Use the proxy path defined in vite.config.js which points to localhost:8001
const BASE_URL = '/api/logparser';
const api = createApi(BASE_URL);

export const logService = {
    /**
     * Fetch logs with optional filters
     * @param {Object} params - { skip, limit, provider, repo_name }
     */
    getLogs: async (params = {}) => {
        try {
            const response = await api.get('/logs', { params });
            return response.data;
        } catch (error) {
            console.warn("Failed to fetch logs, falling back to mock data", error);
            // Fallback mock data from guide
            return [
                {
                    "_id": "mock_1",
                    "run_id": "SIM_GITHUB_MOCK_001",
                    "repo_name": "emsi/devsecops-pipeline",
                    "provider": "GITHUB",
                    "log_data": "Mock log data...",
                    "timestamp_received": new Date().toISOString()
                },
                {
                    "_id": "mock_2",
                    "run_id": "SIM_GITLAB_MOCK_002",
                    "repo_name": "emsi/backend-service",
                    "provider": "GITLAB",
                    "log_data": "Mock log data...",
                    "timestamp_received": new Date(Date.now() - 3600000).toISOString()
                }
            ];
        }
    },

    /**
     * Get log by ID
     * @param {string} id 
     */
    getLogById: async (id) => {
        try {
            const response = await api.get(`/logs/${id}`);
            return response.data;
        } catch (error) {
            console.error("Failed to fetch log details", error);
            throw error;
        }
    }
};
