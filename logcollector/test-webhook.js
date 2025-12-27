const axios = require('axios');

const payload = {
    provider: "GITHUB",
    repo_name: "safeops/logminer",
    pipeline_name: "ci-build",
    log: "Job: build\nStep: Checkout\nuses: actions/checkout@latest\nAWS_ACCESS_KEY_ID=AKIA1234SECRET\n"
};

async function runTest() {
    try {
        console.log("Sending webhook to http://localhost:5000/webhook...");
        const response = await axios.post('http://localhost:5000/webhook', payload);
        console.log("Response:", response.data);
    } catch (error) {
        console.error("Error:", error.response ? error.response.data : error.message);
    }
}

runTest();
