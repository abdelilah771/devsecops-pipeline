
const axios = require('axios');

const LOGPARSER_URL = 'http://localhost:8001';

async function verify() {
    console.log('Starting Verification for LogParser Integration...');

    // 1. Health Check
    try {
        console.log(`\n[1/2] Checking Health at ${LOGPARSER_URL}/health ...`);
        const healthRes = await axios.get(`${LOGPARSER_URL}/health`);
        console.log('✅ Health Check Passed:', healthRes.data);
    } catch (error) {
        console.error('❌ Health Check Failed:', error.message);
        if (error.code === 'ECONNREFUSED') {
            console.error('   -> Service seems to be DOWN. Please start LogParser on port 8001.');
        }
        process.exit(1);
    }

    // 2. Manual Parse
    try {
        console.log(`\n[2/2] Testing Manual Parse at ${LOGPARSER_URL}/api/parse ...`);
        const sampleYaml = "name: Test\njobs:\n  build:\n    runs-on: ubuntu-latest\n    steps:\n      - run: echo hello";

        const parseRes = await axios.post(`${LOGPARSER_URL}/api/parse`, {
            yaml: sampleYaml
        });

        if (parseRes.data && parseRes.data.parsed) {
            console.log('✅ Manual Parse Passed. Structure detected.');
        } else {
            console.log('⚠️ Manual Parse returned unexpected response:', parseRes.data);
        }
    } catch (error) {
        console.error('❌ Manual Parse Failed:', error.message);
        if (error.response) {
            console.error('   -> Status:', error.response.status);
            console.error('   -> Data:', error.response.data);
        }
    }

    console.log('\nVerification Complete.');
}

verify();
