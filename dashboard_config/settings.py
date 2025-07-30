"""
Configuration management for the custom admin dashboard.
"""

from django.conf import settings


# Default configuration
DEFAULT_CONFIG = {
    'THEME': 'light',  # 'light' or 'dark'
    'TITLE': 'Admin Dashboard',
    'LOGO_URL': None,
    'WIDGETS': [
        'dashboard.widgets.UserCountWidget',
        'dashboard.widgets.RecentLoginsWidget',
        'dashboard.widgets.LoginActivityChartWidget',
        'dashboard.widgets.SystemStatusWidget',
        'dashboard.widgets.UserRegistrationChartWidget',
    ],
    'CHART_COLORS': {
        'primary': '#4F46E5',
        'secondary': '#10B981',
        'success': '#10B981',
        'warning': '#F59E0B',
        'danger': '#EF4444',
        'info': '#3B82F6',
        'purple': '#8B5CF6',
        'pink': '#EC4899',
        'indigo': '#6366F1',
        'blue': '#3B82F6',
        'green': '#10B981',
        'yellow': '#F59E0B',
        'red': '#EF4444',
        'gray': '#6B7280',
    },
    'ENABLE_API': True,
    'API_PERMISSIONS': ['rest_framework.permissions.IsAdminUser'],
    'CACHE_TIMEOUT': 300,  # 5 minutes
    'AUTO_REFRESH': True,
    'REFRESH_INTERVAL': 30000,  # 30 seconds in milliseconds
    'SIDEBAR_ENABLED': True,
    'BREADCRUMBS_ENABLED': True,
    'SEARCH_ENABLED': True,
    'NOTIFICATIONS_ENABLED': True,
    'EXPORT_ENABLED': True,
    'RESPONSIVE_BREAKPOINTS': {
        'sm': '640px',
        'md': '768px',
        'lg': '1024px',
        'xl': '1280px',
        '2xl': '1536px',
    },
    'WIDGET_GRID': {
        'cols': {
            'default': 1,
            'md': 2,
            'lg': 3,
            'xl': 4,
        },
        'gap': 4,
    },
    'ANIMATION_DURATION': 300,  # milliseconds
    'DATE_FORMAT': 'Y-m-d H:i:s',
    'TIMEZONE_DISPLAY': True,
    'LANGUAGE_CODE': 'en-us',
    'DEBUG_MODE': False,
}


def get_dashboard_settings():
    """
    Get dashboard configuration merged with user settings.
    """
    user_config = getattr(settings, 'CUSTOM_ADMIN_DASHBOARD_CONFIG', {})
    
    # Deep merge configurations
    config = DEFAULT_CONFIG.copy()
    
    for key, value in user_config.items():
        if key in config and isinstance(config[key], dict) and isinstance(value, dict):
            # Deep merge dictionaries
            config[key] = {**config[key], **value}
        else:
            # Override other values
            config[key] = value
    
    return config


def get_theme_config(theme=None):
    """
    Get theme-specific configuration.
    """
    config = get_dashboard_settings()
    current_theme = theme or config.get('THEME', 'light')
    
    if current_theme == 'dark':
        return {
            'bg_primary': 'bg-gray-900',
            'bg_secondary': 'bg-gray-800',
            'bg_card': 'bg-gray-800',
            'text_primary': 'text-white',
            'text_secondary': 'text-gray-300',
            'text_muted': 'text-gray-400',
            'border': 'border-gray-700',
            'hover': 'hover:bg-gray-700',
            'ring': 'ring-gray-700',
        }
    else:
        return {
            'bg_primary': 'bg-white',
            'bg_secondary': 'bg-gray-50',
            'bg_card': 'bg-white',
            'text_primary': 'text-gray-900',
            'text_secondary': 'text-gray-700',
            'text_muted': 'text-gray-500',
            'border': 'border-gray-200',
            'hover': 'hover:bg-gray-50',
            'ring': 'ring-gray-200',
        }


def get_chart_colors():
    """
    Get chart color palette.
    """
    config = get_dashboard_settings()
    return config.get('CHART_COLORS', DEFAULT_CONFIG['CHART_COLORS'])


def get_widget_config():
    """
    Get widget-specific configuration.
    """
    config = get_dashboard_settings()
    return {
        'refresh_interval': config.get('REFRESH_INTERVAL', 30000),
        'cache_timeout': config.get('CACHE_TIMEOUT', 300),
        'auto_refresh': config.get('AUTO_REFRESH', True),
        'grid': config.get('WIDGET_GRID', DEFAULT_CONFIG['WIDGET_GRID']),
    }


def is_feature_enabled(feature):
    """
    Check if a specific feature is enabled.
    """
    config = get_dashboard_settings()
    feature_key = f"{feature.upper()}_ENABLED"
    return config.get(feature_key, False)


def get_api_config():
    """
    Get API-specific configuration.
    """
    config = get_dashboard_settings()
    return {
        'enabled': config.get('ENABLE_API', True),
        'permissions': config.get('API_PERMISSIONS', ['rest_framework.permissions.IsAdminUser']),
        'cache_timeout': config.get('CACHE_TIMEOUT', 300),
    }
