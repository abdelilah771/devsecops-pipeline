import { logService } from './src/services/logService.js';
import axios from 'axios';

// Mock axios since we are running in node
import { jest } from '@jest/globals'; // Only if we had jest, but we don't.
// Let's just use raw axios for testing the endpoint directly
const API_URL = 'http://localhost:8001';

async function verifyLogs() {
    try {
        console.log("Testing GET /logs...");
        const response = await axios.get(`${API_URL}/logs?limit=5`);

        if (response.status === 200) {
            console.log("✅ Success! Logs fetched:", response.data.length);
            if (response.data.length > 0) {
                const log = response.data[0];
                console.log("Sample Log:", {
                    id: log._id || log.id,
                    provider: log.provider,
                    repo: log.repo_name
                });
            }
        } else {
            console.error("❌ Failed. Status:", response.status);
        }

    } catch (error) {
        console.error("❌ API Error:", error.message);
        if (error.response) {
            console.error("Response data:", error.response.data);
        }
    }
}

verifyLogs();
