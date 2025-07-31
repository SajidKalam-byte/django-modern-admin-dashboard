# Complete Setup Guide to Replace Django Admin with Custom Dashboard

## Your Main Project's urls.py

Replace your main `urls.py` with this configuration:

```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Option 1: Replace admin completely with dashboard
    path('admin/', include('dashboard.urls')),
    
    # Option 2: Keep both (alternative)
    # path('admin/', admin.site.urls),  # Original admin at /admin/
    # path('dashboard/', include('dashboard.urls')),  # Dashboard at /dashboard/
]

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

## Your settings.py Configuration

Add this to your `settings.py`:

```python
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

INSTALLED_APPS = [
    'dashboard',  # Add this BEFORE django.contrib.admin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    # ... your other apps
]

# Static files configuration
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Dashboard Configuration
CUSTOM_ADMIN_DASHBOARD_CONFIG = {
    'SITE_TITLE': 'My Admin Dashboard',
    'SITE_HEADER': 'Modern Administration',
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

# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# Admin site customization
ADMIN_SITE_HEADER = 'Modern Administration'
ADMIN_SITE_TITLE = 'Admin Dashboard'
ADMIN_INDEX_TITLE = 'Welcome to Dashboard'
```

## Commands to Run

After updating your configuration:

```bash
# 1. Initialize dashboard
python manage.py dashboard_init

# 2. Collect static files
python manage.py collectstatic --noinput

# 3. Create superuser if you haven't
python manage.py createsuperuser

# 4. Run the server
python manage.py runserver
```

## What You Should See

1. Go to `http://127.0.0.1:8000/admin/`
2. You should now see the modern dashboard design instead of the default Django admin
3. It will show both admin functionality AND your dashboard widgets

## Troubleshooting

If you still see the default admin:

1. **Check INSTALLED_APPS order**: Make sure `'dashboard'` comes BEFORE `'django.contrib.admin'`
2. **Clear browser cache**: Force refresh with Ctrl+F5
3. **Check templates**: Make sure Django can find the dashboard templates
4. **Restart server**: Sometimes Django needs a restart to pick up template changes

## Template Hierarchy

The dashboard now provides these templates:
- `admin/index.html` - Custom admin index with dashboard
- `admin/base_site.html` - Base admin template with dashboard styling
- `dashboard/base.html` - Main dashboard base template
- `dashboard/dashboard.html` - Pure dashboard view

## Alternative URLs

If you want to keep both interfaces:

- Original Django Admin: `http://127.0.0.1:8000/admin/`  
- Custom Dashboard: `http://127.0.0.1:8000/dashboard/`

Just use Option 2 in the URLs configuration above.
