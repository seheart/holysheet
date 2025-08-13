# API Setup Guide 🔐

HolySheet requires two API integrations to work its divine magic. This guide walks you through setting up both.

## 🤖 Anthropic API (Claude)

### Creating Your API Key

1. **Visit Anthropic Console**: https://console.anthropic.com/account/keys
2. **Sign in** with your existing account (or create one)
3. **Click "Create Key"**
4. **Name your key**: "HolySheet" or similar
5. **Copy the key** - it starts with `sk-ant-`

### Adding Credits

⚠️ **Important**: You need credits to use the API!

1. **Go to Billing**: https://console.anthropic.com/settings/billing
2. **Add Credits**: Start with $5-10 (lasts months for typical use)
3. **Or set up monthly billing** if you prefer

### Cost Expectations

- **Claude 3.5 Sonnet**: ~$3 per million input tokens
- **Typical HolySheet usage**: $2-5/month
- **Heavy analysis**: $5-15/month
- **One analysis session**: Usually under $0.50

### Using Your Key in HolySheet

1. **Start HolySheet**: `streamlit run app.py`
2. **Enter API Key**: Paste your key in the sidebar
3. **Success**: You should see "✅ Claude connected!"

---

## 📊 Google Sheets API

### Setting Up Google Cloud Project

#### Step 1: Create Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click **"New Project"** (or select existing)
3. **Name it**: "HolySheet" or similar
4. Click **"Create"**

#### Step 2: Enable API
1. Go to **"APIs & Services"** → **"Library"**
2. Search for **"Google Sheets API"**
3. Click on it and press **"Enable"**

#### Step 3: Create Credentials
1. Go to **"APIs & Services"** → **"Credentials"**
2. Click **"Create Credentials"** → **"OAuth 2.0 Client ID"**
3. If prompted, configure OAuth consent screen:
   - **User Type**: External
   - **App name**: "HolySheet"
   - **User support email**: Your email
   - **Scopes**: Add `../auth/spreadsheets.readonly`
4. **Application type**: Desktop application
5. **Name**: "HolySheet Desktop"
6. Click **"Create"**

#### Step 4: Download Credentials
1. **Download JSON** file from the credentials page
2. **Rename** it to `credentials.json`
3. **Place** in your HolySheet project folder

### OAuth Consent Screen

If your app needs verification:

- **Development**: Add yourself as a test user
- **Production**: Submit for verification (not needed for personal use)

### First-Time Authorization

1. **Start HolySheet** and click "Connect Google Sheets"
2. **Browser opens** → Google OAuth flow
3. **Choose your account**
4. **Grant permissions** (read-only access to sheets)
5. **Copy authorization code** back to HolySheet

---

## 🔒 Security Best Practices

### API Key Security
- **Never share** your Anthropic API key
- **Don't commit** keys to git (`.gitignore` protects you)
- **Regenerate** if accidentally exposed

### Google Credentials
- **Keep `credentials.json` private** (also in `.gitignore`)
- **Use read-only permissions** (HolySheet only reads sheets)
- **Revoke access** anytime from your Google Account settings

### Local Storage
- All keys stored locally in encrypted form
- No data sent to external services (except Claude API)
- Your spreadsheet data stays on your machine

---

## 🛠️ Troubleshooting API Issues

### Anthropic API
- **"Credit balance too low"** → Add credits to your account
- **"Invalid API key"** → Check key format (starts with `sk-ant-`)
- **"Rate limited"** → Wait a moment and try again

### Google Sheets API
- **"Credentials not found"** → Ensure `credentials.json` is in project root
- **"Permission denied"** → Check sheet sharing settings
- **"API not enabled"** → Enable Google Sheets API in Cloud Console

### Still Having Issues?
Check the **[Troubleshooting Guide](Troubleshooting)** for more solutions!

---

**Ready to unleash divine analysis powers?** Next: **[🚀 First Analysis](First-Analysis)** 🙏✨