FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for numpy/pandas/scikit-learn if needed (often needed for binary wheels)
# But python:3.11-slim usually works for these via wheels.

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and models
COPY . .

# Expose port
EXPOSE 8000

# Run the application (using app.main:app)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
