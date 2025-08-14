#!/usr/bin/env python3
"""
Claude + Google Sheets Assistant
A local web app that lets you chat with Claude and execute sheet actions

Requirements:
pip install streamlit anthropic google-api-python-client google-auth-oauthlib pandas
"""

import streamlit as st
import anthropic
import pandas as pd
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
import json
import os

class ClaudeSheetsAssistant:
    def __init__(self):
        self.claude = None
        self.sheets_service = None
        
    def setup_claude(self, api_key):
        self.claude = anthropic.Anthropic(api_key=api_key)
        
    def setup_google_auth(self):
        """Setup Google Sheets authentication"""
        # You'll need credentials.json from Google Cloud Console
        scopes = ['https://www.googleapis.com/auth/spreadsheets']
        
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', scopes)
        else:
            flow = Flow.from_client_secrets_file('credentials.json', scopes)
            flow.redirect_uri = 'http://localhost:8080/callback'
            
            auth_url, _ = flow.authorization_url(prompt='consent')
            st.write(f"Please visit this URL to authorize: {auth_url}")
            
            # In a real app, you'd handle the callback
            # For now, user would paste the code
            code = st.text_input("Enter authorization code:")
            if code:
                flow.fetch_token(code=code)
                creds = flow.credentials
                
                with open('token.json', 'w') as token:
                    token.write(creds.to_json())
        
        self.sheets_service = build('sheets', 'v4', credentials=creds)
        
    def read_sheet(self, sheet_id, range_name):
        """Read data from Google Sheet"""
        result = self.sheets_service.spreadsheets().values().get(
            spreadsheetId=sheet_id, range=range_name
        ).execute()
        return result.get('values', [])
        
    def write_sheet(self, sheet_id, range_name, values):
        """Write data to Google Sheet"""
        body = {'values': values}
        result = self.sheets_service.spreadsheets().values().update(
            spreadsheetId=sheet_id, range=range_name,
            valueInputOption='RAW', body=body
        ).execute()
        return result
        
    def clear_sheet(self, sheet_id, range_name):
        """Clear a range in Google Sheet"""
        result = self.sheets_service.spreadsheets().values().clear(
            spreadsheetId=sheet_id, range=range_name
        ).execute()
        return result
        
    def chat_with_claude(self, message, sheet_data=None):
        """Chat with Claude about the sheet data"""
        
        system_prompt = """You are a Google Sheets assistant. You can:
        1. Analyze spreadsheet data
        2. Suggest improvements and cleanup
        3. Generate formulas
        4. Provide data insights
        5. Help organize and structure data
        
        When the user asks you to make changes, provide:
        1. A clear explanation of what you'll do
        2. The exact data/formulas to write
        3. Which range to update
        
        Format responses for Google Sheets actions as:
        ACTION: READ|WRITE|CLEAR|FORMULA
        RANGE: A1:C10
        DATA: [[row1], [row2], ...]
        EXPLANATION: What this does
        """
        
        if sheet_data:
            message = f"Current sheet data:\n{sheet_data}\n\nUser request: {message}"
            
        response = self.claude.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            system=system_prompt,
            messages=[{"role": "user", "content": message}]
        )
        
        return response.content[0].text

def main():
    st.title("🤖 Claude Sheets Assistant")
    st.write("Chat with Claude to clean up and organize your Google Sheets!")
    
    # Initialize session state
    if 'assistant' not in st.session_state:
        st.session_state.assistant = ClaudeSheetsAssistant()
    
    # Sidebar for setup
    with st.sidebar:
        st.header("Setup")
        
        # Anthropic API Key
        anthropic_key = st.text_input("Anthropic API Key", type="password")
        if anthropic_key:
            st.session_state.assistant.setup_claude(anthropic_key)
            st.success("Claude connected!")
        
        # Google Sheets setup
        st.write("Google Sheets Setup:")
        st.write("1. Enable Google Sheets API in Google Cloud Console")
        st.write("2. Download credentials.json")
        st.write("3. Place in same folder as this script")
        
        if st.button("Connect Google Sheets"):
            try:
                st.session_state.assistant.setup_google_auth()
                st.success("Google Sheets connected!")
            except Exception as e:
                st.error(f"Error: {e}")
        
        # Sheet ID input
        sheet_id = st.text_input("Google Sheet ID")
        range_name = st.text_input("Range (e.g., A1:Z100)", value="A1:Z100")
    
    # Main chat interface
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    if prompt := st.chat_input("What would you like to do with your sheet?"):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        
        # Get sheet data if available
        sheet_data = None
        if sheet_id and st.session_state.assistant.sheets_service:
            try:
                sheet_data = st.session_state.assistant.read_sheet(sheet_id, range_name)
            except Exception as e:
                st.error(f"Error reading sheet: {e}")
        
        # Get Claude's response
        if st.session_state.assistant.claude:
            try:
                response = st.session_state.assistant.chat_with_claude(prompt, sheet_data)
                
                # Add Claude's response
                st.session_state.messages.append({"role": "assistant", "content": response})
                with st.chat_message("assistant"):
                    st.write(response)
                    
                    # Check if Claude wants to execute an action
                    if "ACTION:" in response and sheet_id:
                        if st.button("Execute this action"):
                            # Parse and execute the action
                            # (You'd implement action parsing here)
                            st.success("Action executed!")
                
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.error("Please add your Anthropic API key first!")

if __name__ == "__main__":
    main()