// Secure version - stores API key in Script Properties
// Paste this in Google Apps Script instead

function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('🤖 Claude Assistant')
    .addItem('💬 Chat with Claude', 'openClaudeDialog')
    .addItem('📊 Analyze This Sheet', 'analyzeCurrentData')
    .addItem('🧹 Clean Up Data', 'cleanCurrentData')
    .addItem('⚙️ Setup API Key', 'setupApiKey')
    .addToUi();
}

function setupApiKey() {
  const ui = SpreadsheetApp.getUi();
  const result = ui.prompt(
    'Setup API Key',
    'Enter your Anthropic API key (starts with sk-ant-):',
    ui.ButtonSet.OK_CANCEL
  );
  
  if (result.getSelectedButton() == ui.Button.OK) {
    const apiKey = result.getResponseText();
    if (apiKey.startsWith('sk-ant-')) {
      PropertiesService.getScriptProperties().setProperty('ANTHROPIC_API_KEY', apiKey);
      ui.alert('Success!', 'API key saved securely.', ui.ButtonSet.OK);
    } else {
      ui.alert('Error', 'Invalid API key. Should start with sk-ant-', ui.ButtonSet.OK);
    }
  }
}

function askClaude(message, includeData = true) {
  const apiKey = PropertiesService.getScriptProperties().getProperty('ANTHROPIC_API_KEY');
  
  if (!apiKey) {
    SpreadsheetApp.getUi().alert('Setup Required', 'Please set up your API key first using the menu.', SpreadsheetApp.getUi().ButtonSet.OK);
    return 'Please set up your API key first.';
  }
  
  let prompt = message;
  
  if (includeData) {
    const sheet = SpreadsheetApp.getActiveSheet();
    const data = sheet.getDataRange().getValues();
    const sheetName = sheet.getName();
    
    // Limit data size to avoid API limits
    const maxRows = 100;
    const limitedData = data.slice(0, maxRows);
    
    prompt = `Current Google Sheet: "${sheetName}"
Data (first ${maxRows} rows):
${JSON.stringify(limitedData)}

User request: ${message}

Please provide actionable suggestions. If you recommend changes, specify:
- Exact cell ranges (like A1:C10)
- Formulas to use
- Step-by-step instructions`;
  }
  
  const payload = {
    model: "claude-3-5-sonnet-20241022",
    max_tokens: 2000,
    messages: [{
      role: "user", 
      content: prompt
    }]
  };
  
  const options = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': apiKey,
      'anthropic-version': '2023-06-01'
    },
    payload: JSON.stringify(payload)
  };
  
  try {
    const response = UrlFetchApp.fetch('https://api.anthropic.com/v1/messages', options);
    const data = JSON.parse(response.getContentText());
    
    if (data.error) {
      return `API Error: ${data.error.message}`;
    }
    
    return data.content[0].text;
    
  } catch (error) {
    return `Error: ${error.toString()}`;
  }
}

function analyzeCurrentData() {
  const response = askClaude("Analyze this spreadsheet data. What insights, patterns, or issues do you see? Suggest specific improvements.");
  
  const ui = SpreadsheetApp.getUi();
  ui.alert('📊 Claude\'s Analysis', response, ui.ButtonSet.OK);
}

function cleanCurrentData() {
  const response = askClaude("Help me clean up this data. Identify issues like duplicates, formatting problems, missing values, or inconsistencies. Provide specific instructions to fix them.");
  
  const ui = SpreadsheetApp.getUi();
  ui.alert('🧹 Cleanup Suggestions', response, ui.ButtonSet.OK);
}

function openClaudeDialog() {
  const html = `
    <div style="padding: 20px; font-family: Arial, sans-serif;">
      <h3>💬 Chat with Claude</h3>
      <p>Ask Claude anything about your spreadsheet:</p>
      <textarea id="userInput" style="width: 100%; height: 100px; margin: 10px 0; padding: 8px;" 
                placeholder="Example: Help me organize this data better, or create a summary of sales by month"></textarea>
      <button onclick="askClaudeCustom()" style="background: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer;">
        Ask Claude
      </button>
      <div id="response" style="margin-top: 20px; padding: 10px; background: #f5f5f5; border-radius: 4px; max-height: 300px; overflow-y: auto;">
        Response will appear here...
      </div>
    </div>
    
    <script>
      function askClaudeCustom() {
        const input = document.getElementById('userInput').value;
        const responseDiv = document.getElementById('response');
        
        if (!input.trim()) {
          responseDiv.innerHTML = 'Please enter a question first.';
          return;
        }
        
        responseDiv.innerHTML = 'Thinking... 🤔';
        
        google.script.run
          .withSuccessHandler(function(result) {
            responseDiv.innerHTML = result.replace(/\\n/g, '<br>');
          })
          .withFailureHandler(function(error) {
            responseDiv.innerHTML = 'Error: ' + error;
          })
          .askClaude(input);
      }
    </script>
  `;
  
  const htmlOutput = HtmlService.createHtmlOutput(html)
    .setWidth(600)
    .setHeight(500);
  
  SpreadsheetApp.getUi().showModalDialog(htmlOutput, '🤖 Claude Assistant');
}