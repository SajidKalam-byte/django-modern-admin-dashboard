"""
Django app configuration for the dashboard.
"""

from django.apps import AppConfig


class DashboardConfig(AppConfig):
    """Configuration for the dashboard app."""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dashboard'
    verbose_name = 'Modern Admin Dashboard'
    
    def ready(self):
        """Initialize the dashboard when Django starts."""
        # Import widgets to ensure they are registered
        try:
            from . import widgets  # noqa
        except ImportError:
            pass
