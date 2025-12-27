
const request = require('supertest');
const { app, startServer } = require('./server'); // Import the app and startServer
const prisma = require('./config/db');
const jwt = require('jsonwebtoken');
require('dotenv').config();

jest.setTimeout(30000);

let token;
let server;

// Before all tests, start the server and generate a JWT for authenticated routes
beforeAll(async () => {
  server = await startServer();
  token = jwt.sign({ user: { id: 'testuser' } }, process.env.JWT_SECRET, { expiresIn: '1h' });
});

// After all tests, close the server and disconnect from the database
afterAll(async () => {
  await prisma.$disconnect();
  server.close(); // Close the server to release the port
});

// Before each test, clear the database
beforeEach(async () => {
  await prisma.log.deleteMany({});
});

describe('LogCollector API', () => {
  // --- Test Suite for POST /logs/upload ---
  describe('POST /logs/upload', () => {
    // Test case for successful log upload with JSON payload
    it('should save a log successfully with a JSON payload', async () => {
      const logPayload = {
        log_data: { message: 'Successful build process.' },
        repo_name: 'test-repo',
        author: 'test-author',
        pipeline_name: 'main-build',
        run_id: 'run-123',
        source: 'API',
      };

      const res = await request(app)
        .post('/logs/upload')
        .send(logPayload)
        .expect('Content-Type', /json/)
        .expect(201);

      expect(res.body.status).toBe('success');
      expect(res.body.log_id).toBeDefined();

      // Verify the log was saved to the database
      const savedLog = await prisma.log.findUnique({ where: { id: res.body.log_id } });
      expect(savedLog).not.toBeNull();
      expect(savedLog.log_data.message).toBe('Successful build process.');
    });

    // Test case for successful log upload with text payload
    it('should save a log successfully with a text payload and query params', async () => {
      const logData = 'This is a raw text log.';
      const res = await request(app)
        .post('/logs/upload?repo_name=text-repo&author=text-author&pipeline_name=text-build&run_id=run-456&source=Webhook')
        .set('Content-Type', 'text/plain')
        .send(logData)
        .expect('Content-Type', /json/)
        .expect(201);

      expect(res.body.status).toBe('success');
      expect(res.body.log_id).toBeDefined();

      // Verify the log was saved
      const savedLog = await prisma.log.findUnique({ where: { id: res.body.log_id } });
      expect(savedLog).not.toBeNull();
      expect(savedLog.log_data).toBe(logData);
      expect(savedLog.repo_name).toBe('text-repo');
    });

    // Test case for missing required fields
    it('should return a 400 error if required fields are missing', async () => {
      const logPayload = {
        log_data: 'Incomplete log.',
        // Missing repo_name, author, etc.
      };

      const res = await request(app)
        .post('/logs/upload')
        .send(logPayload)
        .expect('Content-Type', /json/)
        .expect(400);

      expect(res.body.errors).toBeInstanceOf(Array);
      expect(res.body.errors.length).toBeGreaterThan(0);
    });

    // Test case for input sanitization
    it('should sanitize malicious input from log_data', async () => {
      const maliciousPayload = {
        log_data: '<script>alert("xss")</script>Some log text.',
        repo_name: 'secure-repo',
        author: 'hacker',
        pipeline_name: 'exploit-build',
        run_id: 'run-666',
        source: 'Unknown',
      };

      const res = await request(app)
        .post('/logs/upload')
        .send(maliciousPayload)
        .expect(201);

      // Verify the saved log data is sanitized
      const savedLog = await prisma.log.findUnique({ where: { id: res.body.log_id } });
      expect(savedLog.log_data).toBe('Some log text.');
    });
  });

  // --- Test Suite for GET /logs/github ---
  describe('GET /logs/github', () => {
    // Test case for requests without an authentication token
    it('should return a 401 error if no token is provided', async () => {
      await request(app).get('/logs/github').expect(401);
    });

    // Test case for requests with an invalid token
    it('should return a 401 error if the token is invalid', async () => {
      await request(app)
        .get('/logs/github')
        .set('x-auth-token', 'invalidtoken')
        .expect(401);
    });

    // Test case for authenticated requests missing required query parameters
    it('should return a 400 error if query parameters are missing', async () => {
      const res = await request(app)
        .get('/logs/github')
        .set('x-auth-token', token)
        .expect('Content-Type', /json/)
        .expect(400);

      expect(res.body.msg).toBe('Missing owner, repo, or run_id query parameters');
    });

    // Test case for a successful (conceptual) API call
    it('should return the conceptual info message on a successful call', async () => {
      const res = await request(app)
        .get('/logs/github?owner=test-owner&repo=test-repo&run_id=123')
        .set('x-auth-token', token)
        .expect('Content-Type', /json/)
        .expect(200);

      expect(res.body.status).toBe('info');
      expect(res.body.message).toContain('Conceptual endpoint');
    });
  });

  // --- Test Suite for POST /logs/gitlab ---
  describe('POST /logs/gitlab', () => {
    // Test case for successful log upload from GitLab
    it('should save a log from GitLab successfully', async () => {
      const logPayload = {
        log_data: 'GitLab CI log content.',
        repo_name: 'gitlab-repo',
        author: 'gitlab-user',
        pipeline_name: 'gitlab-pipeline',
        run_id: 'run-789',
      };

      const res = await request(app)
        .post('/logs/gitlab')
        .send(logPayload)
        .expect('Content-Type', /json/)
        .expect(201);

      expect(res.body.status).toBe('success');
      expect(res.body.log_id).toBeDefined();

      // Verify the log was saved to the database
      const savedLog = await prisma.log.findUnique({ where: { id: res.body.log_id } });
      expect(savedLog).not.toBeNull();
      expect(savedLog.provider).toBe('GITLAB');
    });
  });
});
