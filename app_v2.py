#!/usr/bin/env python3
"""
HolySheet - Divine Google Sheets Analysis with Claude AI
Version 2.0 with Google Authentication
Run: streamlit run app_v2.py
"""

import streamlit as st
import anthropic
import pandas as pd
from googleapiclient.discovery import build
import json
import os
import re

# Import our new authentication modules
from auth.google_auth import (
    handle_authentication_flow, 
    is_authenticated, 
    get_current_user, 
    get_credentials,
    logout
)
from auth.session_manager import initialize_session_state, get_session_info
from auth.ui_components import (
    show_login_page, 
    setup_authenticated_ui, 
    show_onboarding_tips,
    show_privacy_notice
)

# Page config
st.set_page_config(
    page_title="HolySheet 🙏",
    page_icon="🙏",
    layout="wide"
)

class HolySheetApp:
    def __init__(self):
        self.claude = None
        self.sheets_service = None
        
    def setup_claude(self, api_key):
        try:
            self.claude = anthropic.Anthropic(api_key=api_key)
            return True
        except Exception as e:
            st.error(f"Claude setup error: {e}")
            return False
    
    def extract_sheet_id(self, url_or_id):
        """Extract sheet ID from URL or return if already ID"""
        if 'docs.google.com/spreadsheets' in url_or_id:
            match = re.search(r'/spreadsheets/d/([a-zA-Z0-9-_]+)', url_or_id)
            return match.group(1) if match else None
        return url_or_id
    
    def read_sheet_data(self, sheet_id, range_name='A1:Z1000'):
        """Read data from Google Sheet"""
        try:
            if not st.session_state.sheets_service:
                st.error("Google Sheets service not available")
                return None, "Google Sheets not connected"
            
            result = st.session_state.sheets_service.spreadsheets().values().get(
                spreadsheetId=sheet_id, range=range_name
            ).execute()
            
            values = result.get('values', [])
            if not values:
                return None, "No data found in sheet"
            
            # Convert to DataFrame for better display
            df = pd.DataFrame(values[1:], columns=values[0] if values else [])
            return df, None
            
        except Exception as e:
            return None, f"Error reading sheet: {str(e)}"
    
    def get_sheet_info(self, sheet_id):
        """Get sheet metadata"""
        try:
            if not st.session_state.sheets_service:
                return 'Unknown Sheet'
            
            sheet = st.session_state.sheets_service.spreadsheets().get(spreadsheetId=sheet_id).execute()
            return sheet.get('properties', {}).get('title', 'Unknown Sheet')
        except:
            return 'Unknown Sheet'
    
    def chat_with_claude(self, message, sheet_data=None, sheet_name=""):
        """Send message to Claude with optional sheet data"""
        try:
            if sheet_data is not None:
                # Limit data size for API
                data_sample = sheet_data.head(50).to_string(index=False)
                prompt = f"""Sheet: "{sheet_name}"
                
Sample data (first 50 rows):
{data_sample}

Total rows: {len(sheet_data)}
Columns: {list(sheet_data.columns)}

User request: {message}

Please provide specific, actionable advice about this financial data. Include exact formulas, cell ranges, or step-by-step instructions where helpful."""
            else:
                prompt = message
            
            response = self.claude.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return response.content[0].text
            
        except Exception as e:
            return f"Error: {str(e)}"


def main():
    # Initialize session state
    initialize_session_state()
    
    # Handle authentication flow
    if not handle_authentication_flow():
        if not is_authenticated():
            show_login_page()
            show_privacy_notice()
            return
    
    # User is authenticated, show main app
    show_main_app()


def show_main_app():
    """Main application interface for authenticated users"""
    
    # Setup authenticated UI
    setup_authenticated_ui()
    
    # App title with user context
    user_info = get_current_user()
    st.title(f"🙏 HolySheet")
    st.write("Divine Google Sheets analysis with Claude AI - Holy Sheet, this is powerful!")
    
    # Initialize app instance
    if 'app' not in st.session_state:
        st.session_state.app = HolySheetApp()
    
    # Initialize other session state
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'current_sheet_data' not in st.session_state:
        st.session_state.current_sheet_data = None
    if 'current_sheet_name' not in st.session_state:
        st.session_state.current_sheet_name = ""
    
    # Setup Google Sheets service from authenticated credentials
    if not st.session_state.sheets_service:
        credentials = get_credentials()
        if credentials:
            try:
                st.session_state.sheets_service = build('sheets', 'v4', credentials=credentials)
            except Exception as e:
                st.error(f"Failed to create Sheets service: {e}")
    
    # Sidebar setup
    with st.sidebar:
        st.header("⚙️ Setup")
        
        # User info
        if user_info:
            st.success(f"✅ Signed in as {user_info.get('name', 'User')}")
            st.info(f"📧 {user_info.get('email', '')}")
        
        # Anthropic API Key
        anthropic_key = st.text_input("Anthropic API Key", type="password", 
                                    help="Get from console.anthropic.com")
        
        if anthropic_key and not st.session_state.app.claude:
            if st.session_state.app.setup_claude(anthropic_key):
                st.success("✅ Claude connected!")
        
        # Google Sheets section
        st.subheader("📊 Google Sheets")
        
        if st.session_state.sheets_service:
            st.success("✅ Google Sheets connected!")
        else:
            st.error("❌ Google Sheets connection failed")
        
        # Sheet input
        if st.session_state.sheets_service:
            st.subheader("📈 Select Sheet")
            
            sheet_input = st.text_input(
                "Sheet URL or ID", 
                placeholder="Paste Google Sheets URL or ID",
                help="Example: https://docs.google.com/spreadsheets/d/1ABC..."
            )
            
            range_input = st.text_input("Range", value="A1:Z1000", 
                                       help="e.g., A1:Z1000 or Sheet1!A1:C100")
            
            if st.button("📥 Load Sheet") and sheet_input:
                sheet_id = st.session_state.app.extract_sheet_id(sheet_input)
                if sheet_id:
                    with st.spinner("Loading sheet data..."):
                        df, error = st.session_state.app.read_sheet_data(sheet_id, range_input)
                        
                        if df is not None:
                            st.session_state.current_sheet_data = df
                            st.session_state.current_sheet_name = st.session_state.app.get_sheet_info(sheet_id)
                            st.success(f"✅ Loaded: {st.session_state.current_sheet_name}")
                            st.write(f"📊 {len(df)} rows, {len(df.columns)} columns")
                        else:
                            st.error(error)
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("💬 Chat with Claude")
        
        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask Claude about your sheet..."):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            with st.chat_message("user"):
                st.write(prompt)
            
            # Get Claude's response
            if st.session_state.app.claude:
                with st.chat_message("assistant"):
                    with st.spinner("Claude is thinking..."):
                        response = st.session_state.app.chat_with_claude(
                            prompt, 
                            st.session_state.current_sheet_data,
                            st.session_state.current_sheet_name
                        )
                        st.write(response)
                        
                        # Add to chat history
                        st.session_state.messages.append({"role": "assistant", "content": response})
            else:
                st.error("Please add your Anthropic API key first!")
    
    with col2:
        st.header("📊 Sheet Preview")
        
        if st.session_state.current_sheet_data is not None:
            st.subheader(f"📈 {st.session_state.current_sheet_name}")
            
            # Show data info
            df = st.session_state.current_sheet_data
            st.write(f"**{len(df)} rows × {len(df.columns)} columns**")
            
            # Show data preview
            st.dataframe(df, use_container_width=True, height=400)
            
            # Quick stats for financial data
            numeric_cols = df.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                st.subheader("📈 Quick Stats")
                for col in numeric_cols[:3]:  # Show stats for first 3 numeric columns
                    if not df[col].empty:
                        st.metric(
                            label=col,
                            value=f"${df[col].sum():,.2f}" if 'amount' in col.lower() or 'cost' in col.lower() or 'price' in col.lower() else f"{df[col].sum():,.2f}",
                            delta=f"Avg: ${df[col].mean():,.2f}" if 'amount' in col.lower() or 'cost' in col.lower() or 'price' in col.lower() else f"Avg: {df[col].mean():.2f}"
                        )
        else:
            st.info("👆 Load a Google Sheet from the sidebar to see data preview")
            show_onboarding_tips()
    
    # Quick action buttons
    if st.session_state.current_sheet_data is not None and st.session_state.app.claude:
        st.header("🚀 Quick Actions")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("📊 Analyze Data"):
                prompt = "Analyze this financial data. What patterns, trends, or insights do you see?"
                st.session_state.messages.append({"role": "user", "content": prompt})
                response = st.session_state.app.chat_with_claude(prompt, st.session_state.current_sheet_data, st.session_state.current_sheet_name)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()
        
        with col2:
            if st.button("🧹 Clean Data"):
                prompt = "Help me clean up this data. Identify duplicates, formatting issues, missing values, or inconsistencies."
                st.session_state.messages.append({"role": "user", "content": prompt})
                response = st.session_state.app.chat_with_claude(prompt, st.session_state.current_sheet_data, st.session_state.current_sheet_name)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()
        
        with col3:
            if st.button("📈 Find Trends"):
                prompt = "What financial trends can you identify in this data over time? Any concerning patterns or opportunities?"
                st.session_state.messages.append({"role": "user", "content": prompt})
                response = st.session_state.app.chat_with_claude(prompt, st.session_state.current_sheet_data, st.session_state.current_sheet_name)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()
        
        with col4:
            if st.button("🔧 Suggest Formulas"):
                prompt = "Suggest useful Excel/Google Sheets formulas for this financial data. Include specific cell references."
                st.session_state.messages.append({"role": "user", "content": prompt})
                response = st.session_state.app.chat_with_claude(prompt, st.session_state.current_sheet_data, st.session_state.current_sheet_name)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()


if __name__ == "__main__":
    main()