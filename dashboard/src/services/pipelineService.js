import { createApi } from './api';

const api = createApi('/api/logparser');

export const pipelineService = {
    getAll: async (params = {}) => {
        // Fetches logs/runs from LogParser
        const response = await api.get('/logs', { params });
        return response.data;
    },

    getById: async (id) => {
        const response = await api.get(`/logs/${id}`);
        return response.data;
    }
};
