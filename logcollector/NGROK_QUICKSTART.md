# ngrok Quick Start Guide

## What is ngrok?

ngrok creates a secure tunnel from a public URL to your local server, allowing external services (like GitHub, GitLab, Jenkins) to send data to your development machine.

## Quick Setup (5 Minutes)

### Step 1: Install ngrok

**Option A: Download Manually**
1. Go to https://ngrok.com/download
2. Download for Windows
3. Extract `ngrok.exe` to a folder (e.g., `C:\ngrok\`)

**Option B: Using Chocolatey**
```bash
choco install ngrok
```

### Step 2: Sign Up and Get Auth Token

1. Create account: https://dashboard.ngrok.com/signup
2. Get your token: https://dashboard.ngrok.com/get-started/your-authtoken
3. Authenticate ngrok:
```bash
ngrok config add-authtoken YOUR_AUTH_TOKEN_HERE
```

### Step 3: Start Your Server

Make sure your server is running:
```bash
node server.js
```

You should see:
```
Database connected successfully
Server started on port 5000
```

### Step 4: Start ngrok

Open a NEW terminal/command prompt and run:
```bash
ngrok http 5000
```

You'll see output like this:
```
ngrok

Session Status                online
Account                       your-email@example.com
Version                       3.x.x
Region                        United States (us)
Latency                       -
Web Interface                 http://127.0.0.1:4040
Forwarding                    https://a1b2c3d4.ngrok.io -> http://localhost:5000

Connections                   ttl     opn     rt1     rt5     p50     p90
                              0       0       0.00    0.00    0.00    0.00
```

**IMPORTANT:** Copy your Forwarding URL (e.g., `https://a1b2c3d4.ngrok.io`)

### Step 5: Test Your Setup

**Option A: Use the test script (Windows)**

1. Edit `test-ngrok.bat`
2. Replace `YOUR_NGROK_URL` with your ngrok subdomain (e.g., `a1b2c3d4`)
3. Run:
```bash
test-ngrok.bat
```

**Option B: Manual curl test**

Replace `a1b2c3d4` with your actual ngrok subdomain:

```bash
curl -X POST https://a1b2c3d4.ngrok.io/logs/github -H "Content-Type: application/json" -d "{\"log_data\": {\"test\": \"data\"}, \"repo_name\": \"test/repo\", \"author\": \"testuser\", \"pipeline_name\": \"test\", \"run_id\": \"123\", \"timestamp_original\": \"2025-10-23T10:00:00Z\"}"
```

**Option C: Use Postman or Insomnia**

1. Method: POST
2. URL: `https://YOUR_NGROK_URL.ngrok.io/logs/github`
3. Headers: `Content-Type: application/json`
4. Body (raw JSON):
```json
{
  "log_data": {
    "test": "data",
    "message": "Testing ngrok integration"
  },
  "repo_name": "test/repo",
  "author": "testuser",
  "pipeline_name": "test-pipeline",
  "run_id": "12345",
  "timestamp_original": "2025-10-23T10:00:00Z"
}
```

### Step 6: View Requests in Real-Time

ngrok provides a web interface to inspect requests:

1. Open http://127.0.0.1:4040 in your browser
2. You'll see all incoming HTTP requests
3. Click on any request to see:
   - Headers
   - Request body
   - Response
   - Timing

This is VERY helpful for debugging!

## Using with CI/CD Platforms

### For GitHub Actions:

1. Copy your ngrok URL (e.g., `https://a1b2c3d4.ngrok.io`)
2. See `INTEGRATION_GUIDE.md` for workflow examples
3. Replace `YOUR_NGROK_URL` in the workflow files with `a1b2c3d4`

### For GitLab CI:

1. Copy your ngrok URL
2. Update `.gitlab-ci.yml` with your ngrok URL
3. See `INTEGRATION_GUIDE.md` for examples

### For Jenkins:

1. Copy your ngrok URL
2. Update your Jenkinsfile or job configuration
3. See `INTEGRATION_GUIDE.md` for examples

## Monitoring Your Logs

You can verify logs are being saved by:

### Option 1: Check MongoDB Atlas
1. Go to https://cloud.mongodb.com
2. Navigate to your cluster
3. Click "Browse Collections"
4. Select `safeops-logminer` database
5. Select `Log` collection

### Option 2: Create a GET endpoint (coming soon)
Add an endpoint to view logs via API

## Common Issues

### Issue 1: "command not found: ngrok"
**Solution:** Add ngrok to your PATH or use full path to ngrok.exe

### Issue 2: ngrok session expired
**Solution:** The free tier has 2-hour sessions. Just restart ngrok:
```bash
ngrok http 5000
```
**Note:** URL will change, so update your CI/CD configs

### Issue 3: "Connection refused"
**Solution:** Make sure your server is running on port 5000 first

### Issue 4: "404 Not Found"
**Solution:** Check your endpoint URL:
- GitHub: `/logs/github`
- GitLab: `/logs/gitlab`
- Jenkins: `/logs/jenkins`

## Tips

### Tip 1: Keep ngrok URL Static (Paid Plan)
Free tier gives you a new URL each restart. For $8/month, get:
- Static domain
- No session limits
- More concurrent connections

### Tip 2: Use ngrok Config File
Create `ngrok.yml`:
```yaml
version: "2"
authtoken: YOUR_AUTH_TOKEN
tunnels:
  logminer:
    proto: http
    addr: 5000
    inspect: true
```

Then run:
```bash
ngrok start logminer
```

### Tip 3: Monitor in Terminal
Watch your server logs and ngrok logs simultaneously to debug issues

### Tip 4: For Production
Don't use ngrok in production! Deploy to:
- Heroku
- Railway
- Render
- AWS/Azure/GCP
- DigitalOcean
- Vercel (for serverless)

## Next Steps

1. ✅ Set up ngrok
2. ✅ Test with curl
3. ✅ Configure GitHub Actions (see INTEGRATION_GUIDE.md)
4. ✅ Configure GitLab CI (see INTEGRATION_GUIDE.md)
5. ✅ Configure Jenkins (see INTEGRATION_GUIDE.md)
6. 📊 Create a dashboard to view collected logs
7. 🚀 Deploy to production server

## Support

- ngrok docs: https://ngrok.com/docs
- ngrok dashboard: https://dashboard.ngrok.com
- GitHub Actions docs: https://docs.github.com/actions
- GitLab CI docs: https://docs.gitlab.com/ee/ci/
- Jenkins docs: https://www.jenkins.io/doc/

## Your Current Setup

- Server: http://localhost:5000
- Database: MongoDB Atlas (safeops-logminer)
- Available endpoints:
  - POST /logs/github
  - POST /logs/gitlab
  - POST /logs/jenkins
  - POST /logs/upload (with provider field)
