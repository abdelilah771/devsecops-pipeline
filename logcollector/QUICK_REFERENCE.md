# Quick Reference Card

## ngrok Setup (3 Commands)

```bash
# 1. Install ngrok (one-time)
# Download from: https://ngrok.com/download

# 2. Authenticate (one-time)
ngrok config add-authtoken YOUR_TOKEN_FROM_DASHBOARD

# 3. Start tunnel (every time)
ngrok http 5000
```

**Copy this URL:** `https://YOUR_SUBDOMAIN.ngrok.io`

---

## Test Your Setup

```bash
# Replace abc123 with your ngrok subdomain
curl -X POST https://abc123.ngrok.io/logs/github \
  -H "Content-Type: application/json" \
  -d '{"log_data":{"test":"Hello"},"repo_name":"test/repo","author":"me","pipeline_name":"test","run_id":"1","timestamp_original":"2025-10-23T10:00:00Z"}'
```

**Expected Response:**
```json
{
  "status": "success",
  "message": "Log from GITHUB saved successfully",
  "log_id": "672f..."
}
```

---

## GitHub Actions (Minimal)

**.github/workflows/send-logs.yml**
```yaml
name: Send Logs
on: [push]
jobs:
  log:
    runs-on: ubuntu-latest
    steps:
      - run: |
          curl -X POST https://YOUR_NGROK_URL.ngrok.io/logs/github \
            -H "Content-Type: application/json" \
            -d "{
              \"log_data\": {\"status\": \"${{ job.status }}\"},
              \"repo_name\": \"${{ github.repository }}\",
              \"author\": \"${{ github.actor }}\",
              \"pipeline_name\": \"${{ github.workflow }}\",
              \"run_id\": \"${{ github.run_id }}\",
              \"timestamp_original\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"
            }"
```

---

## GitLab CI (Minimal)

**.gitlab-ci.yml**
```yaml
send-logs:
  stage: .post
  script:
    - |
      curl -X POST https://YOUR_NGROK_URL.ngrok.io/logs/gitlab \
        -H "Content-Type: application/json" \
        -d "{
          \"log_data\": {\"status\": \"${CI_JOB_STATUS}\"},
          \"repo_name\": \"${CI_PROJECT_PATH}\",
          \"author\": \"${GITLAB_USER_LOGIN}\",
          \"pipeline_name\": \"${CI_PIPELINE_SOURCE}\",
          \"run_id\": \"${CI_PIPELINE_ID}\",
          \"timestamp_original\": \"${CI_PIPELINE_CREATED_AT}\"
        }"
```

---

## Jenkins (Minimal)

**Jenkinsfile**
```groovy
pipeline {
    agent any
    post {
        always {
            sh '''
                curl -X POST https://YOUR_NGROK_URL.ngrok.io/logs/jenkins \
                  -H "Content-Type: application/json" \
                  -d "{
                    \\"log_data\\": {\\"build\\": \\"${BUILD_NUMBER}\\"},
                    \\"repo_name\\": \\"${JOB_NAME}\\",
                    \\"author\\": \\"jenkins\\",
                    \\"pipeline_name\\": \\"${JOB_NAME}\\",
                    \\"run_id\\": \\"${BUILD_ID}\\",
                    \\"timestamp_original\\": \\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\\"
                  }"
            '''
        }
    }
}
```

---

## Required Fields

All endpoints require these fields:

| Field | Type | Example | Description |
|-------|------|---------|-------------|
| `log_data` | Object/String | `{"status": "success"}` | The actual log content |
| `repo_name` | String | `"myorg/myrepo"` | Repository or project name |
| `author` | String | `"john.doe"` | Who triggered the pipeline |
| `pipeline_name` | String | `"Build Pipeline"` | Name of the pipeline/workflow |
| `run_id` | String | `"12345"` | Unique run identifier |
| `timestamp_original` | String | `"2025-10-23T10:00:00Z"` | When the pipeline started (ISO 8601) |

---

## Monitoring URLs

| Tool | URL | Purpose |
|------|-----|---------|
| ngrok Inspector | http://localhost:4040 | See all HTTP requests |
| MongoDB Atlas | https://cloud.mongodb.com | View stored logs |
| Local Server | http://localhost:5000 | Your API server |

---

## Common Commands

```bash
# Start server
node server.js

# Start ngrok
ngrok http 5000

# Test GitHub endpoint
curl -X POST https://YOUR_URL.ngrok.io/logs/github -H "Content-Type: application/json" -d @test-log.json

# Test GitLab endpoint
curl -X POST https://YOUR_URL.ngrok.io/logs/gitlab -H "Content-Type: application/json" -d @test-log.json

# Test Jenkins endpoint
curl -X POST https://YOUR_URL.ngrok.io/logs/jenkins -H "Content-Type: application/json" -d @test-log.json

# Kill process on port 5000
npx kill-port 5000

# Regenerate Prisma client
npx prisma generate

# View MongoDB schema
npx prisma db push
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| ngrok not found | Add to PATH or use full path to ngrok.exe |
| Connection refused | Start server first: `node server.js` |
| 404 Not Found | Check endpoint: `/logs/github` not `/logs` |
| 400 Bad Request | Include all required fields |
| 500 Server Error | Check server logs, verify MongoDB connection |
| ngrok URL changed | Free tier resets URL on restart - update CI/CD configs |

---

## Project Structure

```
📁 project/
├── 📄 server.js                 # Start here
├── 📄 .env                      # MongoDB connection (DO NOT COMMIT)
├── 📄 README.md                 # Main docs
├── 📄 NGROK_QUICKSTART.md       # Setup guide
├── 📄 INTEGRATION_GUIDE.md      # CI/CD examples
├── 📄 SETUP_SUMMARY.md          # What we fixed
├── 📄 test-ngrok.bat           # Test script (Windows)
└── 📁 examples/
    ├── 📁 github-actions/       # GitHub workflow examples
    ├── 📁 gitlab-ci/            # GitLab pipeline examples
    └── 📁 jenkins/              # Jenkins pipeline examples
```

---

## Help & Resources

**Detailed Guides:**
- Quick Start: [NGROK_QUICKSTART.md](NGROK_QUICKSTART.md)
- Integration: [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)
- Architecture: [ARCHITECTURE.md](ARCHITECTURE.md)

**External Docs:**
- ngrok: https://ngrok.com/docs
- GitHub Actions: https://docs.github.com/actions
- GitLab CI: https://docs.gitlab.com/ee/ci/
- Jenkins: https://www.jenkins.io/doc/

---

**Ready to start? Run these 3 commands:**

```bash
# Terminal 1: Start your server
node server.js

# Terminal 2: Start ngrok
ngrok http 5000

# Terminal 3: Test it works
curl -X POST https://YOUR_NGROK_URL.ngrok.io/logs/github -H "Content-Type: application/json" -d '{"log_data":{"test":"works"},"repo_name":"test","author":"me","pipeline_name":"test","run_id":"1","timestamp_original":"2025-10-23T10:00:00Z"}'
```
