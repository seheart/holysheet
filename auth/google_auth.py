"""
Google Authentication Module for HolySheet
Handles Google OAuth flow and credential management
"""

import streamlit as st
import json
import os
from typing import Optional, Dict, Any
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import base64
import secrets


# Google OAuth scopes - requesting minimal necessary permissions
SCOPES = [
    'openid',
    'email', 
    'profile',
    'https://www.googleapis.com/auth/spreadsheets.readonly'
]

# OAuth configuration
REDIRECT_URI = "http://localhost:8501"


class GoogleAuthManager:
    """Manages Google OAuth authentication for HolySheet"""
    
    def __init__(self):
        self.credentials_file = 'credentials.json'
        
    def is_credentials_configured(self) -> bool:
        """Check if Google OAuth credentials file exists"""
        return os.path.exists(self.credentials_file)
    
    def generate_auth_url(self) -> str:
        """Generate Google OAuth authorization URL"""
        if not self.is_credentials_configured():
            raise FileNotFoundError("credentials.json not found. Please download from Google Cloud Console.")
        
        # Create OAuth flow
        flow = Flow.from_client_secrets_file(
            self.credentials_file,
            scopes=SCOPES,
            redirect_uri=REDIRECT_URI
        )
        
        # Generate state parameter for security
        state = secrets.token_urlsafe(32)
        st.session_state['oauth_state'] = state
        
        authorization_url, _ = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            state=state,
            prompt='consent'  # Force consent to get refresh token
        )
        
        return authorization_url
    
    def handle_oauth_callback(self, authorization_response: str) -> Optional[Credentials]:
        """Handle OAuth callback and exchange code for credentials"""
        try:
            flow = Flow.from_client_secrets_file(
                self.credentials_file,
                scopes=SCOPES,
                redirect_uri=REDIRECT_URI
            )
            
            # Fetch token
            flow.fetch_token(authorization_response=authorization_response)
            credentials = flow.credentials
            
            return credentials
            
        except Exception as e:
            st.error(f"Authentication failed: {str(e)}")
            return None
    
    def get_user_info(self, credentials: Credentials) -> Dict[str, Any]:
        """Get user profile information from Google"""
        try:
            # Build OAuth2 service
            service = build('oauth2', 'v2', credentials=credentials)
            user_info = service.userinfo().get().execute()
            
            return {
                'id': user_info.get('id'),
                'email': user_info.get('email'),
                'name': user_info.get('name'),
                'picture': user_info.get('picture'),
                'verified_email': user_info.get('verified_email', False)
            }
            
        except Exception as e:
            st.error(f"Failed to get user info: {str(e)}")
            return {}
    
    def refresh_credentials(self, credentials: Credentials) -> Credentials:
        """Refresh expired credentials"""
        try:
            credentials.refresh(Request())
            return credentials
        except Exception as e:
            st.error(f"Failed to refresh credentials: {str(e)}")
            return None
    
    def create_sheets_service(self, credentials: Credentials):
        """Create authenticated Google Sheets service"""
        try:
            return build('sheets', 'v4', credentials=credentials)
        except Exception as e:
            st.error(f"Failed to create Sheets service: {str(e)}")
            return None
    
    def revoke_credentials(self, credentials: Credentials) -> bool:
        """Revoke user credentials"""
        try:
            credentials.revoke(Request())
            return True
        except Exception as e:
            st.error(f"Failed to revoke credentials: {str(e)}")
            return False


# Convenience functions for Streamlit app
def get_auth_manager() -> GoogleAuthManager:
    """Get or create GoogleAuthManager instance"""
    if 'auth_manager' not in st.session_state:
        st.session_state.auth_manager = GoogleAuthManager()
    return st.session_state.auth_manager


def is_authenticated() -> bool:
    """Check if user is currently authenticated"""
    return (
        'google_credentials' in st.session_state and 
        st.session_state.google_credentials is not None and
        'user_info' in st.session_state and
        st.session_state.user_info is not None
    )


def get_current_user() -> Optional[Dict[str, Any]]:
    """Get current authenticated user info"""
    if is_authenticated():
        return st.session_state.user_info
    return None


def get_credentials() -> Optional[Credentials]:
    """Get current user credentials"""
    if is_authenticated():
        return st.session_state.google_credentials
    return None


def logout():
    """Log out current user and clear session"""
    # Revoke credentials if possible
    if 'google_credentials' in st.session_state:
        auth_manager = get_auth_manager()
        auth_manager.revoke_credentials(st.session_state.google_credentials)
    
    # Clear session state
    keys_to_clear = [
        'google_credentials',
        'user_info', 
        'sheets_service',
        'oauth_state',
        'current_sheet_data',
        'current_sheet_name',
        'messages'
    ]
    
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]
    
    st.rerun()


def handle_authentication_flow():
    """Handle the complete authentication flow"""
    auth_manager = get_auth_manager()
    
    # Check if we have credentials and they're valid
    if is_authenticated():
        # Check if credentials need refresh
        credentials = get_credentials()
        if credentials and credentials.expired and credentials.refresh_token:
            try:
                refreshed_creds = auth_manager.refresh_credentials(credentials)
                if refreshed_creds:
                    st.session_state.google_credentials = refreshed_creds
                else:
                    # Refresh failed, need to re-authenticate
                    logout()
                    return False
            except Exception:
                logout()
                return False
        return True
    
    # Check for OAuth callback in URL parameters
    query_params = st.query_params
    
    if 'code' in query_params:
        # Handle OAuth callback
        authorization_code = query_params['code']
        state = query_params.get('state')
        
        # Verify state parameter for security
        if state != st.session_state.get('oauth_state'):
            st.error("Invalid authentication state. Please try again.")
            return False
        
        # Exchange code for credentials
        authorization_response = f"{REDIRECT_URI}?code={authorization_code}&state={state}"
        credentials = auth_manager.handle_oauth_callback(authorization_response)
        
        if credentials:
            # Get user info
            user_info = auth_manager.get_user_info(credentials)
            
            if user_info:
                # Store in session
                st.session_state.google_credentials = credentials
                st.session_state.user_info = user_info
                st.session_state.sheets_service = auth_manager.create_sheets_service(credentials)
                
                # Clear query parameters and redirect
                st.query_params.clear()
                st.success(f"Welcome, {user_info.get('name', 'User')}!")
                st.rerun()
            else:
                st.error("Failed to get user information.")
                return False
        else:
            st.error("Authentication failed. Please try again.")
            return False
    
    return False