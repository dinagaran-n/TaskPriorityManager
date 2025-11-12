# Use lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy backend files into container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Render port
EXPOSE 10000

# Start FastAPI app
CMD ["uvicorn", "task_priority_manager_backend:app", "--host", "0.0.0.0", "--port", "10000"]
