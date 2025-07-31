# Publishing to PyPI Guide

## Prerequisites

1. **Create PyPI Account**: 
   - Go to https://pypi.org/account/register/
   - Create an account
   - Verify your email

2. **Create TestPyPI Account** (for testing):
   - Go to https://test.pypi.org/account/register/
   - Create an account

## Step 1: Install Publishing Tools

```bash
pip install build twine
```

## Step 2: Build the Package

```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info/

# Build the package
python -m build
```

This creates:
- `dist/django_modern_admin_dashboard-0.1.0.tar.gz` (source distribution)
- `dist/django_modern_admin_dashboard-0.1.0-py3-none-any.whl` (wheel)

## Step 3: Test on TestPyPI First

```bash
# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ django-modern-admin-dashboard
```

## Step 4: Upload to PyPI

```bash
# Upload to real PyPI
twine upload dist/*
```

## Step 5: Verify Installation

```bash
pip install django-modern-admin-dashboard
```

## GitHub Actions Auto-Publishing

The repository already has a GitHub Actions workflow (`.github/workflows/publish.yml`) that automatically publishes to PyPI when you create a release.

### To use auto-publishing:

1. **Add PyPI Token to GitHub Secrets**:
   - Go to PyPI → Account Settings → API Tokens
   - Create a new token with scope for this project
   - Go to GitHub repo → Settings → Secrets and Variables → Actions
   - Add secret named `PYPI_API_TOKEN` with your token value

2. **Create a Release**:
   - Go to GitHub repo → Releases
   - Click "Create a new release"
   - Tag version: `v0.1.0`
   - Release title: `v0.1.0 - Initial Release`
   - Describe changes
   - Click "Publish release"

3. **Automatic Publishing**:
   - GitHub Actions will automatically build and publish to PyPI
   - Check the Actions tab for build status

## Manual Publishing Commands

If you prefer manual publishing:

```bash
# Install dependencies
pip install build twine

# Build package
python -m build

# Check package
twine check dist/*

# Upload to PyPI (will prompt for username/password or token)
twine upload dist/*
```

## Troubleshooting

### Common Issues:

1. **Package name already exists**: 
   - Choose a different name in `pyproject.toml`
   - Or contact PyPI to claim the name

2. **Authentication error**:
   - Use API token instead of username/password
   - Format: `__token__` as username, token as password

3. **File already exists**:
   - You can't upload the same version twice
   - Increment version number in `dashboard/_version.py`

### Version Management:

Update version in `dashboard/_version.py`:
```python
__version__ = '0.1.1'  # Increment for new releases
```

## Post-Publishing

After publishing, update the README installation instructions:

```bash
pip install django-modern-admin-dashboard
```

The package will be available at:
- PyPI: https://pypi.org/project/django-modern-admin-dashboard/
- Installation: `pip install django-modern-admin-dashboard`
