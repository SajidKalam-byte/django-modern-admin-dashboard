# Quick Setup Guide for Django Settings

# Add this to your settings.py file:

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Add 'dashboard' to INSTALLED_APPS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',  # Required for dashboard API
    'dashboard',       # Add this line
    # ... your other apps
]

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Dashboard Configuration
CUSTOM_ADMIN_DASHBOARD_CONFIG = {
    'SITE_TITLE': 'My Dashboard',
    'SITE_HEADER': 'Administration Dashboard',
    'INDEX_TITLE': 'Welcome to Dashboard',
    'CACHE_TIMEOUT': 300,
    'WIDGETS': [
        'dashboard.widgets.UserCountWidget',
        'dashboard.widgets.RecentLoginsWidget',
        'dashboard.widgets.LoginActivityChartWidget',
        'dashboard.widgets.SystemStatusWidget',
        'dashboard.widgets.UserRegistrationChartWidget',
    ],
    'THEME': {
        'PRIMARY_COLOR': '#3B82F6',
        'SECONDARY_COLOR': '#64748B',
    }
}

# Django REST Framework settings (required for dashboard API)
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# Cache configuration (optional, for better performance)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}
