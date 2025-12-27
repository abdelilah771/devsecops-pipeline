import axios from 'axios';

const API_BASE = '/api/fixes';

// Configure axios defaults
const apiClient = axios.create({
    baseURL: API_BASE,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const fixService = {
    /**
     * Get fix proposal for a specific vulnerability
     * @param {string} vulnId - The vulnerability ID
     * @returns {Promise<{id: number, vuln_id: string, fix: string, explanation: string, created_at: string}>}
     */
    getFix: async (vulnId) => {
        try {
            const response = await apiClient.get(`/${vulnId}`);
            return response.data;
        } catch (error) {
            console.error('Failed to fetch fix:', error);
            throw error;
        }
    }
};
