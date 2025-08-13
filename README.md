# Claude Sheets Assistant

A local web application for analyzing Google Sheets with Claude AI. Perfect for financial data analysis and cleanup.

## Features

- 🤖 **Chat with Claude** about your spreadsheet data
- 📊 **Side-by-side view** - see your data while getting analysis
- 🧹 **Data cleanup** suggestions and automation
- 📈 **Financial analysis** optimized for multi-year data
- 🔐 **Local and secure** - your data stays on your machine
- ⚡ **Quick actions** - analyze, clean, find trends, suggest formulas

## Screenshots

[Add screenshots here]

## Setup

### Prerequisites

- Python 3.8+
- Google Cloud Project with Sheets API enabled
- Anthropic API key

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/claude-sheets-assistant.git
   cd claude-sheets-assistant
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Google Cloud Setup**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing
   - Enable Google Sheets API
   - Create OAuth 2.0 Client ID (Desktop application)
   - Download credentials as `credentials.json` in project root

4. **Get Anthropic API Key**:
   - Visit [Anthropic Console](https://console.anthropic.com/account/keys)
   - Create new API key
   - Add credits to your account (~$5-10 recommended)

### Usage

1. **Start the application**:
   ```bash
   streamlit run app.py
   ```

2. **Setup (first time)**:
   - Enter your Anthropic API key
   - Connect Google Sheets (one-time OAuth)

3. **Analyze sheets**:
   - Paste any Google Sheets URL
   - Chat with Claude about your data
   - Use quick action buttons for common tasks

## Use Cases

- **Financial Analysis**: Track expenses, income, budgets over multiple years
- **Data Cleanup**: Find duplicates, formatting issues, missing values
- **Trend Analysis**: Identify patterns in time-series data
- **Formula Generation**: Get specific Excel/Sheets formulas for your data
- **Data Organization**: Restructure messy spreadsheets

## Project Structure

```
claude-sheets-assistant/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── setup.sh              # Setup script
├── credentials.json       # Google OAuth credentials (not in git)
├── token.json            # Google auth token (not in git)
├── .env                  # API keys (not in git)
├── .gitignore            # Git ignore file
└── README.md             # This file
```

## Development

### Adding Features

Ideas for future enhancements:
- [ ] Export analysis reports to PDF
- [ ] Batch processing multiple sheets
- [ ] Custom AI prompts/templates
- [ ] Data visualization charts
- [ ] Automated data cleaning actions
- [ ] Integration with other Google Workspace apps
- [ ] Support for Excel files
- [ ] Scheduled analysis reports

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## License

MIT License - see LICENSE file for details

## Security

- API keys are stored locally only
- No data is sent to external services except Anthropic's Claude API
- Google Sheets data is processed locally
- All communication uses HTTPS

## Troubleshooting

### Common Issues

1. **"Your credit balance is too low"**
   - Add credits to your Anthropic account at console.anthropic.com

2. **Google authentication errors**
   - Delete `token.json` and re-authenticate
   - Ensure OAuth consent screen is configured

3. **Sheet not loading**
   - Check if sheet is publicly readable or you have access
   - Verify the sheet URL format

## Support

- Open an issue on GitHub
- Check existing issues for solutions
- Review the troubleshooting section above