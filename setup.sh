#!/bin/bash

# Install Python dependencies
pip install -r requirements.txt

# Create Streamlit configuration file
mkdir -p ~/.streamlit/
echo -e "[server]\nheadless = true\nport = $PORT\nenableCORS = false\n" > ~/.streamlit/config.toml
