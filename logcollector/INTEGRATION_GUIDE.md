# CI/CD Integration Guide with ngrok

This guide shows how to send logs from GitHub Actions, GitLab CI, and Jenkins to your local server using ngrok.

## Prerequisites

1. Your server is running on port 5000
2. ngrok is installed and running: `ngrok http 5000`
3. You have your ngrok public URL (e.g., `https://abc123.ngrok.io`)

---

## Option 1: GitHub Actions

### Method A: Using Workflow Dispatch (Manual Trigger)

Create a file `.github/workflows/send-logs.yml` in your repository:

```yaml
name: Send Logs to SafeOps LogMiner

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  workflow_dispatch:

jobs:
  send-logs:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run tests or build
        id: build
        run: |
          # Your build/test commands here
          npm install
          npm test
          npm run build
        continue-on-error: true

      - name: Capture and send logs
        if: always()
        run: |
          # Prepare log data
          LOG_OUTPUT=$(cat <<EOF
          {
            "log_data": {
              "workflow": "${{ github.workflow }}",
              "job": "${{ github.job }}",
              "status": "${{ job.status }}",
              "event": "${{ github.event_name }}",
              "commit": "${{ github.sha }}",
              "logs": "Build completed with status: ${{ job.status }}"
            },
            "repo_name": "${{ github.repository }}",
            "author": "${{ github.actor }}",
            "pipeline_name": "${{ github.workflow }}",
            "run_id": "${{ github.run_id }}",
            "timestamp_original": "${{ github.event.head_commit.timestamp }}"
          }
          EOF
          )

          # Send to your ngrok URL
          curl -X POST https://YOUR_NGROK_URL.ngrok.io/logs/github \
            -H "Content-Type: application/json" \
            -d "$LOG_OUTPUT"
```

### Method B: Download and Send Full Logs

```yaml
name: Download and Send Full Logs

on:
  workflow_run:
    workflows: ["*"]
    types: [completed]

jobs:
  send-logs:
    runs-on: ubuntu-latest
    permissions:
      actions: read

    steps:
      - name: Download logs
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');

            // Get workflow run logs
            const logs = await github.rest.actions.downloadWorkflowRunLogs({
              owner: context.repo.owner,
              repo: context.repo.repo,
              run_id: context.payload.workflow_run.id,
            });

            // Save logs
            fs.writeFileSync('logs.zip', Buffer.from(logs.data));

      - name: Extract and send logs
        run: |
          unzip logs.zip
          LOG_CONTENT=$(cat */*)

          curl -X POST https://YOUR_NGROK_URL.ngrok.io/logs/github \
            -H "Content-Type: application/json" \
            -d "{
              \"log_data\": $(echo "$LOG_CONTENT" | jq -Rs .),
              \"repo_name\": \"${{ github.repository }}\",
              \"author\": \"${{ github.actor }}\",
              \"pipeline_name\": \"${{ github.workflow }}\",
              \"run_id\": \"${{ github.run_id }}\",
              \"timestamp_original\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"
            }"
```

**Replace `YOUR_NGROK_URL` with your actual ngrok URL (without https://)**

---

## Option 2: GitLab CI

Create or update `.gitlab-ci.yml` in your repository:

```yaml
stages:
  - build
  - test
  - send-logs

variables:
  LOG_ENDPOINT: "https://YOUR_NGROK_URL.ngrok.io/logs/gitlab"

build:
  stage: build
  script:
    - echo "Building application..."
    - npm install
    - npm run build
  artifacts:
    paths:
      - build/
    expire_in: 1 hour

test:
  stage: test
  script:
    - echo "Running tests..."
    - npm test
  allow_failure: true

send-logs:
  stage: send-logs
  when: always
  script:
    - |
      # Collect job information
      LOG_DATA=$(cat <<EOF
      {
        "log_data": {
          "pipeline_id": "${CI_PIPELINE_ID}",
          "job_name": "${CI_JOB_NAME}",
          "job_status": "${CI_JOB_STATUS}",
          "commit_sha": "${CI_COMMIT_SHA}",
          "commit_message": "${CI_COMMIT_MESSAGE}",
          "branch": "${CI_COMMIT_BRANCH}",
          "runner": "${CI_RUNNER_DESCRIPTION}"
        },
        "repo_name": "${CI_PROJECT_PATH}",
        "author": "${GITLAB_USER_LOGIN}",
        "pipeline_name": "${CI_PIPELINE_SOURCE}",
        "run_id": "${CI_PIPELINE_ID}",
        "timestamp_original": "${CI_PIPELINE_CREATED_AT}"
      }
      EOF
      )

      # Send to your endpoint
      curl -X POST ${LOG_ENDPOINT} \
        -H "Content-Type: application/json" \
        -d "$LOG_DATA"
```

### Alternative: Send Logs After Each Job

Add this to each job:

```yaml
build:
  stage: build
  script:
    - npm install
    - npm run build
  after_script:
    - |
      curl -X POST https://YOUR_NGROK_URL.ngrok.io/logs/gitlab \
        -H "Content-Type: application/json" \
        -d "{
          \"log_data\": {\"job\": \"${CI_JOB_NAME}\", \"status\": \"${CI_JOB_STATUS}\"},
          \"repo_name\": \"${CI_PROJECT_PATH}\",
          \"author\": \"${GITLAB_USER_LOGIN}\",
          \"pipeline_name\": \"Build\",
          \"run_id\": \"${CI_PIPELINE_ID}\",
          \"timestamp_original\": \"${CI_PIPELINE_CREATED_AT}\"
        }"
```

---

## Option 3: Jenkins

### Method A: Pipeline Script (Jenkinsfile)

Create a `Jenkinsfile` in your repository:

```groovy
pipeline {
    agent any

    environment {
        LOG_ENDPOINT = 'https://YOUR_NGROK_URL.ngrok.io/logs/jenkins'
    }

    stages {
        stage('Build') {
            steps {
                echo 'Building...'
                sh 'npm install'
                sh 'npm run build'
            }
        }

        stage('Test') {
            steps {
                echo 'Testing...'
                sh 'npm test'
            }
        }
    }

    post {
        always {
            script {
                def logData = """
                {
                    "log_data": {
                        "build_number": "${env.BUILD_NUMBER}",
                        "job_name": "${env.JOB_NAME}",
                        "build_status": "${currentBuild.result}",
                        "build_url": "${env.BUILD_URL}",
                        "duration": "${currentBuild.durationString}",
                        "console_log": "Build completed"
                    },
                    "repo_name": "${env.JOB_NAME}",
                    "author": "${env.BUILD_USER:-system}",
                    "pipeline_name": "${env.JOB_NAME}",
                    "run_id": "${env.BUILD_ID}",
                    "timestamp_original": "${new Date().format('yyyy-MM-dd\'T\'HH:mm:ss\'Z\'')}"
                }
                """

                sh """
                    curl -X POST ${LOG_ENDPOINT} \
                        -H 'Content-Type: application/json' \
                        -d '${logData}'
                """
            }
        }
    }
}
```

### Method B: Freestyle Project with Post-build Action

1. Go to your Jenkins job configuration
2. Scroll to "Post-build Actions"
3. Add "Execute shell" (Linux) or "Execute Windows batch command" (Windows)
4. Add this script:

**For Linux/Mac:**
```bash
#!/bin/bash

LOG_ENDPOINT="https://YOUR_NGROK_URL.ngrok.io/logs/jenkins"

curl -X POST $LOG_ENDPOINT \
  -H "Content-Type: application/json" \
  -d "{
    \"log_data\": {
      \"build_number\": \"$BUILD_NUMBER\",
      \"job_name\": \"$JOB_NAME\",
      \"build_status\": \"SUCCESS\",
      \"build_url\": \"$BUILD_URL\"
    },
    \"repo_name\": \"$JOB_NAME\",
    \"author\": \"jenkins\",
    \"pipeline_name\": \"$JOB_NAME\",
    \"run_id\": \"$BUILD_ID\",
    \"timestamp_original\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"
  }"
```

**For Windows:**
```batch
@echo off
set LOG_ENDPOINT=https://YOUR_NGROK_URL.ngrok.io/logs/jenkins

curl -X POST %LOG_ENDPOINT% ^
  -H "Content-Type: application/json" ^
  -d "{\"log_data\": {\"build_number\": \"%BUILD_NUMBER%\", \"job_name\": \"%JOB_NAME%\"}, \"repo_name\": \"%JOB_NAME%\", \"author\": \"jenkins\", \"pipeline_name\": \"%JOB_NAME%\", \"run_id\": \"%BUILD_ID%\", \"timestamp_original\": \"%date%\"}"
```

### Method C: Using HTTP Request Plugin

1. Install "HTTP Request Plugin" in Jenkins
2. In your pipeline, add:

```groovy
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Building...'
            }
        }
    }

    post {
        always {
            httpRequest(
                httpMode: 'POST',
                url: 'https://YOUR_NGROK_URL.ngrok.io/logs/jenkins',
                contentType: 'APPLICATION_JSON',
                requestBody: """
                {
                    "log_data": {"build": "${env.BUILD_NUMBER}", "status": "${currentBuild.result}"},
                    "repo_name": "${env.JOB_NAME}",
                    "author": "jenkins",
                    "pipeline_name": "${env.JOB_NAME}",
                    "run_id": "${env.BUILD_ID}",
                    "timestamp_original": "${new Date().format('yyyy-MM-dd\'T\'HH:mm:ss\'Z\'')}"
                }
                """
            )
        }
    }
}
```

---

## Testing Your Setup

### Test with curl:

**GitHub endpoint:**
```bash
curl -X POST https://YOUR_NGROK_URL.ngrok.io/logs/github \
  -H "Content-Type: application/json" \
  -d '{
    "log_data": {"test": "data", "message": "Test from GitHub"},
    "repo_name": "test/repo",
    "author": "testuser",
    "pipeline_name": "test-pipeline",
    "run_id": "12345",
    "timestamp_original": "2025-10-23T10:00:00Z"
  }'
```

**GitLab endpoint:**
```bash
curl -X POST https://YOUR_NGROK_URL.ngrok.io/logs/gitlab \
  -H "Content-Type: application/json" \
  -d '{
    "log_data": {"test": "data", "message": "Test from GitLab"},
    "repo_name": "test/repo",
    "author": "testuser",
    "pipeline_name": "test-pipeline",
    "run_id": "12345",
    "timestamp_original": "2025-10-23T10:00:00Z"
  }'
```

**Jenkins endpoint:**
```bash
curl -X POST https://YOUR_NGROK_URL.ngrok.io/logs/jenkins \
  -H "Content-Type: application/json" \
  -d '{
    "log_data": {"test": "data", "message": "Test from Jenkins"},
    "repo_name": "test-job",
    "author": "jenkins",
    "pipeline_name": "test-pipeline",
    "run_id": "12345",
    "timestamp_original": "2025-10-23T10:00:00Z"
  }'
```

---

## Important Notes

### ngrok Limitations (Free Tier):
- URL changes every time you restart ngrok
- Session timeout after 2 hours
- Limited connections per minute

### For Production:
1. Deploy your server to a cloud platform (Heroku, AWS, Azure, Render, Railway, etc.)
2. Use a permanent domain name
3. Set up proper authentication
4. Use HTTPS
5. Consider using webhooks instead of polling

### Security Recommendations:
1. Add authentication to your endpoints (JWT tokens)
2. Validate incoming data
3. Use environment variables for sensitive data
4. Monitor rate limits
5. Log all incoming requests

### Keeping ngrok URL Updated:
If using the free tier, you'll need to update the URL in your CI/CD configs each time you restart ngrok. Consider:
- Getting an ngrok paid plan for a static domain
- Using ngrok's API to get the current URL programmatically
- Deploying to a permanent server instead
