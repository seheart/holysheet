# Troubleshooting Guide 🛠️

Having issues with HolySheet? This guide covers the most common problems and their divine solutions!

## 🚨 Quick Fixes

### HolySheet Won't Start
```bash
# Check Python version (need 3.8+)
python3 --version

# Reinstall dependencies
pip install -r requirements.txt

# Try running directly
streamlit run app.py
```

### "Module not found" Errors
```bash
# Make sure you're in the right directory
cd /path/to/holysheet

# Install missing packages
pip install streamlit anthropic google-api-python-client pandas
```

## 🔐 API & Authentication Issues

### Anthropic API Problems

#### "Your credit balance is too low"
**Solution**: Add credits to your Anthropic account
1. Go to https://console.anthropic.com/settings/billing
2. Add $5-10 in credits
3. Wait a few minutes for credits to appear
4. Try again in HolySheet

#### "Invalid API key"
**Symptoms**: Error message when entering API key
**Solutions**:
- Check key format (should start with `sk-ant-`)
- Copy key again from Anthropic console
- Ensure no extra spaces or characters
- Try regenerating the API key

#### "Rate limited" or "Too many requests"
**Solution**: Wait 1-2 minutes and try again
- Claude API has usage limits
- Spread out requests if analyzing large datasets
- Consider upgrading your Anthropic plan for higher limits

### Google Sheets API Problems

#### "Credentials not found" or "credentials.json missing"
**Solutions**:
1. Download `credentials.json` from Google Cloud Console
2. Place it in your HolySheet root directory
3. Ensure filename is exactly `credentials.json`
4. Check file permissions (should be readable)

#### "Google authentication failed"
**Solutions**:
1. Delete `token.json` file if it exists
2. Click "Connect Google Sheets" again
3. Complete OAuth flow in browser
4. Grant all requested permissions

#### "Permission denied" on sheets
**Causes & Solutions**:
- **Private sheet**: Make sure you have access to the sheet
- **Wrong URL**: Check the Google Sheets URL format
- **Sharing settings**: Sheet needs to be accessible to your Google account

#### "API not enabled"
**Solution**: Enable Google Sheets API
1. Go to Google Cloud Console
2. Navigate to "APIs & Services" → "Library"
3. Search for "Google Sheets API"
4. Click "Enable"

## 📊 Sheet Loading Issues

### Sheet Won't Load

#### "No data found in sheet"
**Possible causes**:
- Sheet is empty
- Wrong range specified (try A1:Z100)
- Data starts in a different row
- Sheet has multiple tabs (specify tab name)

**Solutions**:
```
# Try different ranges
A1:Z1000    # Standard range
Sheet1!A1:C100    # Specific tab
B2:F500     # Skip headers
```

#### "Sheet not found" or "Invalid sheet ID"
**Solutions**:
- Check the Google Sheets URL format
- Ensure sheet is not deleted
- Verify you have access to the sheet
- Try copying the URL again

#### "Timeout" errors
**Causes**: Very large sheets (10k+ rows)
**Solutions**:
- Use smaller ranges (A1:Z1000)
- Analyze data in chunks
- Focus on specific date ranges

### Data Display Problems

#### "Data looks wrong" or "Formatting issues"
**Solutions**:
- Check if data contains merged cells
- Verify column headers are in row 1
- Look for hidden columns or rows
- Consider data type mismatches

#### "Missing columns" in preview
**Explanation**: HolySheet shows first 50 rows
**Solutions**:
- This is normal for preview
- Claude analyzes the full dataset
- Use specific ranges if needed

## 💻 Technical Issues

### Streamlit Problems

#### "Streamlit command not found"
**Solutions**:
```bash
# Install streamlit
pip install streamlit

# Use Python module syntax
python -m streamlit run app.py

# Check PATH
which streamlit
```

#### "Port already in use"
**Solution**: Change port
```bash
streamlit run app.py --server.port 8502
```

#### Browser won't open
**Solutions**:
- Manually go to http://localhost:8501
- Check firewall settings
- Try different browser
- Disable browser extensions

### Python Environment Issues

#### "Wrong Python version"
**Check version**:
```bash
python3 --version
# Should be 3.8 or higher
```

#### "Package conflicts"
**Solutions**:
```bash
# Create virtual environment
python3 -m venv holysheet-env
source holysheet-env/bin/activate  # Linux/Mac
# holysheet-env\Scripts\activate  # Windows

# Install fresh dependencies
pip install -r requirements.txt
```

## 🧠 Claude Response Issues

### Claude Gives Weird Responses

#### "Claude seems confused about my data"
**Solutions**:
- Provide more context: "This is financial data with columns for..."
- Clarify data meanings: "Amount column is in dollars, Date is YYYY-MM-DD"
- Ask follow-up questions for clarification

#### "Responses are too generic"
**Solutions**:
- Be more specific in your questions
- Provide context about your goals
- Ask for examples and specific recommendations

#### "Claude says it can't access my data"
**Check**:
- Is the sheet loaded? (Shows in right panel)
- Try refreshing and reloading the sheet
- Verify the data appears in the preview

### Performance Issues

#### "Responses are very slow"
**Causes**:
- Large datasets (many columns/rows)
- Complex analysis requests
- API throttling

**Solutions**:
- Break down requests into smaller parts
- Use smaller data ranges
- Ask simpler questions first, then build complexity

## 🔍 Debugging Steps

### When Nothing Works

1. **Check the basics**:
   - HolySheet running? (streamlit app in browser)
   - API key entered correctly?
   - Google Sheets connected?

2. **Restart everything**:
   ```bash
   # Stop streamlit (Ctrl+C)
   # Start again
   streamlit run app.py
   ```

3. **Clear browser cache**:
   - Refresh page (F5)
   - Hard refresh (Ctrl+Shift+R)
   - Clear browser cache

4. **Check error messages**:
   - Look at terminal where you started streamlit
   - Check browser console (F12)
   - Note exact error messages

### Getting Help

#### Before Asking for Help
1. **Try the solutions above**
2. **Note your setup**:
   - Operating system
   - Python version
   - Exact error messages
   - Steps to reproduce

#### Where to Get Help
- **[GitHub Issues](https://github.com/seheart/holysheet/issues)** - Bug reports
- **[GitHub Discussions](https://github.com/seheart/holysheet/discussions)** - Questions
- **Community Wiki** - Updated solutions

## 🛡️ Security & Privacy Issues

### "Is my data safe?"
**Yes! Here's why**:
- Data processed locally on your machine
- Only sent to Claude API for analysis
- No data stored on external servers
- API keys encrypted locally

### "Can others see my spreadsheets?"
**No**:
- OAuth gives access only to your account
- Other HolySheet users can't access your sheets
- Each installation is completely independent

### "What if I accidentally share sensitive data?"
**Prevention**:
- Remove sensitive columns before analysis
- Use generic column names if needed
- Consider creating sanitized copies of sheets

## 📋 Common Error Messages

### "Request failed for https://api.anthropic.com returned code 400"
**Solution**: Credit balance too low - add credits

### "Request failed for https://api.anthropic.com returned code 401"  
**Solution**: Invalid API key - check and re-enter

### "Request failed for https://api.anthropic.com returned code 429"
**Solution**: Rate limited - wait and try again

### "FileNotFoundError: credentials.json"
**Solution**: Download Google Cloud credentials file

### "google.auth.exceptions.RefreshError"
**Solution**: Delete token.json and re-authenticate

---

**Still having issues?** Don't worry - even divine tools sometimes need debugging! 🙏

**[Open an issue](https://github.com/seheart/holysheet/issues)** and we'll help you get your HolySheet working perfectly! ✨