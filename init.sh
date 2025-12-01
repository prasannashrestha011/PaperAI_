#!/bin/bash
# init.sh

# Activate your virtual environment if needed
# source /path/to/venv/bin/activate

# Upgrade pip

# Install dependencies
pip install -r server/requirements.txt

# Download the English model if not already installed
python -m spacy download en_core_web_sm
