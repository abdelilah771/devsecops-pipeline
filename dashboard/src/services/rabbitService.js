import { createApi } from './api';

// Proxy path configured in vite.config.js
const BASE_URL = '/api/rabbit';
// Basic Auth credentials for local RabbitMQ (guest/guest)
const AUTH = {
    username: 'guest',
    password: 'guest'
};

const api = createApi(BASE_URL);

export const rabbitService = {
    /**
     * Get Overview Stats (Message rates, Totals)
     */
    getOverview: async () => {
        try {
            const response = await api.get('/overview', { auth: AUTH });
            return response.data;
        } catch (error) {
            console.error("RabbitMQ Overview fetch failed", error);
            // Return mock data fallback if fails (or throw based on preference)
            throw error;
        }
    },

    /**
     * Get Queue Details
     */
    getQueues: async () => {
        try {
            const response = await api.get('/queues', { auth: AUTH });
            return response.data;
        } catch (error) {
            console.error("RabbitMQ Queues fetch failed", error);
            throw error;
        }
    }
};
