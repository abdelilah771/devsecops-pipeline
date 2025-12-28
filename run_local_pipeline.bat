@echo off
echo ==========================================
echo   Simulating Jenkins Pipeline Locally
echo ==========================================

echo [Stage: Build ^& Test Microservices]
echo ------------------------------------------

echo [1/6] Building LogCollector...
docker build -t devsecops/logcollector ./logcollector
if %errorlevel% neq 0 exit /b %errorlevel%

echo [2/6] Building LogParser...
docker build -t devsecops/logparser ./logparser
if %errorlevel% neq 0 exit /b %errorlevel%

echo [3/6] Building VulnDetector...
docker build -t devsecops/vulndetector ./vulndetcteur
if %errorlevel% neq 0 exit /b %errorlevel%

echo [4/6] Building FixSuggester...
docker build -t devsecops/fixsuggester ./FixSuggester
if %errorlevel% neq 0 exit /b %errorlevel%

echo [5/6] Building ReportGenerator...
docker build -t devsecops/reportgenerator ./ReportGenerator
if %errorlevel% neq 0 exit /b %errorlevel%

echo [Stage: Build Frontend]
echo ------------------------------------------

echo [6/6] Building Dashboard...
docker build -t devsecops/dashboard ./dashboard
if %errorlevel% neq 0 exit /b %errorlevel%

echo ==========================================
echo   Pipeline Simulation Completed Successfully
echo ==========================================
pause
