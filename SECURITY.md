# Security Policy

## Supported Versions

We actively support the following versions with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | ✅ Yes            |

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security vulnerability in this Django admin dashboard package, please report it responsibly.

### How to Report

1. **Do NOT** create a public GitHub issue for security vulnerabilities
2. Email us directly at: [maintainer email] (will be updated when repository is created)
3. Include detailed information about the vulnerability:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### What to Expect

- **Acknowledgment**: We will acknowledge receipt of your report within 48 hours
- **Investigation**: We will investigate and validate the vulnerability within 5 business days
- **Resolution**: We will work on a fix and coordinate disclosure timeline with you
- **Credit**: We will acknowledge your responsible disclosure (if you wish)

### Security Best Practices for Users

When using this package in production:

1. **Keep Dependencies Updated**: Regularly update Django and all dependencies
2. **Secure Configuration**: 
   - Use strong SECRET_KEY values
   - Enable HTTPS in production
   - Configure proper CORS settings
   - Set appropriate permissions for API access
3. **Database Security**: Use secure database credentials and connections
4. **Authentication**: Ensure proper user authentication and authorization
5. **Input Validation**: The package validates inputs, but always validate data in your own views
6. **Permissions**: Configure `CUSTOM_ADMIN_DASHBOARD_CONFIG['API_PERMISSIONS']` appropriately

### Known Security Considerations

- This package requires staff/admin privileges for dashboard access
- API endpoints are protected by authentication and permission checks
- Widget data is cached - ensure cache backend is secure in production
- CSRF protection is enabled for all views

### Scope

This security policy covers:
- The dashboard package code
- Default configurations and templates
- API endpoints and authentication
- Widget system security

This policy does NOT cover:
- Third-party dependencies (report to their respective maintainers)
- User-created custom widgets (secure your own code)
- Django framework itself (report to Django security team)
- Deployment environment security

### Contact

For non-security issues, please use GitHub issues.
For security concerns, use the private reporting method described above.
