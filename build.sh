#!/bin/bash
# Build script for Render deployment

# Install Python dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Create uploads directory
mkdir -p uploads

echo "Build completed successfully!" 