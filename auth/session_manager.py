"""
Session Management for HolySheet
Handles user session persistence and state management
"""

import streamlit as st
import json
import os
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials


class SessionManager:
    """Manages user session state and persistence"""
    
    def __init__(self):
        self.session_file = '.holysheet_session'
        
    def save_session(self, user_info: Dict[str, Any], credentials: Credentials):
        """Save user session for persistence across browser restarts"""
        try:
            session_data = {
                'user_info': user_info,
                'credentials': {
                    'token': credentials.token,
                    'refresh_token': credentials.refresh_token,
                    'token_uri': credentials.token_uri,
                    'client_id': credentials.client_id,
                    'client_secret': credentials.client_secret,
                    'scopes': credentials.scopes,
                    'expiry': credentials.expiry.isoformat() if credentials.expiry else None
                },
                'saved_at': datetime.now().isoformat()
            }
            
            # Save to session state
            st.session_state.google_credentials = credentials
            st.session_state.user_info = user_info
            
            # Optionally save to file for persistence (be careful with credentials)
            # This is commented out for security - credentials should not be saved to disk
            # with open(self.session_file, 'w') as f:
            #     json.dump(session_data, f)
            
        except Exception as e:
            st.error(f"Failed to save session: {str(e)}")
    
    def load_session(self) -> bool:
        """Load saved session if available"""
        try:
            # For now, we rely on Streamlit's session state
            # In production, you might want to implement secure session storage
            return (
                'google_credentials' in st.session_state and
                'user_info' in st.session_state
            )
            
        except Exception:
            return False
    
    def clear_session(self):
        """Clear all session data"""
        # Remove session file if it exists
        if os.path.exists(self.session_file):
            try:
                os.remove(self.session_file)
            except Exception:
                pass
        
        # Clear Streamlit session state
        session_keys = [
            'google_credentials',
            'user_info',
            'sheets_service',
            'oauth_state',
            'current_sheet_data',
            'current_sheet_name',
            'messages',
            'app'
        ]
        
        for key in session_keys:
            if key in st.session_state:
                del st.session_state[key]
    
    def is_session_valid(self) -> bool:
        """Check if current session is valid"""
        if not self.load_session():
            return False
        
        # Check if credentials exist and are not expired
        if 'google_credentials' not in st.session_state:
            return False
        
        credentials = st.session_state.google_credentials
        if credentials and credentials.expired:
            # If expired but has refresh token, it can be refreshed
            return credentials.refresh_token is not None
        
        return True
    
    def get_session_info(self) -> Dict[str, Any]:
        """Get information about current session"""
        if not self.is_session_valid():
            return {}
        
        user_info = st.session_state.get('user_info', {})
        credentials = st.session_state.get('google_credentials')
        
        return {
            'user_id': user_info.get('id'),
            'email': user_info.get('email'),
            'name': user_info.get('name'),
            'authenticated': True,
            'credentials_valid': credentials and not credentials.expired,
            'needs_refresh': credentials and credentials.expired and credentials.refresh_token
        }


# Convenience functions
def get_session_manager() -> SessionManager:
    """Get or create SessionManager instance"""
    if 'session_manager' not in st.session_state:
        st.session_state.session_manager = SessionManager()
    return st.session_state.session_manager


def save_user_session(user_info: Dict[str, Any], credentials: Credentials):
    """Save current user session"""
    session_manager = get_session_manager()
    session_manager.save_session(user_info, credentials)


def is_session_valid() -> bool:
    """Check if current session is valid"""
    session_manager = get_session_manager()
    return session_manager.is_session_valid()


def clear_user_session():
    """Clear current user session"""
    session_manager = get_session_manager()
    session_manager.clear_session()


def get_session_info() -> Dict[str, Any]:
    """Get current session information"""
    session_manager = get_session_manager()
    return session_manager.get_session_info()


def initialize_session_state():
    """Initialize session state with default values"""
    defaults = {
        'messages': [],
        'current_sheet_data': None,
        'current_sheet_name': "",
        'google_credentials': None,
        'user_info': None,
        'sheets_service': None,
        'app': None
    }
    
    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value