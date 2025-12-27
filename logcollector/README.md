# SafeOps-LogMiner - LogCollector Microservice

This microservice is a component of the SafeOps-LogMiner platform. It is responsible for collecting and storing pipeline logs from various CI/CD sources (GitHub Actions, GitLab CI, Jenkins, and more).

## Quick Start with ngrok

To test locally with CI/CD platforms, see [NGROK_QUICKSTART.md](NGROK_QUICKSTART.md) for a 5-minute setup guide.

## Features

- **Node.js & Express**: Built with a robust and popular backend framework.
- **MongoDB Storage**: Uses Mongoose for reliable and scalable log storage.
- **REST Endpoints**: Provides endpoints for both pushing logs via API and pulling them from services like GitHub.
- **Secure**: Includes patterns for input validation, sanitization, and authentication (JWT).
- **Flexible Payload**: Accepts logs as either `application/json` or `text/plain`.

## Documentation

- [NGROK_QUICKSTART.md](NGROK_QUICKSTART.md) - Quick setup guide for testing with ngrok
- [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md) - Complete CI/CD integration examples
- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture and data flow
- [examples/](examples/) - Ready-to-use workflow files

## Prerequisites

- [Node.js](https://nodejs.org/) v18+
- MongoDB (Atlas cloud or local installation)
- [ngrok](https://ngrok.com) (for local development with CI/CD platforms)

## 1. Installation

Clone the repository and install the dependencies.

```bash
npm install
```

## 2. Configuration

Create a `.env` file in the root of the project and add the following environment variables. A template is provided in `.env.example`.

```env
# MongoDB Connection String
# Replace with your actual MongoDB connection string
MONGO_URI=mongodb://localhost:27017/safeops-logminer

# JWT Secret for token generation
# Replace with a long, random, and secret string for production
JWT_SECRET=your_jwt_secret

# GitHub Personal Access Token (PAT)
# Required for the /logs/github endpoint. Generate a token with 'repo' scope.
GITHUB_TOKEN=your_github_personal_access_token

# Port for the server to run on
PORT=5000
```

## 3. Running the Service

Start the server using:

```bash
node server.js
```

The service will be running at `http://localhost:5000`.

## 4. API Endpoints

### POST /webhook

Generic endpoint for receiving logs from various CI/CD providers (simulated).

- **URL**: `/webhook`
- **Method**: `POST`
- **Body**: JSON

```json
{
  "provider": "GITHUB",
  "repo_name": "safeops/logminer",
  "pipeline_name": "ci-build",
  "log": "Job: build\nStep: Checkout..."
}
```

**Response**:
```json
{
  "run_id": "test-run-1234567890",
  "status": "stored_and_parse_triggered"
}
```

This endpoint:
1. Generates a `run_id`.
2. Stores the log in MongoDB `Log` collection.
3. Triggers the LogParser service via REST (`POST http://logparser/parse?run_id=...`).

- **URL**: `/logs/github`
- **Method**: `GET`
- **Authentication**: **Required**. A valid JWT must be passed in the `x-auth-token` header.
- **Query Parameters**:
  - `owner`: The repository owner.
  - `repo`: The repository name.
  - `run_id`: The ID of the GitHub Actions workflow run.

**Example Request**

`GET /logs/github?owner=my-org&repo=my-app&run_id=123456789`

### How to Connect GitHub Actions

You can use a tool like `curl` in a workflow step to push logs to the `/logs/upload` endpoint.

1.  **Store Endpoint URL as a Secret**: In your GitHub repository, go to `Settings > Secrets and variables > Actions` and create a new secret (e.g., `LOG_COLLECTOR_URL`) with your endpoint's URL (`http://your-server-address:5000/logs/upload`).

2.  **Add a Step to Your Workflow**: In your `.github/workflows/main.yml` file, add a final step that sends the log data.

```yaml
name: CI Build

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      # ... your other build and test steps ...

      - name: Send Log to SafeOps-LogMiner
        if: always() # Ensures this step runs even if previous steps fail
        run: |
          LOG_CONTENT="Pipeline run for ${{ github.repository }} by ${{ github.actor }}."
          # In a real scenario, you might collect logs from a file
          # LOG_CONTENT=$(cat build.log)

          curl -X POST ${{ secrets.LOG_COLLECTOR_URL }} \
          -H "Content-Type: application/json" \
          -d '{
            "log_data": "${LOG_CONTENT}",
            "repo_name": "${{ github.repository }}",
            "author": "${{ github.actor }}",
            "pipeline_name": "${{ github.workflow }}",
            "run_id": "${{ github.run_id }}",
            "timestamp_original": "${{ github.event.head_commit.timestamp }}",
            "source": "GitHub"
          }'
```