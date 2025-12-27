import axios from 'axios';

const API_BASE = '/api/vuln';

// Configure axios defaults
const apiClient = axios.create({
    baseURL: API_BASE,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const vulnService = {
    /**
     * Get aggregated statistics for dashboard charts
     * @returns {Promise<{total_vulnerabilities: number, by_severity: {LOW: number, MEDIUM: number, HIGH: number, CRITICAL: number}}>}
     */
    getStats: async () => {
        try {
            const response = await apiClient.get('/stats');
            return response.data;
        } catch (error) {
            console.error('Failed to fetch stats:', error);
            // Default fallback structure
            return {
                total_vulnerabilities: 0,
                by_severity: { LOW: 0, MEDIUM: 0, HIGH: 0, CRITICAL: 0 }
            };
        }
    },

    /**
     * Get list of detected vulnerabilities
     * @param {string} [runId] - Optional run ID to filter by
     * @param {number} [limit=100] - Max results
     * @returns {Promise<Array>}
     */
    getVulnerabilities: async (runId = null, limit = 100) => {
        try {
            const params = { limit };
            if (runId) params.run_id = runId;
            const response = await apiClient.get('/vulnerabilities', { params });
            return response.data;
        } catch (error) {
            console.error('Failed to fetch vulnerabilities:', error);
            return [];
        }
    },

    /**
     * Check service health
     * @returns {Promise<boolean>}
     */
    getHealth: async () => {
        try {
            await apiClient.get('/health');
            return true;
        } catch (error) {
            return false;
        }
    }
};
