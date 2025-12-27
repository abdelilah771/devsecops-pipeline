# Test Examples for SafeOps LogMiner

## Testing Endpoints Locally

### Available Endpoints

1. **POST /logs/github** - Specifically for GitHub Actions logs
2. **POST /logs/gitlab** - Specifically for GitLab CI logs
3. **POST /logs/jenkins** - Specifically for Jenkins logs
4. **POST /logs/upload** - Generic endpoint (requires provider field)

---

## Required Fields

All endpoints require these fields:

| Field | Type | Required | Example | Notes |
|-------|------|----------|---------|-------|
| `log_data` | Object or String | Yes | `{"level": "info", "message": "..."}` | The actual log content |
| `repo_name` | String | Yes | `"myorg/myrepo"` | Repository or project name |
| `author` | String | Yes | `"john.doe"` | Who triggered the pipeline |
| `pipeline_name` | String | Yes | `"Build Pipeline"` | Name of the pipeline/workflow |
| `run_id` | String | Yes | `"12345"` | Unique run identifier |
| `timestamp_original` | String | No | `"2025-10-23T10:00:00Z"` | ISO 8601 timestamp (optional) |
| `provider` | String | Only for `/logs/upload` | `"GITHUB"` or `"GitHub Actions"` | Provider name (auto-normalized) |

---

## Provider Values

### Accepted Provider Values (with Normalization)

The `/logs/upload` endpoint now accepts various formats and automatically normalizes them:

| You Can Send | Normalized To | Examples |
|--------------|---------------|----------|
| `GITHUB`, `github`, `GitHub Actions`, `github-actions`, `GH`, `gh` | `GITHUB` | "GitHub Actions", "github", "GH" |
| `GITLAB`, `gitlab`, `GitLab CI`, `GitLab CI/CD`, `GL`, `gl` | `GITLAB` | "GitLab CI/CD", "gitlab", "GL" |
| `JENKINS`, `jenkins` | `JENKINS` | "Jenkins", "jenkins" |
| `API`, `api` | `API` | "API", "api" |

---

## Test Examples

### 1. Testing GitHub Endpoint

#### Using test file:
```bash
curl -X POST http://localhost:5000/logs/github \
  -H "Content-Type: application/json" \
  -d @test-log-github.json
```

#### Inline JSON:
```bash
curl -X POST http://localhost:5000/logs/github \
  -H "Content-Type: application/json" \
  -d '{
    "log_data": {
      "workflow": "CI Pipeline",
      "status": "success",
      "commit": "abc123"
    },
    "repo_name": "myorg/myrepo",
    "author": "github-actions",
    "pipeline_name": "Build and Test",
    "run_id": "123456",
    "timestamp_original": "2025-10-23T10:00:00Z"
  }'
```

**Expected Response:**
```json
{
  "status": "success",
  "message": "Log from GITHUB saved successfully",
  "log_id": "68fa5128649df5c378fc43be"
}
```

---

### 2. Testing GitLab Endpoint

```bash
curl -X POST http://localhost:5000/logs/gitlab \
  -H "Content-Type: application/json" \
  -d '{
    "log_data": {
      "pipeline_id": "98765",
      "job_name": "build",
      "status": "passed"
    },
    "repo_name": "mygroup/myproject",
    "author": "gitlab-ci",
    "pipeline_name": "Build Pipeline",
    "run_id": "98765",
    "timestamp_original": "2025-10-23T10:05:00Z"
  }'
```

**Expected Response:**
```json
{
  "status": "success",
  "message": "Log from GITLAB saved successfully",
  "log_id": "68fa5175649df5c378fc43c0"
}
```

---

### 3. Testing Jenkins Endpoint

```bash
curl -X POST http://localhost:5000/logs/jenkins \
  -H "Content-Type: application/json" \
  -d '{
    "log_data": {
      "build_number": "42",
      "job_name": "deploy-prod",
      "status": "SUCCESS"
    },
    "repo_name": "my-jenkins-job",
    "author": "jenkins",
    "pipeline_name": "Production Deployment",
    "run_id": "build-42",
    "timestamp_original": "2025-10-23T10:10:00Z"
  }'
```

**Expected Response:**
```json
{
  "status": "success",
  "message": "Log from JENKINS saved successfully",
  "log_id": "68fa51a3649df5c378fc43c1"
}
```

---

### 4. Testing Upload Endpoint with Provider

#### With exact provider value:
```bash
curl -X POST http://localhost:5000/logs/upload \
  -H "Content-Type: application/json" \
  -d '{
    "log_data": {
      "message": "Custom log entry"
    },
    "repo_name": "test-repo",
    "author": "test-user",
    "pipeline_name": "test-pipeline",
    "run_id": "test-123",
    "timestamp_original": "2025-10-23T10:00:00Z",
    "provider": "API"
  }'
```

#### With provider variation (GitHub Actions):
```bash
curl -X POST http://localhost:5000/logs/upload \
  -H "Content-Type: application/json" \
  -d '{
    "log_data": {
      "message": "Custom log from GitHub"
    },
    "repo_name": "test-repo",
    "author": "test-user",
    "pipeline_name": "test-pipeline",
    "run_id": "test-456",
    "timestamp_original": "2025-10-23T10:00:00Z",
    "provider": "GitHub Actions"
  }'
```

#### With provider variation (GitLab CI/CD):
```bash
curl -X POST http://localhost:5000/logs/upload \
  -H "Content-Type: application/json" \
  -d '{
    "log_data": {
      "message": "Custom log from GitLab"
    },
    "repo_name": "test-repo",
    "author": "test-user",
    "pipeline_name": "test-pipeline",
    "run_id": "test-789",
    "timestamp_original": "2025-10-23T10:00:00Z",
    "provider": "GitLab CI/CD"
  }'
```

---

## Testing with ngrok

Once you have ngrok running, replace `localhost:5000` with your ngrok URL:

```bash
# Get your ngrok URL from the ngrok dashboard
# Example: https://abc123.ngrok.io

curl -X POST https://abc123.ngrok.io/logs/github \
  -H "Content-Type: application/json" \
  -d '{
    "log_data": {"test": "ngrok test"},
    "repo_name": "test/repo",
    "author": "testuser",
    "pipeline_name": "test-pipeline",
    "run_id": "12345",
    "timestamp_original": "2025-10-23T10:00:00Z"
  }'
```

---

## Error Responses

### Missing Required Fields (400 Bad Request)

```bash
curl -X POST http://localhost:5000/logs/github \
  -H "Content-Type: application/json" \
  -d '{
    "log_data": {"test": "data"},
    "repo_name": "test/repo"
  }'
```

**Response:**
```json
{
  "errors": [
    {
      "msg": "Missing required fields"
    }
  ]
}
```

### Invalid Provider (400 Bad Request)

```bash
curl -X POST http://localhost:5000/logs/upload \
  -H "Content-Type: application/json" \
  -d '{
    "log_data": {"test": "data"},
    "repo_name": "test/repo",
    "author": "test",
    "pipeline_name": "test",
    "run_id": "123",
    "timestamp_original": "2025-10-23T10:00:00Z",
    "provider": "INVALID_PROVIDER"
  }'
```

**Response:**
```json
{
  "errors": [
    {
      "msg": "Invalid provider. Accepted values: GITHUB, GITLAB, JENKINS, API (or variations like \"GitHub Actions\", \"GitLab CI\", etc.)"
    }
  ]
}
```

### Missing Provider Field (400 Bad Request)

```bash
curl -X POST http://localhost:5000/logs/upload \
  -H "Content-Type: application/json" \
  -d '{
    "log_data": {"test": "data"},
    "repo_name": "test/repo",
    "author": "test",
    "pipeline_name": "test",
    "run_id": "123",
    "timestamp_original": "2025-10-23T10:00:00Z"
  }'
```

**Response:**
```json
{
  "errors": [
    {
      "msg": "Missing provider field"
    }
  ]
}
```

---

## Testing with PowerShell (Windows)

If you prefer PowerShell instead of curl:

```powershell
# GitHub endpoint
Invoke-RestMethod -Uri "http://localhost:5000/logs/github" `
  -Method Post `
  -ContentType "application/json" `
  -Body '{
    "log_data": {"test": "PowerShell test"},
    "repo_name": "test/repo",
    "author": "testuser",
    "pipeline_name": "test",
    "run_id": "123",
    "timestamp_original": "2025-10-23T10:00:00Z"
  }'
```

---

## Testing with Python

```python
import requests
import json
from datetime import datetime

url = "http://localhost:5000/logs/github"

payload = {
    "log_data": {
        "level": "info",
        "message": "Test from Python"
    },
    "repo_name": "python-test/repo",
    "author": "python-script",
    "pipeline_name": "Python Test Pipeline",
    "run_id": "py-123",
    "timestamp_original": datetime.utcnow().isoformat() + "Z"
}

headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
```

---

## Testing with Node.js

```javascript
const axios = require('axios');

const url = 'http://localhost:5000/logs/github';

const payload = {
  log_data: {
    level: 'info',
    message: 'Test from Node.js'
  },
  repo_name: 'nodejs-test/repo',
  author: 'nodejs-script',
  pipeline_name: 'Node.js Test Pipeline',
  run_id: 'node-123',
  timestamp_original: new Date().toISOString()
};

axios.post(url, payload)
  .then(response => {
    console.log('Status:', response.status);
    console.log('Response:', response.data);
  })
  .catch(error => {
    console.error('Error:', error.response?.data || error.message);
  });
```

---

## Verifying Logs in MongoDB Atlas

1. Go to https://cloud.mongodb.com
2. Login and navigate to your cluster
3. Click "Browse Collections"
4. Select database: `safeops-logminer`
5. Select collection: `Log`
6. You should see all your test logs

---

## Using the Provided Test Scripts

### Windows (test-ngrok.bat)

1. Edit the file and replace `YOUR_NGROK_URL` with your ngrok subdomain
2. Run: `test-ngrok.bat`
3. Check the output for success messages

### Linux/Mac (test-ngrok.sh)

1. Make executable: `chmod +x test-ngrok.sh`
2. Edit the file and replace `YOUR_NGROK_URL` with your ngrok subdomain
3. Run: `./test-ngrok.sh`
4. Check the output for success messages

---

## Batch Testing Multiple Logs

```bash
# Test all three specific endpoints
for endpoint in github gitlab jenkins; do
  echo "Testing /logs/$endpoint..."
  curl -X POST http://localhost:5000/logs/$endpoint \
    -H "Content-Type: application/json" \
    -d "{
      \"log_data\": {\"test\": \"Batch test for $endpoint\"},
      \"repo_name\": \"batch-test/repo\",
      \"author\": \"batch-tester\",
      \"pipeline_name\": \"Batch Test\",
      \"run_id\": \"batch-$RANDOM\",
      \"timestamp_original\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"
    }"
  echo -e "\n\n"
done
```

---

## Quick Summary

✅ **Fixed Issues:**
- Provider validation now accepts variations like "GitHub Actions", "GitLab CI/CD"
- Added `timestamp_original` to test files
- Server properly normalizes provider names to enum values

✅ **Ready to Use:**
- All endpoints tested and working
- Provider normalization working
- Test files updated and ready
- MongoDB Atlas connected and saving logs

🚀 **Next Steps:**
1. Start ngrok: `ngrok http 5000`
2. Test with ngrok URL
3. Configure your CI/CD pipelines
4. Monitor logs in MongoDB Atlas
