#!/bin/bash

echo "🚀 Setting up Claude Sheets Web App..."
echo ""

echo "📦 Installing required packages..."
pip install streamlit anthropic google-api-python-client google-auth-oauthlib pandas

echo ""
echo "🔐 Google Cloud Setup:"
echo "1. Go to: https://console.cloud.google.com/"
echo "2. Create/select a project"
echo "3. Enable Google Sheets API"
echo "4. Go to Credentials → Create Credentials → OAuth 2.0 Client ID"
echo "5. Application type: Desktop application"
echo "6. Download JSON and save as 'credentials.json' in this folder"

echo ""
echo "🎯 Ready to run!"
echo "Command: streamlit run claude_sheets_webapp.py"
echo ""
echo "🌟 Features:"
echo "- Side-by-side: Chat with Claude + See your sheet"
echo "- Load any sheet by URL/ID"
echo "- Quick action buttons"
echo "- Financial data analysis"
echo "- No overlay blocking your view!"