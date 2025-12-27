import { createApi } from './api';

const api = createApi(import.meta.env.VITE_LOGPARSER_URL);

export const dashboardService = {
    getStats: async () => {
        // Attempt to fetch from LogParser stats endpoint
        const providerStats = await api.get('/stats/providers');
        return {
            providerStats: providerStats.data
        };
    }
};
