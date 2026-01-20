#!/bin/bash

# Start Celery worker in background
echo "Starting Celery worker..."
celery -A src.celery_app.celery worker --loglevel=info &

# Start FastAPI app
echo "Starting FastAPI app..."
uvicorn src.main:app --host 0.0.0.0 --port 8000
