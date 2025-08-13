#!/bin/bash

echo "🙏 HolySheet Setup - Divine Sheets Analysis"
echo "=========================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

echo ""
echo "🔐 Setup Instructions:"
echo ""
echo "1. Google Cloud Setup:"
echo "   • Go to: https://console.cloud.google.com/"
echo "   • Create/select a project"
echo "   • Enable Google Sheets API"
echo "   • Create OAuth 2.0 Client ID (Desktop app)"
echo "   • Download as 'credentials.json' in this folder"
echo ""
echo "2. Anthropic API:"
echo "   • Go to: https://console.anthropic.com/account/keys"
echo "   • Create API key"
echo "   • Add $5-10 credits to your account"
echo ""
echo "3. Run the app:"
echo "   streamlit run app.py"
echo ""
echo "🙏 Holy Sheet, you're ready to divine insights from your spreadsheets!"