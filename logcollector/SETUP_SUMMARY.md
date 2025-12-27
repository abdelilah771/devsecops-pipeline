# Setup Summary - SafeOps LogMiner with ngrok

## What We Fixed

### Issue
Your application couldn't connect to MongoDB, showing error:
```
Server selection timeout: No available servers. Topology: { Type: ReplicaSetNoPrimary }
```

### Solution
Changed `DATABASE_URL` in `.env` from local MongoDB to MongoDB Atlas cloud instance.

### Current Status
✅ Server running on port 5000
✅ Connected to MongoDB Atlas
✅ Ready to receive logs from CI/CD platforms

---

## How to Use ngrok with Your CI/CD Platforms

### Step-by-Step Guide

#### 1. Install ngrok
```bash
# Download from https://ngrok.com/download
# Or use Chocolatey:
choco install ngrok

# Authenticate (get token from https://dashboard.ngrok.com)
ngrok config add-authtoken YOUR_TOKEN
```

#### 2. Start Your Server
```bash
node server.js
```
Expected output:
```
Database connected successfully
Server started on port 5000
```

#### 3. Start ngrok Tunnel
Open a NEW terminal and run:
```bash
ngrok http 5000
```

Copy your public URL (e.g., `https://abc123.ngrok.io`)

#### 4. Test the Connection
Replace `abc123` with your ngrok subdomain:

```bash
curl -X POST https://abc123.ngrok.io/logs/github -H "Content-Type: application/json" -d "{\"log_data\": {\"test\": \"data\"}, \"repo_name\": \"test/repo\", \"author\": \"testuser\", \"pipeline_name\": \"test\", \"run_id\": \"123\", \"timestamp_original\": \"2025-10-23T10:00:00Z\"}"
```

Or use the test script:
```bash
# Edit test-ngrok.bat first to add your ngrok URL
test-ngrok.bat
```

#### 5. Configure Your CI/CD Platform

Choose your platform and follow the guide:

**GitHub Actions:**
- See [examples/github-actions/simple-workflow.yml](examples/github-actions/simple-workflow.yml)
- Copy to `.github/workflows/` in your repo
- Replace `YOUR_NGROK_URL` with your ngrok subdomain

**GitLab CI:**
- See [examples/gitlab-ci/.gitlab-ci.yml](examples/gitlab-ci/.gitlab-ci.yml)
- Copy to root of your repo as `.gitlab-ci.yml`
- Replace `YOUR_NGROK_URL` with your ngrok subdomain

**Jenkins:**
- See [examples/jenkins/Jenkinsfile](examples/jenkins/Jenkinsfile)
- Copy to root of your repo as `Jenkinsfile`
- Replace `YOUR_NGROK_URL` with your ngrok subdomain

---

## Available Endpoints

| Endpoint | Method | Purpose | Provider |
|----------|--------|---------|----------|
| `/logs/github` | POST | Receive logs from GitHub Actions | GITHUB |
| `/logs/gitlab` | POST | Receive logs from GitLab CI | GITLAB |
| `/logs/jenkins` | POST | Receive logs from Jenkins | JENKINS |
| `/logs/upload` | POST | Generic log upload (specify provider) | API |

---

## Example Payloads

### GitHub Actions
```json
{
  "log_data": {
    "workflow": "CI Pipeline",
    "status": "success",
    "message": "Build completed"
  },
  "repo_name": "myorg/myrepo",
  "author": "github-actions",
  "pipeline_name": "Build and Test",
  "run_id": "123456",
  "timestamp_original": "2025-10-23T10:00:00Z"
}
```

### GitLab CI
```json
{
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
}
```

### Jenkins
```json
{
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
}
```

---

## Monitoring Your Logs

### Method 1: MongoDB Atlas Dashboard
1. Go to https://cloud.mongodb.com
2. Login with your credentials
3. Navigate to your cluster: `safeops-logminer.ns6lzot.mongodb.net`
4. Click "Browse Collections"
5. Select database: `safeops-logminer`
6. Select collection: `Log`
7. View all stored logs

### Method 2: ngrok Inspector
1. Open http://localhost:4040 in browser
2. See all incoming requests in real-time
3. Click any request to see:
   - Request headers
   - Request body
   - Response
   - Timing information

### Method 3: Server Logs
Watch your server terminal for console output showing incoming requests.

---

## File Structure

```
project/
├── server.js                          # Main server file
├── .env                              # Environment variables (MongoDB connection)
├── package.json                      # Dependencies
├── prisma/
│   └── schema.prisma                # Database schema
├── routes/
│   └── logs.js                      # Log endpoints
├── config/
│   └── db.js                        # Prisma client
├── middleware/
│   └── auth.js                      # JWT authentication
├── README.md                         # Main documentation
├── NGROK_QUICKSTART.md              # ngrok setup guide (this file)
├── INTEGRATION_GUIDE.md             # Detailed CI/CD integration
├── ARCHITECTURE.md                   # System architecture
├── test-ngrok.bat                   # Windows test script
├── test-ngrok.sh                    # Linux/Mac test script
└── examples/
    ├── github-actions/
    │   └── simple-workflow.yml      # GitHub Actions example
    ├── gitlab-ci/
    │   └── .gitlab-ci.yml          # GitLab CI example
    └── jenkins/
        └── Jenkinsfile              # Jenkins pipeline example
```

---

## Common Issues & Solutions

### ngrok URL keeps changing
**Problem:** Free tier generates new URL each restart
**Solution:**
- Upgrade to ngrok Pro ($8/month) for static domain
- Or deploy to production server (Heroku, Railway, etc.)

### Connection timeout
**Problem:** Request takes too long
**Solution:**
- Check server is running
- Check ngrok tunnel is active
- Verify MongoDB Atlas is accessible

### 404 Not Found
**Problem:** Endpoint doesn't exist
**Solution:**
- Check endpoint URL (must be `/logs/github`, `/logs/gitlab`, or `/logs/jenkins`)
- Verify ngrok URL is correct

### 400 Bad Request
**Problem:** Missing required fields
**Solution:**
- Ensure all required fields are present:
  - `log_data`
  - `repo_name`
  - `author`
  - `pipeline_name`
  - `run_id`

### 500 Server Error
**Problem:** Server-side error
**Solution:**
- Check server logs for error details
- Verify MongoDB connection
- Check data format is correct

---

## Production Deployment

### When to Deploy to Production

Deploy when you're ready to:
- Stop using ngrok (get permanent URL)
- Remove 2-hour session limits
- Scale to handle more traffic
- Add monitoring and alerting

### Recommended Platforms

1. **Railway** (Recommended for beginners)
   - Connect GitHub repo
   - Auto-deploy on push
   - Free tier available
   - Guide: https://railway.app/

2. **Heroku**
   - Simple deployment
   - Free tier (with limitations)
   - Guide: https://www.heroku.com/

3. **Render**
   - Free tier
   - Auto-deploy from Git
   - Guide: https://render.com/

4. **DigitalOcean App Platform**
   - $5/month
   - Reliable
   - Guide: https://www.digitalocean.com/

### Deployment Checklist

- [ ] Set production environment variables
- [ ] Configure MongoDB Atlas IP whitelist
- [ ] Add production domain to CORS
- [ ] Enable authentication on endpoints
- [ ] Set up logging and monitoring
- [ ] Configure SSL/HTTPS
- [ ] Update CI/CD workflows with production URL
- [ ] Test all endpoints
- [ ] Set up backup strategy

---

## Next Steps

1. ✅ MongoDB connection fixed
2. ✅ Server running locally
3. ⬜ Install and configure ngrok
4. ⬜ Test with curl or Postman
5. ⬜ Set up GitHub Actions workflow
6. ⬜ Set up GitLab CI pipeline
7. ⬜ Set up Jenkins pipeline
8. ⬜ View logs in MongoDB Atlas
9. ⬜ Deploy to production

---

## Support Resources

- **ngrok Documentation:** https://ngrok.com/docs
- **GitHub Actions:** https://docs.github.com/actions
- **GitLab CI/CD:** https://docs.gitlab.com/ee/ci/
- **Jenkins:** https://www.jenkins.io/doc/
- **MongoDB Atlas:** https://docs.atlas.mongodb.com/
- **Prisma:** https://www.prisma.io/docs/

---

## Your Current Configuration

```
Server URL:        http://localhost:5000
Database:          MongoDB Atlas
Database Name:     safeops-logminer
Cluster:           safeops-logminer.ns6lzot.mongodb.net
Collection:        Log
Status:            ✅ Running and connected
```

### Environment Variables (.env)
```
DATABASE_URL=mongodb+srv://abdelilahdahou777_db_user:***@safeops-logminer.ns6lzot.mongodb.net/safeops-logminer?retryWrites=true&w=majority&appName=safeops-logminer
PORT=5000
JWT_SECRET=your_jwt_secret
GITHUB_TOKEN=github_pat_***
```

---

**You're all set! Start with the NGROK_QUICKSTART.md guide to begin collecting logs from your CI/CD platforms.**
