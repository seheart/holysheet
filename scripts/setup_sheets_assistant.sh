#!/bin/bash

echo "Setting up Claude Sheets Assistant..."
echo ""

echo "Step 1: Install required packages"
pip install streamlit anthropic google-api-python-client google-auth-oauthlib pandas

echo ""
echo "Step 2: Google Cloud Console Setup"
echo "1. Go to: https://console.cloud.google.com/"
echo "2. Create a new project or select existing"
echo "3. Enable Google Sheets API"
echo "4. Go to Credentials → Create Credentials → OAuth 2.0 Client ID"
echo "5. Application type: Desktop application"
echo "6. Download the JSON file and rename to 'credentials.json'"
echo "7. Place credentials.json in this directory"

echo ""
echo "Step 3: Get Anthropic API Key"
echo "1. Go to: https://console.anthropic.com/account/keys"
echo "2. Create new API key"
echo "3. Copy the key (starts with 'sk-ant-')"

echo ""
echo "Step 4: Run the assistant"
echo "streamlit run claude_sheets_assistant.py"

echo ""
echo "Ready! The assistant will open in your browser and you can:"
echo "- Chat with Claude about your sheets"
echo "- Ask it to analyze, clean up, or organize data"
echo "- Execute changes in real-time"
echo "- Get insights and suggestions"