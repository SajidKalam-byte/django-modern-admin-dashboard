# CI/CD Troubleshooting Guide

This document helps resolve common CI/CD pipeline issues for the Django Modern Admin Dashboard.

## 🔧 CI/CD Pipeline Overview

Our CI/CD pipeline includes:

1. **Quick Test** - Fast validation with Python 3.10 and Django 4.2
2. **Matrix Test** - Full compatibility testing across Python 3.8-3.11 and Django 3.2-4.2
3. **Security Check** - Basic security scanning with safety

## 🚨 Common Issues and Solutions

### 1. Import Errors

**Problem**: `ImportError` or `ModuleNotFoundError` during imports

**Solutions**:
```bash
# Ensure dependencies are installed
pip install Django>=3.2 djangorestframework>=3.12.0

# Check package installation
pip install -e .

# Run health check
python health_check.py
```

### 2. Django Configuration Issues

**Problem**: `django.core.exceptions.ImproperlyConfigured` or apps not ready

**Solutions**:
- CI uses `tests.conftest` for Django settings
- Ensure `DJANGO_SETTINGS_MODULE=tests.conftest` is set
- Check that `django.setup()` is called after configuration

### 3. Test Failures

**Problem**: Tests fail with database or permission errors

**Solutions**:
```bash
# Run tests locally first
pytest -v

# Check specific test
pytest tests/test_widgets.py -v

# Run with debug output
pytest -s -vv
```

### 4. Dependency Version Conflicts

**Problem**: Version incompatibilities between Django and Python

**Current Support Matrix**:
- Python: 3.8, 3.9, 3.10, 3.11
- Django: 3.2, 4.0, 4.1, 4.2
- DRF: 3.12+

**Solutions**:
```bash
# Check versions
python --version
python -c "import django; print(django.get_version())"

# Install specific versions
pip install Django==4.2 djangorestframework==3.14.0
```

### 5. GitHub Actions Failures

**Problem**: CI workflows fail on GitHub

**Check**:
1. Look at the specific job that failed
2. Check the error logs in GitHub Actions
3. Verify secrets are set (for publishing)
4. Ensure branch protection rules aren't blocking

## 🛠️ Local Development Testing

### Run Full Test Suite
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=dashboard --cov=dashboard_config

# Run specific test categories
pytest tests/test_widgets.py
pytest tests/test_api.py
pytest tests/test_views.py
```

### Run Health Check
```bash
python health_check.py
```

### Code Quality Checks
```bash
# Format code
black dashboard dashboard_config

# Sort imports
isort dashboard dashboard_config

# Lint code
flake8 dashboard dashboard_config
```

### Test Multiple Environments
```bash
# Install tox
pip install tox

# Run tests across environments
tox

# Run specific environment
tox -e py310-django42
```

## 📋 CI Configuration Files

### Key Files:
- `.github/workflows/ci.yml` - Main CI pipeline
- `.github/workflows/publish.yml` - PyPI publishing
- `pyproject.toml` - Modern Python packaging
- `tox.ini` - Multi-environment testing
- `pytest.ini` - Pytest configuration
- `tests/conftest.py` - Django test configuration

### Environment Variables:
- `DJANGO_SETTINGS_MODULE=tests.conftest`
- `PYPI_API_TOKEN` (for publishing, set in GitHub secrets)

## 🔍 Debugging Steps

1. **Local Test First**:
   ```bash
   python health_check.py
   pytest -v
   ```

2. **Check Dependencies**:
   ```bash
   pip list | grep -i django
   pip check
   ```

3. **Verify Installation**:
   ```bash
   pip install -e .
   python -c "import dashboard; print('OK')"
   ```

4. **Check Django Setup**:
   ```bash
   python -c "
   import os
   os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tests.conftest')
   import django
   django.setup()
   print('Django OK')
   "
   ```

## ✅ Success Indicators

When CI is working correctly, you should see:

- ✅ All import checks pass
- ✅ Health check script succeeds
- ✅ Widget registry loads 5 widgets
- ✅ URL patterns resolve correctly
- ✅ Templates load without errors
- ✅ Basic tests pass (45 tests)
- ✅ Security scan completes

## 🚀 Quick Fixes

### Reset Environment
```bash
# Clean slate
rm -rf venv __pycache__ .pytest_cache
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements-dev.txt
pip install -e .
```

### Force Workflow Rerun
```bash
# Create empty commit to trigger CI
git commit --allow-empty -m "Trigger CI"
git push
```

## 📞 Getting Help

If CI issues persist:

1. Check [GitHub Issues](https://github.com/SajidKalam-byte/django-modern-admin-dashboard/issues)
2. Review [GitHub Actions logs](https://github.com/SajidKalam-byte/django-modern-admin-dashboard/actions)
3. Run health check locally: `python health_check.py`
4. Create an issue with error logs and environment details
