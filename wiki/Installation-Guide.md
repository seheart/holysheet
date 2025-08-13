# Installation Guide 📦

Get HolySheet running on your machine in just a few minutes!

## Prerequisites

Before diving into divine spreadsheet analysis, make sure you have:

- **Python 3.8+** installed
- **Git** for cloning the repository
- **Google account** (for Sheets API access)
- **Anthropic account** (for Claude API access)

## Step 1: Clone the Repository

```bash
git clone https://github.com/seheart/holysheet.git
cd holysheet
```

## Step 2: Install Dependencies

### Option A: Quick Setup (Recommended)
```bash
./setup.sh
```

### Option B: Manual Installation
```bash
pip install -r requirements.txt
```

**Dependencies installed:**
- `streamlit` - Web interface
- `anthropic` - Claude AI integration  
- `google-api-python-client` - Google Sheets access
- `pandas` - Data manipulation
- `google-auth-oauthlib` - OAuth authentication

## Step 3: API Configuration

HolySheet needs two API integrations:

### 🤖 Anthropic API (Claude)
1. Go to [Anthropic Console](https://console.anthropic.com/account/keys)
2. Create a new API key
3. **Add credits** to your account (~$5-10 recommended)
4. Keep this key handy - you'll enter it in the app

### 📊 Google Sheets API
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select existing)
3. Enable the **Google Sheets API**
4. Go to **Credentials** → **Create Credentials** → **OAuth 2.0 Client ID**
5. Choose **Desktop application**
6. Download the JSON file as `credentials.json`
7. Place `credentials.json` in your HolySheet folder

## Step 4: Launch HolySheet

```bash
streamlit run app.py
```

Your browser should open to `http://localhost:8501` with HolySheet running!

## First-Time Setup in App

1. **Enter API Key**: Click the sidebar and enter your Anthropic API key
2. **Connect Google Sheets**: Click "Connect Google Sheets" and authorize
3. **Load a Sheet**: Paste any Google Sheets URL and start analyzing!

## Verify Installation

Try these quick tests:

1. **API Connection**: Enter your API key - should show "✅ Claude connected!"
2. **Google Auth**: Click "Connect Google Sheets" - should redirect to Google OAuth
3. **Load Sample**: Try loading a simple Google Sheet

## Next Steps

- **[🔐 API Setup Details](API-Setup)** - Detailed configuration guide
- **[🚀 First Analysis](First-Analysis)** - Analyze your first spreadsheet
- **[🛠️ Troubleshooting](Troubleshooting)** - If something's not working

---

**Holy Sheet, you're ready to divine insights from your spreadsheets!** 🙏✨