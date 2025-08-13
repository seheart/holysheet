# Contributing to HolySheet 🤝

Want to help make HolySheet even more divine? We welcome contributions from the community! Here's how you can help spread the holy spreadsheet wisdom.

## 🌟 Ways to Contribute

### 💻 Code Contributions
- **Bug fixes** - Help squash those unholy bugs
- **New features** - Add divine functionality  
- **Performance improvements** - Make HolySheet faster
- **UI/UX enhancements** - Improve the user experience

### 📚 Documentation
- **Wiki improvements** - Expand these guides
- **Tutorial creation** - Help new users get started
- **FAQ additions** - Answer common questions
- **Code comments** - Make the codebase more readable

### 🐛 Bug Reports & Testing
- **Issue reporting** - Help us find problems
- **Feature requests** - Suggest divine improvements
- **Testing** - Try new features and provide feedback
- **Platform testing** - Test on different OS/environments

### 💬 Community Support
- **Answer questions** in Discussions
- **Share use cases** and success stories
- **Create examples** of interesting analyses
- **Social media** - Spread the word about HolySheet

## 🚀 Getting Started

### Setting Up Development Environment

1. **Fork the repository** on GitHub
2. **Clone your fork**:
   ```bash
   git clone https://github.com/your-username/holysheet.git
   cd holysheet
   ```
3. **Set up development environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```
4. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/seheart/holysheet.git
   ```

### Development Workflow

1. **Create feature branch**:
   ```bash
   git checkout -b feature/divine-new-feature
   ```
2. **Make your changes**
3. **Test thoroughly**:
   ```bash
   streamlit run app.py
   # Test your changes manually
   ```
4. **Commit with descriptive message**:
   ```bash
   git commit -m "✨ Add divine feature for better spreadsheet analysis"
   ```
5. **Push to your fork**:
   ```bash
   git push origin feature/divine-new-feature
   ```
6. **Create Pull Request** on GitHub

## 📋 Contribution Guidelines

### Code Standards

#### Python Style
- Follow **PEP 8** style guidelines
- Use **descriptive variable names**
- Add **docstrings** for functions and classes
- Keep functions **focused and small**
- Use **type hints** where appropriate

#### Example:
```python
def analyze_financial_data(df: pd.DataFrame, date_column: str) -> dict:
    """
    Analyze financial data for trends and insights.
    
    Args:
        df: DataFrame containing financial data
        date_column: Name of the date column
        
    Returns:
        Dictionary containing analysis results
    """
    # Implementation here
    pass
```

#### Streamlit Best Practices
- Use **session state** appropriately
- Implement **error handling** for user inputs
- Provide **clear feedback** to users
- Keep **UI responsive** and intuitive

### Commit Message Format

Use descriptive commit messages with emojis:

```
✨ Add new feature
🐛 Fix bug in data loading
📝 Update documentation  
🎨 Improve UI/UX
⚡ Performance improvement
🔧 Configuration changes
🚀 Deployment related
♻️ Code refactoring
```

### Pull Request Guidelines

#### Before Submitting
- [ ] Code follows style guidelines
- [ ] All existing tests pass
- [ ] New functionality is tested
- [ ] Documentation is updated
- [ ] Changes are described clearly

#### PR Description Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Breaking change

## Testing
Describe how you tested these changes

## Screenshots (if applicable)
Add screenshots for UI changes

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
```

## 🎯 Priority Areas

### High Priority
- **Error handling improvements** - Better user experience
- **Performance optimization** - Faster analysis
- **Mobile responsiveness** - Better mobile experience
- **Data visualization** - Charts and graphs integration

### Medium Priority  
- **Excel file support** - Expand beyond Google Sheets
- **Batch processing** - Multiple sheets at once
- **Custom prompts** - User-defined analysis templates
- **Export features** - Save analysis as PDF/reports

### Nice to Have
- **Dark mode** - Alternative UI theme
- **Keyboard shortcuts** - Power user features
- **Plugin system** - Extensible architecture
- **Voice input** - Accessibility improvements

## 🧪 Testing Guidelines

### Manual Testing Checklist
- [ ] App starts successfully
- [ ] API keys can be configured
- [ ] Google Sheets authentication works
- [ ] Sheet loading functions properly
- [ ] Chat interface responds correctly
- [ ] Quick action buttons work
- [ ] Error handling graceful

### Test Data
Create test sheets with:
- Various data types (financial, business, personal)
- Different sizes (small, medium, large)
- Edge cases (empty cells, special characters)
- Date formats and number formats

## 📊 Project Architecture

### Key Components
- **`app.py`** - Main Streamlit application
- **`HolySheetApp` class** - Core application logic
- **Authentication modules** - Google and Anthropic API handling
- **Data processing** - Sheet loading and formatting
- **Chat interface** - Claude interaction logic

### Dependencies
- **Streamlit** - Web interface framework
- **Anthropic** - Claude AI integration
- **Google APIs** - Sheets access
- **Pandas** - Data manipulation

## 🐛 Bug Report Template

When reporting bugs, please include:

```markdown
## Bug Description
Clear description of the issue

## Steps to Reproduce
1. Step one
2. Step two
3. Bug appears

## Expected Behavior
What should happen

## Actual Behavior  
What actually happens

## Environment
- OS: [Windows/Mac/Linux]
- Python version: [3.x.x]
- HolySheet version: [commit hash]
- Browser: [Chrome/Firefox/Safari]

## Additional Context
Screenshots, error messages, logs
```

## 💡 Feature Request Template

```markdown
## Feature Description
Clear description of the proposed feature

## Use Case
Why is this feature needed? What problem does it solve?

## Proposed Solution
How might this feature work?

## Alternatives Considered
Other approaches you've thought about

## Priority
How important is this feature to you?
```

## 🌟 Recognition

### Contributors Hall of Fame
We recognize contributors in:
- **README.md** acknowledgments
- **Release notes** mentions  
- **Special contributor badges**
- **Annual contributor highlights**

### Contribution Types We Value
- **Code contributions** - Direct development work
- **Documentation** - Improving guides and examples
- **Community support** - Helping other users
- **Testing & QA** - Finding and reporting issues
- **Ideas & feedback** - Shaping project direction

## 📞 Getting Help

### Development Questions
- **[GitHub Discussions](https://github.com/seheart/holysheet/discussions)** - Technical questions
- **[Discord/Slack]** - Real-time chat (coming soon)
- **Email** - Direct contact for sensitive issues

### Code Review Process
1. **Automated checks** run on all PRs
2. **Core maintainer review** for functionality
3. **Community feedback** welcome
4. **Iterative improvements** before merge

## 🚀 Release Process

### Versioning
We use **Semantic Versioning**:
- **MAJOR** - Breaking changes
- **MINOR** - New features (backward compatible)
- **PATCH** - Bug fixes

### Release Timeline
- **Patch releases** - As needed for critical bugs
- **Minor releases** - Monthly feature updates
- **Major releases** - Quarterly significant updates

---

**Thank you for helping make HolySheet more divine!** 🙏✨

Every contribution, no matter how small, helps spread the power of AI-assisted spreadsheet analysis to more users around the world.

**Ready to contribute?** Check out our **[current issues](https://github.com/seheart/holysheet/issues)** or **[open a discussion](https://github.com/seheart/holysheet/discussions)** with your ideas!