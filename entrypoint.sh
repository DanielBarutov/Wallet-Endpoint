#!/bin/sh
echo "Waiting for database..."
sleep 3
echo "Running migrations..."
alembic upgrade head
echo "Starting Gunicorn..."
exec gunicorn app.main:app --bind 0.0.0.0:8000 --workers 4 -k uvicorn.workers.UvicornWorker