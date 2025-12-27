@echo off
REM Test script for ngrok integration (Windows)
REM Replace YOUR_NGROK_URL with your actual ngrok URL (e.g., abc123)

set NGROK_URL=YOUR_NGROK_URL.ngrok.io

echo Testing GitHub endpoint...
curl -X POST https://%NGROK_URL%/logs/github ^
  -H "Content-Type: application/json" ^
  -d "{\"log_data\": {\"workflow\": \"CI Pipeline\", \"status\": \"success\", \"message\": \"Build completed successfully\"}, \"repo_name\": \"myorg/myrepo\", \"author\": \"github-actions\", \"pipeline_name\": \"Build and Test\", \"run_id\": \"123456\", \"timestamp_original\": \"2025-10-23T10:00:00Z\"}"

echo.
echo.
echo Testing GitLab endpoint...
curl -X POST https://%NGROK_URL%/logs/gitlab ^
  -H "Content-Type: application/json" ^
  -d "{\"log_data\": {\"pipeline_id\": \"98765\", \"job_name\": \"build\", \"status\": \"passed\"}, \"repo_name\": \"mygroup/myproject\", \"author\": \"gitlab-ci\", \"pipeline_name\": \"Build Pipeline\", \"run_id\": \"98765\", \"timestamp_original\": \"2025-10-23T10:05:00Z\"}"

echo.
echo.
echo Testing Jenkins endpoint...
curl -X POST https://%NGROK_URL%/logs/jenkins ^
  -H "Content-Type: application/json" ^
  -d "{\"log_data\": {\"build_number\": \"42\", \"job_name\": \"deploy-prod\", \"status\": \"SUCCESS\"}, \"repo_name\": \"my-jenkins-job\", \"author\": \"jenkins\", \"pipeline_name\": \"Production Deployment\", \"run_id\": \"build-42\", \"timestamp_original\": \"2025-10-23T10:10:00Z\"}"

echo.
echo.
echo All tests completed!
pause
