
const express = require('express');
const router = express.Router();
const prisma = require('../config/db');
const auth = require('../middleware/auth');

// Generic log saving function
const saveLog = async (req, res, provider) => {
  const {
    log_data,
    repo_name,
    author,
    pipeline_name,
    run_id,
    timestamp_original,
  } = req.body;

  if (!log_data || !repo_name || !author || !pipeline_name || !run_id) {
    return res.status(400).json({ errors: [{ msg: 'Missing required fields' }] });
  }

  try {
    // Basic sanitization
    const sanitized_log_data =
      typeof log_data === 'string' ? log_data.replace(/<[^>]*>/g, '') : log_data;

    const log = await prisma.log.create({
      data: {
        log_data: sanitized_log_data,
        repo_name,
        author,
        pipeline_name,
        run_id,
        timestamp_original,
        provider,
      },
    });

    res.status(201).json({
      status: 'success',
      message: `Log from ${provider} saved successfully`,
      log_id: log.id,
    });
  } catch (err) {
    console.error(err.message);
    res.status(500).send('Server Error');
  }
};

// @route   POST /logs/github
// @desc    Receives and stores a log entry from GitHub Actions
// @access  Public
router.post('/github', (req, res) => saveLog(req, res, 'GITHUB'));

// @route   POST /logs/gitlab
// @desc    Receives and stores a log entry from GitLab CI
// @access  Public
router.post('/gitlab', (req, res) => saveLog(req, res, 'GITLAB'));

// @route   POST /logs/jenkins
// @desc    Receives and stores a log entry from Jenkins
// @access  Public
router.post('/jenkins', (req, res) => saveLog(req, res, 'JENKINS'));

// @route   POST /logs/upload
// @desc    Receives and stores a log entry from a generic API call
// @access  Public
router.post('/upload', (req, res) => {
    const { provider } = req.body;
    if(!provider) {
        return res.status(400).json({ errors: [{ msg: 'Missing provider field' }] });
    }

    // Normalize provider to match enum values
    const normalizedProvider = normalizeProvider(provider);
    if (!normalizedProvider) {
        return res.status(400).json({
            errors: [{
                msg: 'Invalid provider. Accepted values: GITHUB, GITLAB, JENKINS, API (or variations like "GitHub Actions", "GitLab CI", etc.)'
            }]
        });
    }

    saveLog(req, res, normalizedProvider);
});

// Helper function to normalize provider names
const normalizeProvider = (provider) => {
    const providerStr = String(provider).toUpperCase().replace(/[^A-Z]/g, '');

    // Map common variations to enum values
    const providerMap = {
        'GITHUB': 'GITHUB',
        'GITHUBACTIONS': 'GITHUB',
        'GH': 'GITHUB',
        'GITLAB': 'GITLAB',
        'GITLABCI': 'GITLAB',
        'GITLABCICD': 'GITLAB',
        'GL': 'GITLAB',
        'JENKINS': 'JENKINS',
        'API': 'API'
    };

    return providerMap[providerStr] || null;
};


// @route   GET /logs/github/pull
// @desc    Pull logs from GitHub Actions
// @access  Private (requires valid token)
router.get('/github/pull', auth, async (req, res) => {
  // This is a conceptual endpoint. A real implementation would require more specific details
  // about which repo, run, etc., to fetch. This could be passed as query params.
  const { owner, repo, run_id } = req.query;

  if (!owner || !repo || !run_id) {
    return res.status(400).json({ msg: 'Missing owner, repo, or run_id query parameters' });
  }

  try {
    // Use a library like 'axios' or 'node-fetch' to call the GitHub API
    // const fetch = require('node-fetch'); // Make sure to install this dependency
    // const url = `https://api.github.com/repos/${owner}/${repo}/actions/runs/${run_id}/logs`;
    // const githubToken = process.env.GITHUB_TOKEN;

    // const response = await fetch(url, {
    //   headers: {
    //     Authorization: `token ${githubToken}`,
    //     'Accept': 'application/vnd.github.v3+json',
    //   },
    // });

    // if (!response.ok) {
    //   return res.status(response.status).json({ msg: 'Failed to fetch logs from GitHub' });
    // }

    // const logData = await response.text();

    // You would then process and save the logData as in the /upload endpoint.

    res.json({
      status: 'info',
      message: 'Conceptual endpoint for GitHub Actions log retrieval.',
      details: 'A full implementation would fetch logs from the GitHub API using a token and save them.',
      required_params: ['owner', 'repo', 'run_id'],
    });

  } catch (err) {
    console.error(err.message);
    res.status(500).send('Server Error');
  }
});

module.exports = router;
