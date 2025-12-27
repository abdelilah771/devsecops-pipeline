import axios from 'axios';

// Use the proxy path defined in vite.config.js for local dev, 
// or relative path for production (assuming nginx handles routing)
const BASE_URL = '/api/logparser';

const api = axios.create({
    baseURL: BASE_URL,
    timeout: 30000,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const logParserService = {
    /**
     * Check the health status of the LogParser service.
     * @returns {Promise<Object>} Health status object
     */
    checkHealth: async () => {
        try {
            const response = await api.get('/health');
            return response.data;
        } catch (error) {
            console.error("LogParser health check failed", error);
            // Return a fallback error structure if service is down
            return {
                status: 'unhealthy',
                detail: {
                    status: 'unhealthy',
                    mongodb: 'disconnected', /* assume worst case */
                    error: error.message
                }
            };
        }
    },

    /**
     * Trigger analysis for a specific run ID stored in the DB.
     * @param {string} runId - The GitHub Run ID
     * @param {string} provider - The provider (default: GITHUB)
     * @returns {Promise<Object>} Analysis result
     */
    analyzeRun: async (runId, provider = 'GITHUB') => {
        try {
            const response = await api.post('/api/parse/db', {
                run_id: runId,
                provider: provider
            });
            return response.data;
        } catch (error) {
            console.error("Analysis trigger failed", error);
            throw error;
        }
    },

    /**
     * Manually parse raw YAML log content.
     * @param {string} yamlContent - The raw YAML string
     * @returns {Promise<Object>} Parsed result
     */
    parseLog: async (yamlContent) => {
        try {
            const response = await api.post('/api/parse', {
                yaml: yamlContent
            });
            return response.data;
        } catch (error) {
            console.error("Manual parse failed", error);
            throw error;
        }
    }
};
