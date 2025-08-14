// CORRECTED Google Apps Script + Claude
// Paste this in Google Apps Script (script.google.com)

function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('🤖 Claude Assistant')
    .addItem('💬 Chat with Claude', 'openClaudeDialog')
    .addItem('📊 Analyze Data', 'analyzeCurrentData')
    .addItem('🧹 Clean Data', 'cleanCurrentData')
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
      ui.alert('Error', 'Invalid API key format.', ui.ButtonSet.OK);
    }
  }
}

function askClaude(message, includeData = true) {
  // Get API key from secure storage
  const apiKey = PropertiesService.getScriptProperties().getProperty('ANTHROPIC_API_KEY');
  
  if (!apiKey) {
    SpreadsheetApp.getUi().alert('Setup Required', 'Please set up your API key first using the menu.', SpreadsheetApp.getUi().ButtonSet.OK);
    return 'Please set up your API key first.';
  }

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
      'x-api-key': apiKey,
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

function openClaudeDialog() {
  const html = `
    <div style="padding: 20px; font-family: Arial, sans-serif;">
      <h3>💬 Chat with Claude</h3>
      <p>Ask Claude about your spreadsheet:</p>
      <textarea id="userInput" style="width: 100%; height: 100px; margin: 10px 0; padding: 8px;" 
                placeholder="Example: Help me organize this data, create formulas, find patterns..."></textarea>
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