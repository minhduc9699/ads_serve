#!/bin/bash
# Start script for Ads Server

# Activate virtual environment if exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Start with gunicorn for production
exec gunicorn --bind 0.0.0.0:8089 \
    --workers 4 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    app:app
