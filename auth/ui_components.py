"""
UI Components for Google Authentication
Beautiful login and user profile components for HolySheet
"""

import streamlit as st
from typing import Optional, Dict, Any
from .google_auth import get_auth_manager, is_authenticated, get_current_user, logout
from .session_manager import get_session_info


def show_login_page():
    """Display the Google Login page"""
    st.set_page_config(
        page_title="HolySheet - Sign In",
        page_icon="🙏",
        layout="centered"
    )
    
    # Custom CSS for login page
    st.markdown("""
    <style>
    .login-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin: 2rem 0;
    }
    .login-title {
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .login-subtitle {
        font-size: 1.2rem;
        margin-bottom: 2rem;
        opacity: 0.9;
    }
    .feature-list {
        text-align: left;
        max-width: 500px;
        margin: 2rem auto;
    }
    .feature-item {
        display: flex;
        align-items: center;
        margin: 1rem 0;
        font-size: 1.1rem;
    }
    .feature-icon {
        margin-right: 1rem;
        font-size: 1.5rem;
    }
    .google-login-btn {
        background: white;
        color: #333;
        padding: 0.75rem 2rem;
        border: none;
        border-radius: 5px;
        font-size: 1.1rem;
        font-weight: bold;
        margin: 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .google-login-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Main login container
    st.markdown("""
    <div class="login-container">
        <div class="login-title">🙏 HolySheet</div>
        <div class="login-subtitle">Divine Google Sheets analysis with Claude AI</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Features section
    st.markdown("""
    <div class="feature-list">
        <div class="feature-item">
            <span class="feature-icon">🤖</span>
            <span>Chat with Claude about your spreadsheet data</span>
        </div>
        <div class="feature-item">
            <span class="feature-icon">📊</span>
            <span>Side-by-side view of data and insights</span>
        </div>
        <div class="feature-item">
            <span class="feature-icon">🧹</span>
            <span>Data cleanup and quality improvements</span>
        </div>
        <div class="feature-item">
            <span class="feature-icon">📈</span>
            <span>Financial analysis and trend detection</span>
        </div>
        <div class="feature-item">
            <span class="feature-icon">🔐</span>
            <span>Secure, local processing of your data</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Login section
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🔐 Sign in to get started")
        
        auth_manager = get_auth_manager()
        
        if not auth_manager.is_credentials_configured():
            st.error("⚠️ Google OAuth not configured")
            st.info("Please download `credentials.json` from Google Cloud Console and place it in the project root.")
            return
        
        if st.button("🔐 Sign in with Google", key="google_login", type="primary"):
            try:
                auth_url = auth_manager.generate_auth_url()
                st.markdown(f"""
                <script>
                window.open("{auth_url}", "_self");
                </script>
                """, unsafe_allow_html=True)
                
                st.info("Redirecting to Google for authentication...")
                
            except Exception as e:
                st.error(f"Authentication error: {str(e)}")
        
        st.markdown("---")
        st.markdown("*Secure authentication powered by Google*")


def show_user_profile(user_info: Dict[str, Any]):
    """Display user profile in sidebar"""
    with st.sidebar:
        st.markdown("---")
        
        # User avatar and info
        col1, col2 = st.columns([1, 3])
        
        with col1:
            if user_info.get('picture'):
                st.image(user_info['picture'], width=50)
            else:
                st.markdown("👤")
        
        with col2:
            st.markdown(f"**{user_info.get('name', 'User')}**")
            st.markdown(f"*{user_info.get('email', '')}*")
        
        # User actions
        if st.button("🚪 Sign Out", key="logout_btn"):
            logout()


def show_user_dropdown():
    """Display user dropdown in main header"""
    user_info = get_current_user()
    if not user_info:
        return
    
    # Custom CSS for user dropdown
    st.markdown("""
    <style>
    .user-dropdown {
        position: fixed;
        top: 1rem;
        right: 1rem;
        z-index: 1000;
        background: white;
        border-radius: 25px;
        padding: 0.5rem 1rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
    }
    .user-info {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .user-avatar {
        width: 32px;
        height: 32px;
        border-radius: 50%;
    }
    .user-name {
        font-weight: 500;
        color: #333;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # User dropdown HTML
    avatar_img = f'<img src="{user_info.get("picture", "")}" class="user-avatar">' if user_info.get('picture') else '👤'
    
    st.markdown(f"""
    <div class="user-dropdown">
        <div class="user-info">
            {avatar_img}
            <span class="user-name">{user_info.get('name', 'User')}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def show_auth_status():
    """Show authentication status indicator"""
    if is_authenticated():
        session_info = get_session_info()
        
        if session_info.get('needs_refresh'):
            st.warning("🔄 Refreshing authentication...")
        elif session_info.get('credentials_valid'):
            st.success("✅ Authenticated")
        else:
            st.error("❌ Authentication expired")
    else:
        st.info("🔐 Please sign in to continue")


def show_setup_status():
    """Show setup status for authentication"""
    auth_manager = get_auth_manager()
    
    st.markdown("### 🔧 Setup Status")
    
    # Check credentials file
    if auth_manager.is_credentials_configured():
        st.success("✅ Google OAuth credentials configured")
    else:
        st.error("❌ Google OAuth credentials missing")
        st.info("Download `credentials.json` from Google Cloud Console")
    
    # Check authentication
    if is_authenticated():
        user_info = get_current_user()
        st.success(f"✅ Signed in as {user_info.get('name', 'User')}")
    else:
        st.warning("⏳ Not signed in")


def show_privacy_notice():
    """Show privacy notice on login page"""
    with st.expander("🔒 Privacy & Security"):
        st.markdown("""
        **Your data privacy is our priority:**
        
        - ✅ **Local processing** - Your spreadsheet data is processed locally
        - ✅ **No data storage** - We don't store your sheet contents
        - ✅ **Google security** - Authentication handled by Google's secure system
        - ✅ **Read-only access** - We only request read access to your sheets
        - ✅ **Revocable** - You can revoke access anytime in your Google Account
        
        **What we access:**
        - Your email and name (for personalization)
        - Read-only access to Google Sheets you choose to analyze
        - No access to other Google services or personal data
        
        **Data usage:**
        - Sheet data sent to Claude AI for analysis only
        - No permanent storage of your spreadsheet contents
        - Session data cleared when you sign out
        """)


def show_onboarding_tips():
    """Show helpful tips for new users"""
    st.markdown("### 🎯 Getting Started")
    
    st.info("""
    **Welcome to HolySheet!** Here's how to get divine insights:
    
    1. 📊 **Load a sheet** - Paste any Google Sheets URL
    2. 💬 **Chat with Claude** - Ask questions about your data
    3. ⚡ **Try quick actions** - Use the analysis buttons
    4. 🔍 **Explore insights** - Follow up with specific questions
    """)
    
    with st.expander("💡 Pro Tips"):
        st.markdown("""
        - **Be specific**: "Analyze Q4 spending patterns" vs "analyze this"
        - **Ask follow-ups**: "Can you explain that formula?"
        - **Use quick actions**: Great starting points for analysis
        - **Check data preview**: Make sure Claude sees what you expect
        """)


# Utility functions for authentication flow
def handle_auth_ui():
    """Handle authentication UI flow"""
    if not is_authenticated():
        show_login_page()
        return False
    return True


def setup_authenticated_ui():
    """Setup UI for authenticated users"""
    user_info = get_current_user()
    if user_info:
        show_user_profile(user_info)
        return True
    return False