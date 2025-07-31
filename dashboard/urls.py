"""
URL configuration for the custom admin dashboard with full Django admin integration.
"""

from django.urls import path, include
from django.contrib import admin
from . import views

app_name = 'dashboard'

# Dashboard-specific URLs (widgets and custom views)
dashboard_patterns = [
    path('widgets/', views.dashboard_view, name='widgets'),  # Pure widget dashboard
    path('class-based/', views.DashboardView.as_view(), name='dashboard_class'),
    path('settings/', views.dashboard_settings_view, name='settings'),
    path('export/', views.export_dashboard_data_view, name='export'),
    path('widget/<str:widget_id>/', views.widget_data_view, name='widget_data'),
    path('widget/<str:widget_id>/refresh/', views.refresh_widget_view, name='widget_refresh'),
]

# API URLs
api_patterns = [
    path('v1/', include('dashboard.api.urls')),
]

urlpatterns = [
    # Custom dashboard views
    path('', include(dashboard_patterns)),
    path('api/', include(api_patterns)),
    
    # Full Django admin functionality with dashboard styling
    # This includes all model admin views, forms, etc.
    path('', admin.site.urls),
]
