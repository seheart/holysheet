#!/usr/bin/env python3
"""
HolySheet - FastAPI + Tailwind CSS Version
Clean, fast, real-time Google Sheets analysis with Claude AI
"""

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import json
import asyncio
from typing import List
import uvicorn

# Import our existing backend logic
import anthropic
import pandas as pd
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
import os
import re

app = FastAPI(title="HolySheet", description="Divine Google Sheets Analysis")

# Setup templates and static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# WebSocket connection manager for real-time updates
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

# Our existing HolySheet logic (converted to async)
class HolySheetAPI:
    def __init__(self):
        self.claude = None
        self.sheets_service = None
        
    def setup_claude(self, api_key: str):
        try:
            self.claude = anthropic.Anthropic(api_key=api_key)
            return True
        except Exception as e:
            return False
            
    def extract_sheet_id(self, url_or_id: str):
        if 'docs.google.com/spreadsheets' in url_or_id:
            match = re.search(r'/spreadsheets/d/([a-zA-Z0-9-_]+)', url_or_id)
            return match.group(1) if match else None
        return url_or_id
    
    def read_sheet_data(self, sheet_id: str, range_name: str = 'A1:Z1000'):
        try:
            if not self.sheets_service:
                return None, "Google Sheets not connected"
            
            result = self.sheets_service.spreadsheets().values().get(
                spreadsheetId=sheet_id, range=range_name
            ).execute()
            
            values = result.get('values', [])
            if not values:
                return None, "No data found in sheet"
            
            df = pd.DataFrame(values[1:], columns=values[0] if values else [])
            return df, None
            
        except Exception as e:
            return None, f"Error reading sheet: {str(e)}"
    
    async def chat_with_claude(self, message: str, sheet_data=None, sheet_name=""):
        try:
            if sheet_data is not None:
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

# Global instance
holysheet_api = HolySheetAPI()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/profile", response_class=HTMLResponse)
async def profile(request: Request):
    return templates.TemplateResponse("profile.html", {"request": request})

@app.get("/account", response_class=HTMLResponse)
async def account(request: Request):
    return templates.TemplateResponse("account.html", {"request": request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Handle different message types
            if message_data["type"] == "chat":
                response = await holysheet_api.chat_with_claude(
                    message_data["message"],
                    # Add sheet data if available
                )
                await manager.send_personal_message(json.dumps({
                    "type": "chat_response",
                    "message": response
                }), websocket)
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
