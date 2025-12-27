const express = require('express');
const router = express.Router();
const prisma = require('../config/db');
const axios = require('axios');

// @route   POST /api/logs/simulate
// @desc    Receive simulation logs, adapt them to internal format, store and trigger LogParser
// @access  Public
router.post('/', async (req, res) => {
    try {
        const payload = req.body;

        // Default values for simulation
        let provider = 'GITHUB';
        let repo_name = 'simulation/repo';
        let pipeline_name = 'simulation-pipeline';
        let log_data = '';

        // Adapt payload if it matches the simulation format
        if (payload.workflow) {
            // It's likely a simulation JSON
            if (payload.repository) repo_name = payload.repository;
            if (payload.workflow.name) pipeline_name = payload.workflow.name;

            // Serialize the workflow object to string to serve as "log"
            // Because LogParser expects a string (yaml/json) to parse steps
            log_data = JSON.stringify(payload.workflow, null, 2);
        } else if (payload.log) {
            // It's already in the internal format
            if (payload.provider) provider = payload.provider.toUpperCase();
            if (payload.repo_name) repo_name = payload.repo_name;
            if (payload.pipeline_name) pipeline_name = payload.pipeline_name;
            log_data = payload.log;
        } else {
            // Fallback, treat whole body as log
            log_data = JSON.stringify(payload, null, 2);
        }

        // Generate run_id
        const run_id = `SIM_${provider}_${Date.now()}`;

        console.log(`[SIMULATION] Received log for ${repo_name} - RunID: ${run_id}`);

        // Insert into MongoDB
        await prisma.log.create({
            data: {
                run_id: run_id,
                provider: provider,
                repo_name: repo_name,
                pipeline_name: pipeline_name,
                log_data: log_data,
                author: 'simulator',
                timestamp_received: new Date()
            }
        });

        let logParserStatus = 'skipped';
        let logParserError = null;

        // Call LogParser
        const logParserUrl = process.env.LOGPARSER_URL || process.env.LOG_PARSER_URL || 'http://logparser:8000';

        // Note: LogParser endpoint is typically /parse?run_id=...
        // We fire and forget (or wait a bit), matching webhook logic.
        try {
            // Wait 2 seconds to ensure DB availability
            await new Promise(resolve => setTimeout(resolve, 2000));

            console.log(`[SIMULATION] Triggering LogParser at ${logParserUrl}/api/parse/db`);
            await axios.post(`${logParserUrl}/api/parse/db`, {
                run_id: run_id,
                provider: provider
            }, {
                timeout: 5000
            });
            console.log("[SIMULATION] LogParser triggered successfully");
            logParserStatus = 'success';
        } catch (error) {
            const errorMsg = error.message;
            const errorDetail = error.response && error.response.data ? JSON.stringify(error.response.data) : 'No Data';
            console.warn(`[SIMULATION] LogParser trigger failed: ${errorMsg} - Detail: ${errorDetail}`);

            logParserStatus = 'failed';
            // Include detail in the error message for visibility
            logParserError = `${errorMsg} | Detail: ${errorDetail}`;
        }

        res.status(201).json({
            success: true,
            run_id: run_id,
            logParserStatus: logParserStatus,
            logParserError: logParserError,
            message: 'Simulation log received and processing started'
        });

    } catch (err) {
        console.error("Simulation Endpoint Error:", err);
        res.status(500).json({ error: 'Server Error during simulation processing' });
    }
});

module.exports = router;
