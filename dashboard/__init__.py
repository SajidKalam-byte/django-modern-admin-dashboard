"""
Custom Admin Dashboard Package.
"""

from ._version import __version__

default_app_config = 'dashboard.apps.DashboardConfig'

# Import the custom admin site
from .admin import dashboard_admin_site

__all__ = ['dashboard_admin_site', '__version__']