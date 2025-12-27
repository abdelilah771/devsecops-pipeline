# SafeOps LogMiner - Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         CI/CD Platforms                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │   GitHub     │  │   GitLab     │  │   Jenkins    │              │
│  │   Actions    │  │   CI/CD      │  │   Pipeline   │              │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘              │
│         │                  │                  │                      │
│         │ POST /logs/      │ POST /logs/      │ POST /logs/         │
│         │ github           │ gitlab           │ jenkins             │
└─────────┼──────────────────┼──────────────────┼──────────────────────┘
          │                  │                  │
          │                  │                  │
          └──────────────────┴──────────────────┘
                             │
                             ▼
          ┌──────────────────────────────────────┐
          │         ngrok Tunnel                 │
          │  https://abc123.ngrok.io            │
          │  (Public Internet Access)            │
          └──────────────┬───────────────────────┘
                         │
                         │ Forwards to
                         ▼
          ┌──────────────────────────────────────┐
          │    Your Local Development Server     │
          │    http://localhost:5000             │
          │                                       │
          │  ┌────────────────────────────┐      │
          │  │  Express.js REST API       │      │
          │  │                            │      │
          │  │  Routes:                   │      │
          │  │  - POST /logs/github       │      │
          │  │  - POST /logs/gitlab       │      │
          │  │  - POST /logs/jenkins      │      │
          │  │  - POST /logs/upload       │      │
          │  └────────────┬───────────────┘      │
          │               │                       │
          │               │ Prisma ORM            │
          │               ▼                       │
          │  ┌────────────────────────────┐      │
          │  │    Prisma Client           │      │
          │  │    (Database Layer)        │      │
          │  └────────────┬───────────────┘      │
          └───────────────┼───────────────────────┘
                          │
                          │ Saves logs
                          ▼
          ┌──────────────────────────────────────┐
          │      MongoDB Atlas (Cloud)           │
          │                                       │
          │  Database: safeops-logminer          │
          │  Collection: Log                     │
          │                                       │
          │  Fields:                             │
          │  - id (ObjectId)                     │
          │  - log_data (JSON)                   │
          │  - repo_name (String)                │
          │  - author (String)                   │
          │  - pipeline_name (String)            │
          │  - run_id (String)                   │
          │  - timestamp_original (Date)         │
          │  - timestamp_received (Date)         │
          │  - provider (Enum)                   │
          └──────────────────────────────────────┘
```

## Data Flow

### 1. Trigger Event
- Developer pushes code to GitHub/GitLab
- Or Jenkins build starts
- Or manual API call is made

### 2. CI/CD Pipeline Execution
- Pipeline runs (build, test, deploy)
- At each stage or completion, pipeline sends HTTP POST request

### 3. Request Structure
```json
{
  "log_data": {
    "workflow": "CI Pipeline",
    "status": "success",
    "custom_fields": "..."
  },
  "repo_name": "org/repository",
  "author": "developer-name",
  "pipeline_name": "Build Pipeline",
  "run_id": "12345",
  "timestamp_original": "2025-10-23T10:00:00Z"
}
```

### 4. ngrok Tunnel
- Receives request from public internet
- Forwards to local server at http://localhost:5000
- Maintains bidirectional connection

### 5. Express.js Server
- Receives POST request
- Validates required fields
- Sanitizes log_data (removes HTML tags)
- Calls Prisma to save data

### 6. Prisma ORM
- Formats data for MongoDB
- Handles ObjectId generation
- Manages database connection
- Executes insert operation

### 7. MongoDB Atlas
- Stores log document
- Indexes for quick retrieval
- Replicates data for reliability
- Accessible from anywhere

## Request/Response Flow Example

### GitHub Actions Example

```
GitHub Actions
     │
     │ POST https://abc123.ngrok.io/logs/github
     │ Content-Type: application/json
     │ Body: { log_data, repo_name, author, ... }
     │
     ▼
ngrok Tunnel
     │
     │ Forwards to localhost:5000
     │
     ▼
Express Server (routes/logs.js)
     │
     │ 1. Validate fields
     │ 2. Sanitize log_data
     │ 3. Call prisma.log.create()
     │
     ▼
Prisma Client
     │
     │ Generate ObjectId
     │ Add timestamp_received
     │ Insert document
     │
     ▼
MongoDB Atlas
     │
     │ Save to Log collection
     │ Return inserted document
     │
     ▼
Express Server
     │
     │ Return 201 Created
     │ { status: "success", message: "...", log_id: "..." }
     │
     ▼
GitHub Actions
     │
     └─ Workflow continues
```

## Component Details

### ngrok (Development Tunnel)
- **Purpose**: Expose local server to internet
- **Free Tier**: Random URL, 2-hour sessions
- **Paid Tier**: Static domain, unlimited sessions
- **Alternatives**: localtunnel, serveo, Tailscale

### Express.js Server
- **Port**: 5000
- **Framework**: Express.js (Node.js)
- **Middleware**: body-parser, cors
- **Authentication**: JWT (for protected routes)

### Prisma ORM
- **Provider**: MongoDB
- **Features**: Type safety, migrations, schema management
- **Connection**: MongoDB connection string from .env

### MongoDB Atlas
- **Type**: Cloud-hosted MongoDB
- **Cluster**: safeops-logminer.ns6lzot.mongodb.net
- **Region**: Configurable
- **Backup**: Automated

## Security Layers

```
┌─────────────────────────────────────┐
│  CI/CD Platform                     │
│  - GitHub/GitLab/Jenkins secrets    │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  ngrok Tunnel                       │
│  - HTTPS encryption (TLS 1.2+)      │
│  - Request inspection dashboard     │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Express Server                     │
│  - Input validation                 │
│  - HTML sanitization                │
│  - JWT authentication (optional)    │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Prisma ORM                         │
│  - SQL injection protection         │
│  - Type validation                  │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  MongoDB Atlas                      │
│  - Authentication required          │
│  - IP allowlist                     │
│  - Encryption at rest               │
│  - Encryption in transit            │
└─────────────────────────────────────┘
```

## Scaling for Production

### Current Setup (Development)
```
Local Server → ngrok → Internet
```

### Production Setup (Recommended)
```
CI/CD → Load Balancer → Multiple Servers → MongoDB Cluster
                    ↓
              Auto-scaling
              Health checks
              SSL termination
```

### Production Deployment Options

1. **Heroku** (Easiest)
   - Deploy with Git
   - Automatic HTTPS
   - Free tier available

2. **Railway** (Modern)
   - GitHub integration
   - Automatic deployments
   - Pay per usage

3. **AWS/Azure/GCP** (Enterprise)
   - Full control
   - Highest scalability
   - More complex setup

4. **DigitalOcean App Platform** (Balanced)
   - Simple deployment
   - Good pricing
   - Managed services

## Monitoring & Debugging

### ngrok Inspector
- URL: http://localhost:4040
- Shows all HTTP requests
- Request/response details
- Replay requests

### Server Logs
- Console output
- Error tracking
- Request logging

### MongoDB Atlas Monitoring
- Query performance
- Storage usage
- Connection pools
- Real-time metrics

## Future Enhancements

1. **Authentication**
   - API keys per CI/CD platform
   - JWT tokens
   - Rate limiting

2. **Log Analysis**
   - Pattern detection
   - Error aggregation
   - Trend analysis
   - Anomaly detection

3. **Dashboard**
   - Real-time log viewer
   - Search and filter
   - Visualizations
   - Alerts

4. **Integrations**
   - Slack notifications
   - Email alerts
   - Webhook triggers
   - Export to S3/Cloud Storage

5. **Advanced Features**
   - Log retention policies
   - Compression
   - Full-text search
   - Machine learning insights
