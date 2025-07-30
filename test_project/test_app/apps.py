"""
Test app configuration.
"""

from django.apps import AppConfig


class TestAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'test_app'
    verbose_name = 'Test Application'
    
    def ready(self):
        """Import widgets when app is ready."""
        try:
            import test_app.widgets  # noqa
        except ImportError:
            pass
