# Security Policy

## Supported Versions

We release security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

The Presentation App team takes security vulnerabilities seriously. We appreciate your efforts to responsibly disclose your findings.

### Where to Report

**Please do NOT report security vulnerabilities through public GitHub issues.**

Instead, please report security vulnerabilities via one of the following methods:

1. **Email**: Send details to [security@yourorganization.com](mailto:security@yourorganization.com)
2. **GitHub Security Advisories**: Use the [Security Advisory](https://github.com/yourorg/presentation_app/security/advisories/new) feature

### What to Include

Please include the following information in your report:

- **Description**: Clear description of the vulnerability
- **Impact**: Potential impact and severity
- **Reproduction Steps**: Detailed steps to reproduce the issue
- **Proof of Concept**: If possible, provide a PoC
- **Environment**: OS, browser, versions, etc.
- **Suggested Fix**: If you have ideas on how to fix it

**Example Report**:
```markdown
**Vulnerability**: SQL Injection in session lookup

**Impact**: Attackers could potentially access other users' sessions

**Reproduction Steps**:
1. Send malicious session_id parameter: `' OR '1'='1`
2. Observe unauthorized session access

**Environment**:
- Backend version: 0.1.0
- Python: 3.11
- SQLite: 3.42

**Suggested Fix**:
Use parameterized queries instead of string interpolation
```

## Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 5 business days
- **Resolution Target**: Varies by severity
  - Critical: 1-7 days
  - High: 7-30 days
  - Medium: 30-90 days
  - Low: 90+ days

## Disclosure Policy

- **Coordinated Disclosure**: We practice responsible disclosure
- **Public Disclosure**: After a fix is available and deployed
- **Credit**: Security researchers will be credited (if desired)
- **CVE Assignment**: We'll request CVEs for significant vulnerabilities

## Security Best Practices

### For Users

#### API Key Security

1. **Never commit API keys** to version control
2. **Use environment variables** to store sensitive data
3. **Rotate keys regularly** (at least every 90 days)
4. **Limit key permissions** to minimum required access
5. **Monitor key usage** for suspicious activity

#### Deployment Security

1. **Use HTTPS** in production
2. **Enable CORS** restrictions
3. **Implement rate limiting**
4. **Keep dependencies updated**
5. **Use strong passwords** for all services
6. **Enable 2FA** where available

#### Session Security

1. **Clear browser data** when using shared computers
2. **Log out** when finished
3. **Don't share session IDs**
4. **Report suspicious activity** immediately

### For Developers

#### Code Security

1. **Input Validation**
   ```python
   # Bad
   query = f"SELECT * FROM sessions WHERE id = '{session_id}'"
   
   # Good
   query = "SELECT * FROM sessions WHERE id = ?"
   cursor.execute(query, (session_id,))
   ```

2. **API Key Handling**
   ```python
   # Bad - Storing in database
   db.save_api_key(user_id, api_key)
   
   # Good - Never store API keys
   # Keys should be provided by client with each request
   ```

3. **File Upload Security**
   ```python
   # Validate file types
   ALLOWED_EXTENSIONS = {'.pdf', '.docx', '.txt'}
   
   # Check file size
   MAX_SIZE = 10 * 1024 * 1024  # 10MB
   
   # Sanitize filenames
   secure_filename(original_filename)
   ```

4. **Output Encoding**
   ```typescript
   // Use React's built-in XSS protection
   <div dangerouslySetInnerHTML={{ __html: sanitizedContent }} />
   
   // Or use a sanitization library
   import DOMPurify from 'dompurify';
   const clean = DOMPurify.sanitize(dirty);
   ```

#### Dependency Security

1. **Regular Updates**
   ```bash
   # Backend
   pip list --outdated
   pip install -U package-name
   
   # Frontend
   npm outdated
   npm update
   ```

2. **Security Audits**
   ```bash
   # Python
   pip install safety
   safety check
   
   # Node.js
   npm audit
   npm audit fix
   ```

3. **Automated Scanning**
   - Enable Dependabot
   - Use Snyk or similar tools
   - Configure GitHub Security Alerts

#### Authentication & Authorization

1. **API Key Validation**
   ```python
   async def validate_api_key(api_key: str) -> bool:
       """Validate API key with service provider."""
       try:
           # Test with minimal API call
           await service.test_key(api_key)
           return True
       except AuthenticationError:
           return False
   ```

2. **Rate Limiting**
   ```python
   from slowapi import Limiter
   
   limiter = Limiter(key_func=get_remote_address)
   
   @app.post("/agent")
   @limiter.limit("60/minute")
   async def agent_endpoint(...):
       pass
   ```

3. **CORS Configuration**
   ```python
   # Restrictive CORS in production
   CORS_ORIGINS = [
       "https://yourdomain.com",
       "https://www.yourdomain.com"
   ]
   ```

#### Logging & Monitoring

1. **Secure Logging**
   ```python
   # Bad - Logging sensitive data
   logger.info(f"User API key: {api_key}")
   
   # Good - Redacting sensitive data
   logger.info(f"User API key: {api_key[:8]}...")
   ```

2. **Error Handling**
   ```python
   # Bad - Exposing internal details
   raise Exception(f"Database error: {sql_query}")
   
   # Good - Generic error message
   raise HTTPException(500, "Internal server error")
   # Log details internally for debugging
   logger.error(f"Database error: {sql_query}")
   ```

3. **Security Monitoring**
   - Failed authentication attempts
   - Unusual API usage patterns
   - File upload anomalies
   - Session manipulation attempts

## Known Security Considerations

### Current Limitations

1. **Client-Side API Keys**
   - API keys are stored in browser sessionStorage
   - Keys are transmitted with each request
   - **Mitigation**: Consider server-side key management for production

2. **Session Storage**
   - Sessions stored in SQLite and filesystem
   - No encryption at rest by default
   - **Mitigation**: Implement encryption for sensitive data

3. **File Processing**
   - Uploaded files processed with external service (LlamaParse)
   - **Mitigation**: Validate and sanitize all file inputs

4. **PPTX Export**
   - Uses Node.js subprocess with JSON data
   - **Mitigation**: Validate and sanitize presentation data before export

### Planned Security Enhancements

- [ ] Server-side API key management
- [ ] End-to-end encryption for session data
- [ ] Enhanced file validation and sandboxing
- [ ] OAuth 2.0 integration for authentication
- [ ] Audit logging for all sensitive operations
- [ ] Web Application Firewall (WAF) integration

## Compliance

### Data Privacy

- **No PII Collection**: We don't collect personal information by default
- **User Content**: Presentations are stored temporarily (24 hours)
- **API Keys**: Never stored on backend
- **Context Files**: Processed but not permanently stored

### GDPR Considerations

If deploying in EU:
- Implement data retention policies
- Provide data export functionality
- Enable data deletion on request
- Add cookie consent if using analytics

### SOC 2 Compliance

For enterprise deployments:
- Enable comprehensive audit logging
- Implement access controls
- Document security procedures
- Conduct regular security reviews

## Security Checklist for Production

- [ ] HTTPS enabled with valid SSL/TLS certificate
- [ ] CORS properly configured with allowed origins
- [ ] Rate limiting enabled
- [ ] API keys never logged or stored
- [ ] Input validation on all endpoints
- [ ] Output encoding for user-generated content
- [ ] File upload validation and size limits
- [ ] Database queries parameterized
- [ ] Dependencies up to date
- [ ] Security headers configured (CSP, X-Frame-Options, etc.)
- [ ] Monitoring and alerting enabled
- [ ] Regular security audits scheduled
- [ ] Incident response plan documented
- [ ] Backup and disaster recovery plan in place

## Security Tools & Resources

### Recommended Tools

- **SAST**: Bandit (Python), ESLint security plugin (JavaScript)
- **Dependency Scanning**: Safety, npm audit, Snyk
- **Runtime Protection**: Sentry, CloudFlare WAF
- **Secrets Detection**: git-secrets, truffleHog
- **Container Scanning**: Trivy, Clair

### External Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)
- [CWE Top 25](https://cwe.mitre.org/top25/archive/2023/2023_top25_list.html)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)

## Contact

For security-related questions or concerns:

- **Email**: security@yourorganization.com
- **PGP Key**: [Link to public PGP key if applicable]
- **Security Page**: https://yourorganization.com/security

---

**Last Updated**: February 5, 2026  
**Version**: 1.0
