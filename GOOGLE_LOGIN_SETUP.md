# Google Login Setup Guide 🔐

HolySheet v2.0 includes seamless Google Login for one-click authentication and automatic Google Sheets access.

## 🌟 Benefits of Google Login

### User Experience
- **One-click sign in** with Google account
- **Automatic sheet access** - no separate OAuth flow
- **Persistent sessions** - stay logged in across browser restarts
- **Professional appearance** - matches Google Workspace tools

### Security & Privacy
- **Google's secure authentication** system
- **No password storage** by HolySheet
- **Revocable access** through Google Account settings
- **Read-only permissions** for sheets

## ⚙️ Setup Instructions

### 1. Google Cloud Console Setup

#### Create/Select Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project or select existing
3. Name: "HolySheet" (or your preference)

#### Enable APIs
1. Navigate to **APIs & Services** → **Library**
2. Enable these APIs:
   - **Google Sheets API**
   - **Google Drive API** (optional, for enhanced features)

#### Configure OAuth Consent Screen
1. Go to **APIs & Services** → **OAuth consent screen**
2. Choose **External** user type
3. Fill required fields:
   - **App name**: HolySheet
   - **User support email**: Your email
   - **App logo**: Optional (upload HolySheet logo)
   - **App domain**: `http://localhost:8501` (for local development)
   - **Developer contact**: Your email

4. **Scopes**: Add these scopes:
   - `../auth/userinfo.email`
   - `../auth/userinfo.profile`
   - `../auth/spreadsheets.readonly`

5. **Test Users**: Add your email for testing

#### Create OAuth 2.0 Credentials
1. Go to **APIs & Services** → **Credentials**
2. Click **Create Credentials** → **OAuth 2.0 Client ID**
3. **Application type**: Web application
4. **Name**: HolySheet Web Client
5. **Authorized redirect URIs**: 
   - `http://localhost:8501`
   - `http://localhost:8501/` (with trailing slash)
6. Click **Create**
7. **Download JSON** file
8. **Rename** to `credentials.json`
9. **Place** in HolySheet project root

### 2. HolySheet Configuration

#### File Structure
```
holysheet/
├── credentials.json          # Google OAuth credentials (not in git)
├── app_v2.py                # New app with Google Login
├── auth/                    # Authentication modules
│   ├── __init__.py
│   ├── google_auth.py       # OAuth flow handling
│   ├── session_manager.py   # Session persistence
│   └── ui_components.py     # Login UI components
└── [other files]
```

#### Environment Setup
```bash
# Install additional dependencies (if needed)
pip install google-auth-oauthlib

# Start HolySheet v2
streamlit run app_v2.py
```

## 🚀 User Experience Flow

### New User Journey
```
1. Visit HolySheet → Beautiful login page
2. Click "Sign in with Google" → Google OAuth
3. Grant permissions → Automatic return to HolySheet
4. Enter Anthropic API key → Start analyzing sheets!
```

### Returning User
```
1. Visit HolySheet → Automatic login (if session valid)
2. Start analyzing immediately (no re-auth needed)
```

## 🎨 UI/UX Improvements

### Login Page Features
- **Beautiful gradient design** with HolySheet branding
- **Feature highlights** showing app capabilities
- **Privacy notice** explaining data usage
- **Professional appearance** building user trust

### Authenticated Interface
- **User profile** in sidebar with avatar and email
- **Sign out option** clearly available
- **Session status** indicators
- **Seamless sheet access** without separate OAuth

### Error Handling
- **Clear error messages** for auth failures
- **Helpful guidance** for setup issues
- **Graceful fallbacks** if Google services unavailable

## 🔐 Security Considerations

### Data Privacy
- **Minimal data collection**: Only email, name, and profile picture
- **No persistent storage**: Session data cleared on logout
- **Read-only access**: Only reads sheets, cannot modify
- **Local processing**: Sheet data processed locally

### Token Management
- **Automatic refresh**: Expired tokens refreshed transparently
- **Secure storage**: Credentials in encrypted session state
- **Proper cleanup**: All tokens cleared on logout
- **Revocation support**: Users can revoke via Google Account

### Best Practices
- **HTTPS in production**: Use SSL certificates for production
- **Environment variables**: Store sensitive config in env vars
- **Regular updates**: Keep Google client libraries updated
- **Security monitoring**: Monitor for unusual access patterns

## 🛠️ Development Notes

### Key Components

#### `auth/google_auth.py`
- **GoogleAuthManager**: Main OAuth handler
- **generate_auth_url()**: Creates Google OAuth URL
- **handle_oauth_callback()**: Processes auth response
- **refresh_credentials()**: Handles token refresh

#### `auth/session_manager.py`
- **SessionManager**: Handles session persistence
- **save_session()**: Stores user session
- **is_session_valid()**: Validates current session
- **clear_session()**: Cleans up on logout

#### `auth/ui_components.py`
- **show_login_page()**: Beautiful login interface
- **show_user_profile()**: User info in sidebar
- **show_privacy_notice()**: Privacy information
- **handle_auth_ui()**: Main auth UI flow

### Integration Points
- **Streamlit session state**: Persistent across page reloads
- **Google Sheets API**: Automatic service creation
- **Error boundaries**: Graceful handling of auth failures
- **URL handling**: OAuth callback processing

## 🧪 Testing the Implementation

### Local Testing
1. **Start app**: `streamlit run app_v2.py`
2. **Visit**: http://localhost:8501
3. **Should see**: Beautiful login page
4. **Click login**: Redirects to Google OAuth
5. **Grant permissions**: Returns to HolySheet
6. **Enter API key**: Start using the app

### Troubleshooting

#### "credentials.json not found"
- Download OAuth credentials from Google Cloud Console
- Ensure file is named exactly `credentials.json`
- Place in project root directory

#### "Redirect URI mismatch"
- Check OAuth client configuration in Google Cloud Console
- Ensure `http://localhost:8501` is listed in authorized URIs
- Include both with and without trailing slash

#### "OAuth consent screen not configured"
- Complete OAuth consent screen setup in Google Cloud Console
- Add your email as test user if app is in testing mode

#### "Access denied"
- Ensure Google Sheets API is enabled
- Check that user has access to sheets they're trying to analyze
- Verify OAuth scopes include spreadsheets.readonly

## 🔮 Future Enhancements

### Planned Features
- **Remember last sheets**: Quick access to recently analyzed sheets
- **User preferences**: Save API keys and settings (securely)
- **Team sharing**: Share analyses with team members
- **Usage analytics**: Track API usage and costs
- **Offline mode**: Cache sheets for offline analysis

### Technical Improvements
- **Production OAuth**: Verified app for public use
- **Database integration**: User profiles and preferences
- **Multi-tenancy**: Support for organizations
- **Enhanced security**: Additional security measures

---

## 📞 Support

### Common Issues
- Check the **[Troubleshooting Guide](wiki/Troubleshooting.md)** first
- Review **[API Setup Guide](wiki/API-Setup.md)** for detailed steps
- Open **[GitHub Issue](https://github.com/seheart/holysheet/issues)** for bugs

### Community
- **[GitHub Discussions](https://github.com/seheart/holysheet/discussions)** for questions
- **[Wiki](https://github.com/seheart/holysheet/wiki)** for comprehensive docs

---

**Holy Sheet, one-click authentication makes everything divine!** 🙏✨

The Google Login integration transforms HolySheet from a technical tool to a professional, user-friendly application that matches modern user expectations.