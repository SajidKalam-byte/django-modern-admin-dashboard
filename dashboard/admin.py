"""
Custom admin site configuration for the dashboard.
"""

from django.contrib import admin
from django.urls import path
from django.template.response import TemplateResponse
from django.utils.translation import gettext as _
from . import views


class DashboardAdminSite(admin.AdminSite):
    """
    Custom admin site that uses the dashboard styling.
    """
    site_title = _('Dashboard Admin')
    site_header = _('Dashboard Administration')
    index_title = _('Dashboard Overview')
    
    def index(self, request, extra_context=None):
        """
        Override the admin index to use our custom dashboard template.
        """
        return views.admin_index_view(request, extra_context)
    
    def get_urls(self):
        """
        Override to include custom dashboard URLs.
        """
        urls = super().get_urls()
        
        # Add dashboard-specific URLs
        custom_urls = [
            path('widgets/', views.dashboard_view, name='dashboard_widgets'),
            path('settings/', views.dashboard_settings_view, name='dashboard_settings'),
            path('export/', views.export_dashboard_data_view, name='dashboard_export'),
        ]
        
        return custom_urls + urls


# Create an instance of our custom admin site
dashboard_admin_site = DashboardAdminSite(name='dashboard_admin')

# Register all the models that are registered with the default admin site
def register_default_models():
    """
    Register all models from the default admin site with our custom admin site.
    """
    for model, model_admin in admin.site._registry.items():
        dashboard_admin_site.register(model, model_admin.__class__)
