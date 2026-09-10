#!/bin/bash
set -e

# Run database migrations
echo "Running database migrations..."
alembic upgrade head

# Start the FastAPI server
echo "Starting FastAPI server..."
# Use the PORT environment variable if provided by the host (e.g. Render), default to 8000
PORT="${PORT:-8000}"
exec uvicorn app.main:app --host 0.0.0.0 --port $PORT
