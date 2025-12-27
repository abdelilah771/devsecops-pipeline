import { createApi } from './api';

// Use the proxy path defined in vite.config.js
const BASE_URL = '/api/reports';
const api = createApi(BASE_URL);

export const reportService = {
    /**
     * Trigger report generation task
     * @param {Object} reportData - { run_id, project_name, report_type, format, ... }
     * @returns {Promise<Object>} { task_id, status }
     */
    generate: async (reportData) => {
        try {
            const response = await api.post('/generate', reportData);
            return response.data;
        } catch (error) {
            console.error("Report generation trigger failed", error);
            throw error;
        }
    },

    /**
     * Check status of a generation task
     * @param {string} taskId 
     * @returns {Promise<Object>} { status, result: { report_id } }
     */
    getStatus: async (taskId) => {
        try {
            const response = await api.get(`/status/${taskId}`);
            return response.data;
        } catch (error) {
            console.error("Report status check failed", error);
            throw error;
        }
    },

    /**
     * Get the download URL (actually we might just construct it, but let's follow the API)
     * @param {string} reportId 
     * @returns {Promise<Object>} { file_url }
     */
    getDownloadUrl: async (reportId) => {
        try {
            const response = await api.get(`/download/${reportId}`);
            return response.data;
        } catch (error) {
            console.error("Report download url fetch failed", error);
            throw error;
        }
    }
};
