const axios = require('axios');
const fs = require('fs');
const path = require('path');

async function verify() {
    const PORT = process.env.PORT || 3344;
    const logParserUrl = process.env.LOGPARSER_URL || 'http://localhost:8001';

    console.log(`Testing LogCollector at http://localhost:${PORT}`);
    console.log(`Expecting LogParser at ${logParserUrl}`);

    try {
        const logPath = path.join(__dirname, '../test-log-github.json');
        const logData = JSON.parse(fs.readFileSync(logPath, 'utf8'));

        // 1. Send Log to Simulator (which inserts to DB)
        console.log('1. Sending log to LogCollector Simulator...');
        const response = await axios.post(`http://localhost:${PORT}/api/logs/simulate`, logData);

        if (response.data.success) {
            console.log(`✅ LogCollector accepted the log (RunID: ${response.data.run_id})`);

            // The simulator already calls LogParser, so we are checking the RESULT of that internal call
            // returned in the response fields: logParserStatus, logParserError

            if (response.data.logParserStatus === 'success') {
                console.log(`✅ VERIFIED: LogParser received the data.`);
                process.exit(0);
            } else {
                console.error(`❌ LogParser connection FAILED.`);
                console.error(`Error: ${response.data.logParserError}`);
                console.error(`Status: ${response.data.logParserStatus}`);
                console.log("\nPossible Causes:");
                console.log("1. LogParser is not running on port 8001");
                console.log("2. LogParser is looking at a different Database or Collection (check .env)");
                console.log("3. The endpoint /api/parse/db is incorrect");
                process.exit(1);
            }
        } else {
            console.error('❌ LogCollector rejected the log.');
            process.exit(1);
        }
    } catch (error) {
        if (error.code === 'ECONNREFUSED') {
            console.error(`❌ Connection failed. Is LogCollector running on port ${PORT}?`);
            console.error('Run "npm start" in the logcollector directory first.');
        } else {
            console.error('❌ Error:', error.message);
        }
        process.exit(1);
    }
}

verify();
