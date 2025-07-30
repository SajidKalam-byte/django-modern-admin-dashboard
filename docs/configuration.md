# Configuration Guide

## Basic Configuration

Configure the dashboard through your Django `settings.py` using the `CUSTOM_ADMIN_DASHBOARD_CONFIG` dictionary:

```python
CUSTOM_ADMIN_DASHBOARD_CONFIG = {
    'THEME': 'light',
    'TITLE': 'My Dashboard',
    'SUBTITLE': 'Admin Dashboard',
    'WIDGETS': [
        'dashboard.widgets.UserCountWidget',
        'dashboard.widgets.RecentLoginsWidget',
    ],
    'ENABLE_API': True,
    'CACHE_TIMEOUT': 300,
    'ITEMS_PER_PAGE': 10,
}
```

## Configuration Options

### Visual Settings

#### THEME
Controls the default theme appearance.
- **Type**: String
- **Options**: `'light'`, `'dark'`
- **Default**: `'light'`

```python
'THEME': 'dark'
```

#### TITLE
Main title displayed in the dashboard header.
- **Type**: String
- **Default**: `'Admin Dashboard'`

```python
'TITLE': 'My Company Dashboard'
```

#### SUBTITLE
Subtitle text shown below the main title.
- **Type**: String
- **Default**: `'Dashboard'`

```python
'SUBTITLE': 'Management Portal'
```

#### LOGO_URL
URL to a custom logo image.
- **Type**: String (URL)
- **Default**: None

```python
'LOGO_URL': '/static/images/logo.png'
```

### Widget Configuration

#### WIDGETS
List of widget classes to display on the dashboard.
- **Type**: List of strings (import paths)
- **Default**: Built-in widgets

```python
'WIDGETS': [
    'dashboard.widgets.UserCountWidget',
    'dashboard.widgets.RecentLoginsWidget',
    'dashboard.widgets.LoginActivityChartWidget',
    'dashboard.widgets.SystemStatusWidget',
    'myapp.widgets.CustomWidget',
]
```

#### WIDGET_GRID_COLS
Number of columns in the widget grid.
- **Type**: Integer
- **Range**: 1-6
- **Default**: 3

```python
'WIDGET_GRID_COLS': 4
```

### API Settings

#### ENABLE_API
Enable or disable the REST API endpoints.
- **Type**: Boolean
- **Default**: `True`

```python
'ENABLE_API': False
```

#### API_PERMISSION_CLASSES
Custom permission classes for API access.
- **Type**: List of strings (import paths)
- **Default**: `['dashboard.api.permissions.DashboardAPIPermission']`

```python
'API_PERMISSION_CLASSES': [
    'rest_framework.permissions.IsAuthenticated',
    'myapp.permissions.CustomPermission',
]
```

### Performance Settings

#### CACHE_TIMEOUT
Default cache timeout for widget data (in seconds).
- **Type**: Integer
- **Default**: `300` (5 minutes)

```python
'CACHE_TIMEOUT': 600  # 10 minutes
```

#### ENABLE_CACHING
Enable or disable caching for widgets.
- **Type**: Boolean
- **Default**: `True`

```python
'ENABLE_CACHING': False
```

### Pagination Settings

#### ITEMS_PER_PAGE
Default number of items per page for table widgets.
- **Type**: Integer
- **Default**: `10`

```python
'ITEMS_PER_PAGE': 25
```

### Navigation Settings

#### MENU_ITEMS
Custom menu items for the dashboard navigation.
- **Type**: List of dictionaries

```python
'MENU_ITEMS': [
    {
        'title': 'Users',
        'url': '/admin/auth/user/',
        'icon': 'fa fa-users',
    },
    {
        'title': 'Settings',
        'url': '/admin/dashboard/settings/',
        'icon': 'fa fa-cog',
    },
]
```

#### SHOW_DJANGO_ADMIN_LINK
Show a link to the standard Django admin.
- **Type**: Boolean
- **Default**: `True`

```python
'SHOW_DJANGO_ADMIN_LINK': False
```

## Environment-Specific Configuration

### Development Settings

```python
# settings/development.py
CUSTOM_ADMIN_DASHBOARD_CONFIG = {
    'THEME': 'light',
    'CACHE_TIMEOUT': 60,  # Shorter cache for development
    'ENABLE_API': True,
    'WIDGETS': [
        'dashboard.widgets.UserCountWidget',
        'dashboard.widgets.SystemStatusWidget',
    ],
}
```

### Production Settings

```python
# settings/production.py
CUSTOM_ADMIN_DASHBOARD_CONFIG = {
    'THEME': 'dark',
    'CACHE_TIMEOUT': 900,  # Longer cache for production
    'ENABLE_API': True,
    'WIDGETS': [
        'dashboard.widgets.UserCountWidget',
        'dashboard.widgets.RecentLoginsWidget',
        'dashboard.widgets.LoginActivityChartWidget',
        'dashboard.widgets.SystemStatusWidget',
        'myapp.widgets.SalesWidget',
        'myapp.widgets.PerformanceWidget',
    ],
    'LOGO_URL': 'https://cdn.example.com/logo.png',
}
```

## Widget-Specific Configuration

Some widgets accept additional configuration:

```python
CUSTOM_ADMIN_DASHBOARD_CONFIG = {
    'WIDGET_CONFIG': {
        'UserCountWidget': {
            'show_change_indicator': True,
            'time_period': 30,  # days
        },
        'LoginActivityChartWidget': {
            'chart_type': 'line',
            'time_range': 7,  # days
            'color_scheme': 'blue',
        },
    }
}
```

## Advanced Configuration

### Custom Widget Registry

Register widgets programmatically:

```python
# In your app's ready() method
from dashboard.widgets import widget_registry
from myapp.widgets import CustomWidget

widget_registry.register('custom_widget', CustomWidget)
```

### Template Customization

Override default templates:

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            # Your custom templates will override dashboard templates
        ],
        # ... rest of template configuration
    },
]
```

### Static Files Configuration

Customize static file serving:

```python
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    # Add your custom static files here
]

# For custom CSS/JS
CUSTOM_ADMIN_DASHBOARD_CONFIG = {
    'EXTRA_CSS': [
        'dashboard/css/custom.css',
    ],
    'EXTRA_JS': [
        'dashboard/js/custom.js',
    ],
}
```

## Configuration Validation

The dashboard validates configuration on startup. To manually validate:

```python
from dashboard.config import validate_config

# This will raise an exception if configuration is invalid
validate_config()
```

## Configuration Examples

### Minimal Configuration

```python
CUSTOM_ADMIN_DASHBOARD_CONFIG = {
    'WIDGETS': ['dashboard.widgets.UserCountWidget'],
}
```

### Full-Featured Configuration

```python
CUSTOM_ADMIN_DASHBOARD_CONFIG = {
    'THEME': 'dark',
    'TITLE': 'Enterprise Dashboard',
    'SUBTITLE': 'Management Portal',
    'LOGO_URL': '/static/images/logo.png',
    'WIDGETS': [
        'dashboard.widgets.UserCountWidget',
        'dashboard.widgets.RecentLoginsWidget',
        'dashboard.widgets.LoginActivityChartWidget',
        'dashboard.widgets.SystemStatusWidget',
        'myapp.widgets.SalesWidget',
        'myapp.widgets.InventoryWidget',
    ],
    'WIDGET_GRID_COLS': 3,
    'ENABLE_API': True,
    'CACHE_TIMEOUT': 600,
    'ITEMS_PER_PAGE': 15,
    'MENU_ITEMS': [
        {'title': 'Users', 'url': '/admin/auth/user/', 'icon': 'fa fa-users'},
        {'title': 'Reports', 'url': '/reports/', 'icon': 'fa fa-chart-bar'},
    ],
    'EXTRA_CSS': ['dashboard/css/custom.css'],
    'EXTRA_JS': ['dashboard/js/custom.js'],
}
```
