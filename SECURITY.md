# Security Policy 🔒

## Supported Versions

We support the latest version of HolySheet with security updates.

| Version | Supported          |
| ------- | ------------------ |
| Latest  | ✅ Yes             |
| < Latest| ❌ No              |

## Reporting a Vulnerability

We take security seriously! If you discover a security vulnerability in HolySheet, please report it responsibly.

### 🚨 **DO NOT** create a public issue for security vulnerabilities

### ✅ **DO** report privately:

1. **Email**: seheart@gmail.com with subject "HolySheet Security Issue"
2. **GitHub Security**: Use [private vulnerability reporting](https://github.com/seheart/holysheet/security/advisories/new)

### What to include:

- **Description** of the vulnerability
- **Steps to reproduce** the issue
- **Potential impact** assessment
- **Suggested fix** (if you have one)

### What to expect:

- **Initial response** within 48 hours
- **Regular updates** on progress
- **Credit** in security advisory (if desired)
- **Coordinated disclosure** once fixed

## Security Best Practices for Users

### API Key Security
- **Never share** your Anthropic API key
- **Use environment variables** or secure storage
- **Regenerate keys** if accidentally exposed
- **Monitor usage** in Anthropic console

### Google Credentials
- **Keep `credentials.json` private** (never commit to git)
- **Use read-only permissions** (HolySheet only needs read access)
- **Review OAuth permissions** regularly
- **Revoke access** if no longer needed

### Data Privacy
- **Review sheet contents** before analysis
- **Remove sensitive data** when possible
- **Use generic column names** if needed
- **Remember**: Data is sent to Claude API for analysis

### Local Security
- **Keep Python packages updated**
- **Use virtual environments**
- **Run on trusted networks**
- **Keep your OS updated**

## What We Do to Keep HolySheet Secure

### Code Security
- **Dependency scanning** with Snyk and Dependabot
- **Static analysis** in CI/CD pipeline
- **Regular security updates**
- **Code review** for all changes

### API Integration
- **Secure API communication** (HTTPS only)
- **No data persistence** (process and discard)
- **Minimal permissions** requested
- **Industry standard** OAuth flows

### Privacy by Design
- **Local processing** where possible
- **No user tracking** or analytics
- **No data retention** by HolySheet
- **Transparent** about data flows

## Threat Model

### In Scope
- **Application vulnerabilities** in HolySheet code
- **Dependency vulnerabilities** in requirements
- **API integration security** issues
- **Data handling** vulnerabilities

### Out of Scope
- **Third-party services** (Anthropic, Google)
- **User environment** security
- **Social engineering** attacks
- **Physical access** to user machines

## Security Updates

When we release security updates:

1. **Immediate notification** via GitHub Security Advisories
2. **Update instructions** in release notes
3. **Severity assessment** using CVSS
4. **Coordinated disclosure** timeline

## Compliance

HolySheet follows:

- **OWASP** security guidelines
- **Industry standards** for API integration
- **Privacy by design** principles
- **Responsible disclosure** practices

---

**Holy Sheet, we take security seriously!** 🙏🔒

Thanks for helping keep HolySheet and our community safe!