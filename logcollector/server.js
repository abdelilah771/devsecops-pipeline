
require('dotenv').config();
const express = require('express');
const prisma = require('./config/db');

// Initialize Express app
const app = express();
const cors = require('cors');

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.text());

// A simple middleware to determine content type and place it in req.body
app.use((req, res, next) => {
  if (req.is('text/*') && typeof req.body === 'string') {
    req.body = { log_data: req.body };
  }
  next();
});

// Define Routes
app.use('/logs', require('./routes/logs'));
app.use('/webhook', require('./routes/webhook'));
app.use('/api/logs/simulate', require('./routes/simulate'));
app.use('/test', require('./routes/test'));

// Health Check Endpoint
app.get('/health', async (req, res) => {
  let mongoStatus = 'disconnected';
  try {
    // Simple check if we can query the DB
    await prisma.$runCommandRaw({ ping: 1 });
    mongoStatus = 'connected';
  } catch (e) {
    mongoStatus = 'disconnected';
  }

  res.json({
    status: 'healthy',
    mongodb: mongoStatus
  });
});

// Root endpoint
app.get('/', (req, res) => {
  res.send('SafeOps-LogMiner LogCollector Service is running.');
});

// Basic Error Handling
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).send('Something broke!');
});

const PORT = process.env.PORT || 3344;

let server;

const startServer = async () => {
  // Configuration Validation
  const requiredEnv = ['DATABASE_URL', 'LOGPARSER_URL'];
  const missingEnv = requiredEnv.filter(env => !process.env[env]);

  // Also check MONGO_URI if strictly following checklist, assuming it maps to DATABASE_URL 
  // or is just a checklist requirement. Warning if missing.
  if (!process.env.MONGO_URI && !process.env.DATABASE_URL) {
    console.warn("WARNING: MONGO_URI or DATABASE_URL not set.");
  }

  if (missingEnv.length > 0) {
    console.error(`❌ Missing required environment variables: ${missingEnv.join(', ')}`);
    // Ideally exit, but for dev/verification we might just log error or exit.
    // process.exit(1); 
  }

  try {
    await prisma.$connect();
    console.log('Database connected successfully');
    server = app.listen(PORT, () => {
      console.log(`Server started on port ${PORT}`);

      // Automatic Simulation Trigger
      if (process.env.NODE_ENV !== 'test') {
        const fs = require('fs');
        const path = require('path');
        const axios = require('axios');

        setTimeout(async () => {
          try {
            console.log('🚀 Triggering automatic simulation log...');
            const logPath = path.join(__dirname, 'test-log-github.json');

            if (fs.existsSync(logPath)) {
              const fileContent = fs.readFileSync(logPath, 'utf8');
              const logData = JSON.parse(fileContent);

              const response = await axios.post(`http://localhost:${PORT}/api/logs/simulate`, logData);
              if (response.data && response.data.success) {
                console.log(`✅ Simulation log saved. RunID: ${response.data.run_id}`);

                if (response.data.logParserStatus === 'success') {
                  console.log(`✅ LogParser (localhost:8001) successfully received the data.`);
                } else {
                  console.error(`❌ LogParser failed to receive data: ${response.data.logParserError}`);
                }
              }
            } else {
              console.warn('⚠️ test-log-github.json not found, skipping simulation');
            }
          } catch (error) {
            console.error('⚠️ Failed to send simulation log:', error.message);
          }
        }, 1500);
      }
    });
    return server;
  } catch (error) {
    console.error('Failed to connect to the database', error);
    process.exit(1);
  }
};

if (process.env.NODE_ENV !== 'test') {
  startServer();
}

module.exports = { app, server, startServer };
