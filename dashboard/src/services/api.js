import axios from 'axios';

// Create axios instance with base URL pointing to Nginx API Gateway
// In development, Vite proxy or Nginx will handle /api calls.
// In production (docker), Nginx serves the app and proxies /api.
// Helper to create an API instance for a specific service URL
export const createApi = (baseURL) => {
    const api = axios.create({
        baseURL: baseURL,
        timeout: 30000,
        headers: {
            'Content-Type': 'application/json',
        },
    });

    api.interceptors.response.use(
        (response) => response,
        (error) => {
            console.error('API Error:', error.response || error.message);
            if (error.code === 'ECONNABORTED') {
                console.error('Request timeout');
            }
            return Promise.reject(error);
        }
    );

    return api;
};
