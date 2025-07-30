# Contributing to Custom Admin Dashboard

We love your input! We want to make contributing to Custom Admin Dashboard as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## Development Process

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

## Pull Requests

Pull requests are the best way to propose changes to the codebase. We actively welcome your pull requests:

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Issue that pull request!

## Development Setup

### Prerequisites

- Python 3.8+
- Django 3.2+
- Node.js (for frontend tooling, optional)
- Git

### Local Development

1. **Fork and clone the repository:**

```bash
git clone https://github.com/yourusername/custom-admin-dashboard.git
cd custom-admin-dashboard
```

2. **Set up a virtual environment:**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**

```bash
pip install -e .
pip install -r requirements-dev.txt
```

4. **Set up the test project:**

```bash
cd test_project
python manage.py migrate
python manage.py dashboard_init --create-superuser
```

5. **Run tests:**

```bash
pytest
```

6. **Start the development server:**

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/admin/dashboard/` to see the dashboard.

## Code Style

We use several tools to maintain code quality:

### Python Code Style

- **Black** for code formatting
- **isort** for import sorting
- **flake8** for linting
- **mypy** for type checking

Run these tools before submitting:

```bash
# Format code
black dashboard/ tests/

# Sort imports
isort dashboard/ tests/

# Check linting
flake8 dashboard/ tests/

# Type checking
mypy dashboard/
```

### Frontend Code Style

- **Prettier** for CSS/JavaScript formatting
- **ESLint** for JavaScript linting

```bash
# Format frontend code
npm run format

# Lint JavaScript
npm run lint
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=dashboard

# Run specific test file
pytest tests/test_widgets.py

# Run specific test
pytest tests/test_widgets.py::TestUserCountWidget::test_get_value
```

### Writing Tests

We use pytest for testing. Tests should be placed in the `tests/` directory:

```python
# tests/test_my_feature.py
import pytest
from django.test import TestCase
from dashboard.widgets import MyWidget

class TestMyWidget(TestCase):
    def setUp(self):
        self.widget = MyWidget()
    
    def test_widget_functionality(self):
        result = self.widget.get_value()
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, 0)
```

### Test Guidelines

1. **Write tests for all new features**
2. **Maintain or improve test coverage**
3. **Use descriptive test names**
4. **Mock external dependencies**
5. **Test both success and failure cases**

## Documentation

### Writing Documentation

- Use Markdown for all documentation
- Keep language clear and concise
- Include code examples
- Update relevant docs when changing functionality

### Building Documentation Locally

```bash
# Install documentation dependencies
pip install -r docs/requirements.txt

# Build documentation
cd docs
make html

# View documentation
open _build/html/index.html
```

## Submitting Changes

### Commit Messages

Follow conventional commit format:

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:
```
feat(widgets): add support for custom chart colors

fix(api): handle missing widget data gracefully

docs(readme): update installation instructions
```

### Pull Request Process

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/my-new-feature
   ```

2. **Make your changes and commit:**
   ```bash
   git add .
   git commit -m "feat(widgets): add custom widget type"
   ```

3. **Push to your fork:**
   ```bash
   git push origin feature/my-new-feature
   ```

4. **Create a pull request** on GitHub

### Pull Request Template

When creating a pull request, please include:

- **Description**: What does this PR do?
- **Motivation**: Why is this change needed?
- **Testing**: How has this been tested?
- **Screenshots**: If UI changes, include screenshots
- **Breaking Changes**: Any breaking changes?

## Issue Reporting

### Bug Reports

When filing a bug report, please include:

1. **Clear title** describing the issue
2. **Steps to reproduce** the bug
3. **Expected behavior**
4. **Actual behavior**
5. **Environment details** (OS, Python version, Django version)
6. **Error messages** or stack traces

### Feature Requests

For feature requests, please include:

1. **Clear description** of the feature
2. **Use case** explaining why it's needed
3. **Proposed implementation** (if you have ideas)
4. **Alternative solutions** you've considered

## Coding Standards

### Python Standards

1. **Follow PEP 8** style guidelines
2. **Use type hints** for function signatures
3. **Write docstrings** for classes and functions
4. **Keep functions small** and focused
5. **Use meaningful variable names**

Example:

```python
from typing import Dict, List, Optional

class ExampleWidget(BaseWidget):
    """Example widget demonstrating coding standards.
    
    This widget shows how to properly structure code
    according to project standards.
    """
    
    def get_data(self) -> Dict[str, Any]:
        """Get widget data from the database.
        
        Returns:
            Dictionary containing widget data with keys:
            - value: The main metric value
            - change: Percentage change from previous period
        """
        current_value = self._calculate_current_value()
        previous_value = self._calculate_previous_value()
        
        return {
            'value': current_value,
            'change': self._calculate_change(current_value, previous_value)
        }
    
    def _calculate_current_value(self) -> int:
        """Calculate the current metric value."""
        # Implementation here
        pass
```

### Frontend Standards

1. **Use semantic HTML**
2. **Follow BEM CSS methodology**
3. **Use modern JavaScript (ES6+)**
4. **Ensure accessibility compliance**
5. **Write responsive CSS**

## Release Process

### Versioning

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Creating a Release

1. **Update version** in `setup.py`
2. **Update CHANGELOG.md**
3. **Create release tag:**
   ```bash
   git tag -a v1.2.0 -m "Release version 1.2.0"
   git push origin v1.2.0
   ```
4. **Create GitHub release** with changelog
5. **Publish to PyPI** (maintainers only)

## Community Guidelines

### Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md).

### Getting Help

- **GitHub Discussions**: For questions and general discussion
- **GitHub Issues**: For bugs and feature requests
- **Stack Overflow**: Tag questions with `custom-admin-dashboard`

## Recognition

Contributors will be recognized in:

- **README.md**: Contributors section
- **CHANGELOG.md**: Release notes
- **GitHub**: Contributor graphs and statistics

## License

By contributing, you agree that your contributions will be licensed under the same MIT License that covers the project.

## Questions?

Don't hesitate to ask questions or reach out to maintainers if you need help with your contribution!

Thank you for contributing to Custom Admin Dashboard! 🎉
