import axios from 'axios';

// Map of services and their proxy paths or direct URLs
const SERVICES = [
    { id: 'logcollector', name: 'LogCollector', url: 'http://localhost:3344/health' }, // Direct if CORS allowed, otherwise need proxy
    { id: 'logparser', name: 'LogParser', url: '/api/logparser/health' },
    { id: 'vulndetector', name: 'VulnDetector', url: '/api/vuln/health' },
    { id: 'fixsuggester', name: 'FixSuggester', url: '/api/fixes/health' },
    { id: 'reportgenerator', name: 'ReportGenerator', url: '/api/reports/health' },
];

export const statusService = {
    /**
     * Check health of all services
     * @returns {Promise<Array>} Array of service status objects
     */
    checkAll: async () => {
        const checks = SERVICES.map(async (service) => {
            try {
                // simple timeout to avoid hanging
                await axios.get(service.url, { timeout: 2000 });
                return { ...service, status: 'online' };
            } catch (error) {
                return { ...service, status: 'offline', error: error.message };
            }
        });
        return Promise.all(checks);
    }
};
