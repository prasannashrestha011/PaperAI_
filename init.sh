#!/bin/bash
# init.sh

# Install dependencies
pip install -r server/requirements.txt

# Download the English model if not already installed
python -m spacy download en_core_web_sm
