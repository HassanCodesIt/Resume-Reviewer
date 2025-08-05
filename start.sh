#!/bin/bash
# Startup script for Render deployment

# Set environment variables
export PYTHONPATH="${PYTHONPATH}:${PWD}"

# Create uploads directory if it doesn't exist
mkdir -p uploads

# Download spaCy model if not present
python -c "import spacy; spacy.load('en_core_web_sm')" 2>/dev/null || python -m spacy download en_core_web_sm

# Start the application
exec gunicorn run:app --bind 0.0.0.0:$PORT --timeout 120 --workers 1 --keep-alive 5 --max-requests 1000 