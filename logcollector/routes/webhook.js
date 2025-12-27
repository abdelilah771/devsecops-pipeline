const express = require('express');
const router = express.Router();
const prisma = require('../config/db');
const axios = require('axios');
// const { v4: uuidv4 } = require('uuid'); // Can use this or Date.now() as per user request

// @route   POST /webhook
// @desc    Receive fake webhook from CI/CD, store in DB, call LogParser
// @access  Public
router.post('/', async (req, res) => {
    try {
        const { provider, repo_name, pipeline_name, log } = req.body;

        // 1. Validation basics
        if (!log || !provider || !repo_name || !pipeline_name) {
            return res.status(400).json({ error: 'Missing required fields: log, provider, repo_name, pipeline_name' });
        }

        const normalizedProvider = provider.toUpperCase();
        const validProviders = ['GITHUB', 'GITLAB', 'JENKINS'];

        if (!validProviders.includes(normalizedProvider)) {
            return res.status(400).json({ error: 'Invalid provider. Only GITHUB, GITLAB, JENKINS are accepted.' });
        }

        // 2. Generate run_id
        // Format: provider_timestamp
        const run_id = `${normalizedProvider}_${Date.now()}`;

        // 3. Insert into MongoDB 'Log' collection
        await prisma.log.create({
            data: {
                run_id: run_id,
                provider: normalizedProvider,
                repo_name: repo_name,
                pipeline_name: pipeline_name,
                log_data: log,
                author: 'webhook-ci', // Placeholder
                timestamp_received: new Date()
            }
        });

        // 4. Call LogParser
        const logParserUrl = process.env.LOGPARSER_URL || process.env.LOG_PARSER_URL || 'http://localhost:8001';

        try {
            console.log(`Calling LogParser at ${logParserUrl}/api/parse/db (RunID: ${run_id})`);
            await axios.post(`${logParserUrl}/api/parse/db`, {
                run_id: run_id,
                provider: normalizedProvider
            }, {
                timeout: 5000
            });
            console.log("LogParser called successfully");
        } catch (error) {
            console.warn("LogParser trigger failed but storing succeeded:", error.message);
            // Checklist: "Si LogParser down: log warning mais webhook retourne 200 (or 201) quand même"
        }

        // 5. Return JSON response
        res.status(201).json({
            success: true,
            run_id: run_id
        });

    } catch (err) {
        console.error("Webhook Error:", err);
        res.status(500).json({ error: 'Server Error' });
    }
});

module.exports = router;
