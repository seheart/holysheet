// Google Apps Script + Claude
// Paste this in Google Apps Script (script.google.com)
// Creates a custom menu in your Google Sheet to chat with Claude

function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('Claude Assistant')
    .addItem('Chat with Claude', 'openClaudeDialog')
    .addItem('Analyze Data', 'analyzeCurrentData')
    .addItem('Clean Data', 'cleanCurrentData')
    .addToUi();
}

function openClaudeDialog() {
  const html = HtmlService.createHtmlOutputFromFile('claude_dialog')
    .setWidth(600)
    .setHeight(400);
  SpreadsheetApp.getUi().showModalDialog(html, 'Chat with Claude');
}

function askClaude(message, includeData = true) {
  const ANTHROPIC_API_KEY = 'your-api-key-here'; // Store in Script Properties instead
  
  let prompt = message;
  
  if (includeData) {
    const sheet = SpreadsheetApp.getActiveSheet();
    const data = sheet.getDataRange().getValues();
    prompt = `Current sheet data:\n${JSON.stringify(data)}\n\nRequest: ${message}`;
  }
  
  const payload = {
    model: "claude-3-5-sonnet-20241022",
    max_tokens: 1500,
    messages: [{
      role: "user", 
      content: `You are a Google Sheets assistant. Current sheet: "${SpreadsheetApp.getActiveSheet().getName()}"
      
      ${prompt}
      
      Provide actionable suggestions and if needed, specific cell ranges and formulas to update.`
    }]
  };
  
  const options = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': ANTHROPIC_API_KEY,
      'anthropic-version': '2023-06-01'
    },
    payload: JSON.stringify(payload)
  };
  
  try {
    const response = UrlFetchApp.fetch('https://api.anthropic.com/v1/messages', options);
    const data = JSON.parse(response.getContentText());
    return data.content[0].text;
  } catch (error) {
    return `Error: ${error.toString()}`;
  }
}

function analyzeCurrentData() {
  const response = askClaude("Analyze this data and suggest improvements, cleanup, or insights.");
  SpreadsheetApp.getUi().alert('Claude\'s Analysis', response, SpreadsheetApp.getUi().ButtonSet.OK);
}

function cleanCurrentData() {
  const response = askClaude("Please suggest specific changes to clean up this data. Include exact cell ranges and formulas if needed.");
  SpreadsheetApp.getUi().alert('Claude\'s Cleanup Suggestions', response, SpreadsheetApp.getUi().ButtonSet.OK);
}