#!/usr/bin/env python3
"""
HolySheet - Divine Google Sheets Analysis with Claude AI
A local web interface to analyze Google Sheets with Claude
Run: streamlit run app.py
"""

import streamlit as st
import anthropic
import pandas as pd
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
import json
import os
import re

# Page config
st.set_page_config(
    page_title="HolySheet 🙏",
    page_icon="🙏",
    layout="wide"
)

# Divine Holy Styling - Warm Anthropic-inspired colors
st.markdown("""
<style>
    /* Import fonts for divine typography */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Holy color palette inspired by Anthropic */
    :root {
        --holy-cream: #faf8f5;
        --holy-beige: #f5f2ed;
        --holy-warm-white: #ffffff;
        --holy-text-dark: #2d3748;
        --holy-text-medium: #4a5568;
        --holy-text-light: #718096;
        --holy-accent: #cc785c;
        --holy-accent-light: rgba(204, 120, 92, 0.1);
        --holy-accent-medium: rgba(204, 120, 92, 0.3);
        --holy-border: #e2d8d0;
        --holy-shadow: rgba(204, 120, 92, 0.08);
        --holy-success: #48bb78;
        --holy-warning: #ed8936;
        --holy-error: #f56565;
    }
    
    /* Main app background - sacred parchment */
    .stApp {
        background: linear-gradient(135deg, var(--holy-cream) 0%, var(--holy-beige) 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Header styling - divine title */
    .main h1 {
        color: var(--holy-text-dark) !important;
        font-weight: 700 !important;
        font-size: 3.5rem !important;
        margin-bottom: 0.5rem !important;
        text-shadow: 0 2px 4px var(--holy-shadow);
        letter-spacing: -0.02em;
    }
    
    /* Subtitle and descriptions */
    .main h2 {
        color: var(--holy-text-medium) !important;
        font-weight: 600 !important;
        font-size: 2rem !important;
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
    }
    
    .main h3 {
        color: var(--holy-text-medium) !important;
        font-weight: 600 !important;
        font-size: 1.5rem !important;
    }
    
    /* Body text - sacred scrolls - ENSURE ALL TEXT IS VISIBLE */
    .main p, .main div, p, div, span, label {
        color: var(--holy-text-dark) !important;
        font-size: 1.1rem !important;
        line-height: 1.6 !important;
    }
    
    /* Force all text to be dark and visible */
    * {
        color: var(--holy-text-dark) !important;
    }
    
    /* Sidebar - holy sanctuary */
    .css-1d391kg, .stSidebar {
        background: var(--holy-warm-white) !important;
        border-right: 2px solid var(--holy-border) !important;
        box-shadow: 4px 0 12px var(--holy-shadow) !important;
    }
    
    /* All sidebar text should be visible */
    .stSidebar *, .sidebar *, .css-1d391kg * {
        color: var(--holy-text-dark) !important;
    }
    
    .sidebar .stSelectbox label,
    .sidebar .stTextInput label,
    .sidebar .stTextArea label,
    .stSidebar label {
        color: var(--holy-text-dark) !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
    }
    
    /* Input fields - divine interface */
    .stTextInput input,
    .stTextArea textarea,
    .stSelectbox select {
        background: var(--holy-warm-white) !important;
        border: 2px solid var(--holy-border) !important;
        border-radius: 8px !important;
        color: var(--holy-text-dark) !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput input:focus,
    .stTextArea textarea:focus {
        border-color: var(--holy-accent) !important;
        box-shadow: 0 0 0 3px var(--holy-accent-light) !important;
    }
    
    /* Buttons - sacred actions */
    .stButton button {
        background: linear-gradient(135deg, var(--holy-accent) 0%, #b86650 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 8px var(--holy-shadow) !important;
    }
    
    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 16px var(--holy-accent-medium) !important;
    }
    
    /* Chat interface - divine conversation */
    .stChatMessage {
        background: var(--holy-warm-white) !important;
        border: 1px solid var(--holy-border) !important;
        border-radius: 12px !important;
        margin: 1rem 0 !important;
        box-shadow: 0 2px 8px var(--holy-shadow) !important;
    }
    
    /* Data frames - sacred tables */
    .dataframe {
        background: var(--holy-warm-white) !important;
        border-radius: 8px !important;
        overflow: hidden !important;
        box-shadow: 0 2px 12px var(--holy-shadow) !important;
    }
    
    /* Remove problematic background styling - keep it simple */
    
    /* Metrics - divine statistics */
    .metric-container {
        background: var(--holy-warm-white) !important;
        border: 1px solid var(--holy-border) !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        box-shadow: 0 2px 8px var(--holy-shadow) !important;
    }
    
    /* Expander - sacred scrolls */
    .streamlit-expanderHeader {
        background: var(--holy-beige) !important;
        border: 1px solid var(--holy-border) !important;
        border-radius: 8px !important;
        color: var(--holy-text-dark) !important;
        font-weight: 600 !important;
    }
    
    /* File uploader - sacred offerings */
    .stFileUploader {
        background: var(--holy-warm-white) !important;
        border: 2px dashed var(--holy-border) !important;
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
    }
    
    .stFileUploader:hover {
        border-color: var(--holy-accent) !important;
        background: var(--holy-accent-light) !important;
    }
    
    /* Column separators - divine divisions */
    .element-container {
        margin: 0.5rem 0 !important;
    }
    
    /* Loading spinner - holy meditation */
    .stSpinner {
        color: var(--holy-accent) !important;
    }
    
    /* Links - sacred connections */
    a {
        color: var(--holy-accent) !important;
        text-decoration: none !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }
    
    a:hover {
        color: #b86650 !important;
        text-decoration: underline !important;
    }
    
    /* Custom holy glow effect for important elements */
    .holy-glow {
        box-shadow: 0 0 20px var(--holy-accent-light) !important;
        border: 2px solid var(--holy-accent) !important;
    }
    
    /* Responsive typography scaling */
    @media (max-width: 768px) {
        .main h1 {
            font-size: 2.5rem !important;
        }
        .main h2 {
            font-size: 1.75rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

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
            
    def setup_google_auth(self, credentials_file):
        try:
            scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly']
            
            if os.path.exists('token.json'):
                creds = Credentials.from_authorized_user_file('token.json', scopes)
            else:
                flow = Flow.from_client_secrets_file(credentials_file, scopes)
                flow.redirect_uri = 'http://localhost:8501'
                
                auth_url, _ = flow.authorization_url(prompt='consent')
                
                st.write("🔐 **Google Authentication Required**")
                st.write("1. Click this link to authorize:")
                st.markdown(f"[**Authorize Google Sheets Access**]({auth_url})")
                st.write("2. Copy the code from the URL after authorization")
                
                auth_code = st.text_input("Enter authorization code:")
                
                if auth_code:
                    try:
                        flow.fetch_token(code=auth_code)
                        creds = flow.credentials
                        
                        with open('token.json', 'w') as token:
                            token.write(creds.to_json())
                        
                        st.success("✅ Google Sheets connected!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Auth error: {e}")
                        return False
                        
                return False
            
            self.sheets_service = build('sheets', 'v4', credentials=creds)
            return True
            
        except Exception as e:
            st.error(f"Google setup error: {e}")
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
            result = self.sheets_service.spreadsheets().values().get(
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
            sheet = self.sheets_service.spreadsheets().get(spreadsheetId=sheet_id).execute()
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
    st.title("🙏 HolySheet")
    st.write("Divine Google Sheets analysis with Claude AI - Holy Sheet, this is powerful!")
    
    # Initialize session state
    if 'app' not in st.session_state:
        st.session_state.app = HolySheetApp()
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'current_sheet_data' not in st.session_state:
        st.session_state.current_sheet_data = None
    if 'current_sheet_name' not in st.session_state:
        st.session_state.current_sheet_name = ""
    
    # Sidebar setup
    with st.sidebar:
        st.header("⚙️ Setup")
        
        # Anthropic API Key
        anthropic_key = st.text_input("Anthropic API Key", type="password", 
                                    help="Get from console.anthropic.com")
        
        if anthropic_key and not st.session_state.app.claude:
            if st.session_state.app.setup_claude(anthropic_key):
                st.success("✅ Claude connected!")
        
        # Google Sheets setup
        st.subheader("📊 Google Sheets")
        
        if not os.path.exists('credentials.json'):
            st.warning("📋 **Setup Required:**")
            st.write("1. Go to [Google Cloud Console](https://console.cloud.google.com)")
            st.write("2. Enable Google Sheets API")
            st.write("3. Create OAuth 2.0 credentials")
            st.write("4. Download as `credentials.json`")
            
            uploaded_file = st.file_uploader("Upload credentials.json", type="json")
            if uploaded_file:
                with open("credentials.json", "wb") as f:
                    f.write(uploaded_file.getvalue())
                st.success("Credentials saved! Restart the app.")
        else:
            if not st.session_state.app.sheets_service:
                if st.button("🔗 Connect Google Sheets"):
                    st.session_state.app.setup_google_auth('credentials.json')
            else:
                st.success("✅ Google Sheets connected!")
        
        # Sheet input
        if st.session_state.app.sheets_service:
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