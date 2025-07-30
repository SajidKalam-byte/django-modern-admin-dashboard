"""
URL configuration for the custom admin dashboard.
"""

from django.urls import path, include
from . import views

app_name = 'dashboard'

# Main dashboard URLs
dashboard_patterns = [
    path('', views.dashboard_view, name='dashboard'),
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
    path('', include(dashboard_patterns)),
    path('api/', include(api_patterns)),
]
