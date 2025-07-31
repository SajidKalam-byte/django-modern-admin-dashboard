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
        
        # Override admin site configuration
        self.configure_admin_site()
        
        # Register models with custom admin site
        self.setup_custom_admin()
    
    def setup_custom_admin(self):
        """Set up the custom admin site with all registered models."""
        try:
            from .admin import dashboard_admin_site, register_default_models
            register_default_models()
        except ImportError:
            pass
    
    def configure_admin_site(self):
        """Configure the admin site with custom dashboard styling."""
        from django.contrib import admin
        from django.conf import settings
        
        # Get dashboard config
        dashboard_config = getattr(settings, 'CUSTOM_ADMIN_DASHBOARD_CONFIG', {})
        
        # Update admin site configuration
        admin.site.site_header = dashboard_config.get('SITE_HEADER', 'Modern Admin Dashboard')
        admin.site.site_title = dashboard_config.get('SITE_TITLE', 'Dashboard')
        admin.site.index_title = dashboard_config.get('INDEX_TITLE', 'Welcome to Dashboard')
