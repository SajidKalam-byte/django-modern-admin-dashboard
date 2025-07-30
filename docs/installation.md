# Installation Guide

## Quick Installation

Install the package using pip:

```bash
pip install custom-admin-dashboard
```

## Development Installation

For development or to get the latest features:

```bash
git clone https://github.com/yourname/custom-admin-dashboard.git
cd custom-admin-dashboard
pip install -e .
```

## Requirements

- Python 3.8+
- Django 3.2+
- Django REST Framework 3.12+

## Django Setup

### 1. Add to INSTALLED_APPS

Add the dashboard apps to your Django `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ... your existing apps
    'rest_framework',
    'dashboard',
    'dashboard_config',
]
```

### 2. Configure URLs

Include the dashboard URLs in your main `urls.py`:

```python
from django.urls import path, include

urlpatterns = [
    # ... your existing URLs
    path('admin/dashboard/', include('dashboard.urls')),
]
```

### 3. Configure Settings

Add dashboard configuration to your `settings.py`:

```python
CUSTOM_ADMIN_DASHBOARD_CONFIG = {
    'THEME': 'light',  # 'light' or 'dark'
    'TITLE': 'My Admin Dashboard',
    'WIDGETS': [
        'dashboard.widgets.UserCountWidget',
        'dashboard.widgets.RecentLoginsWidget',
        'dashboard.widgets.LoginActivityChartWidget',
        'dashboard.widgets.SystemStatusWidget',
    ],
    'ENABLE_API': True,
}
```

### 4. Run Migrations

The dashboard doesn't require database migrations, but ensure your Django project is up to date:

```bash
python manage.py migrate
```

### 5. Collect Static Files

Collect static files to serve CSS, JavaScript, and other assets:

```bash
python manage.py collectstatic
```

### 6. Create a Superuser

Create a superuser to access the dashboard:

```bash
python manage.py createsuperuser
```

## Quick Setup Command

Use the built-in management command for quick setup:

```bash
python manage.py dashboard_init --create-superuser --load-sample-data
```

This command will:
- Check your configuration
- Run migrations
- Collect static files
- Create a superuser (optional)
- Load sample data (optional)

## Verification

1. Start your Django development server:
   ```bash
   python manage.py runserver
   ```

2. Visit the dashboard at: `http://127.0.0.1:8000/admin/dashboard/`

3. Log in with your admin credentials

4. You should see the dashboard with default widgets

## Troubleshooting

### Common Issues

**ImportError: No module named 'rest_framework'**
```bash
pip install djangorestframework
```

**TemplateDoesNotExist error**
```bash
python manage.py collectstatic --clear
```

**Permission denied accessing dashboard**
- Ensure your user has `is_staff=True`
- Check that you're logged in as an admin user

**Widgets not showing**
- Verify `CUSTOM_ADMIN_DASHBOARD_CONFIG` is properly configured
- Check that widget classes exist and are importable
- Look for errors in Django logs

### Debug Mode

Enable debug logging for the dashboard:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'dashboard': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
```

## Next Steps

- [Configuration Guide](configuration.md) - Customize your dashboard
- [Creating Widgets](widgets.md) - Build custom widgets
- [API Reference](api.md) - Use the REST API
- [Theming Guide](theming.md) - Customize appearance
