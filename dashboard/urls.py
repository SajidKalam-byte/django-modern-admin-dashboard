"""
URL configuration for the custom admin dashboard.
"""

from django.urls import path, include
from django.contrib import admin
from . import views

app_name = 'dashboard'

# Main dashboard URLs
dashboard_patterns = [
    path('', views.admin_index_view, name='index'),  # Admin index replacement
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('class-based/', views.DashboardView.as_view(), name='dashboard_class'),
    path('settings/', views.dashboard_settings_view, name='settings'),
    path('export/', views.export_dashboard_data_view, name='export'),
    path('widget/<str:widget_id>/', views.widget_data_view, name='widget_data'),
    path('widget/<str:widget_id>/refresh/', views.refresh_widget_view, name='widget_refresh'),
    
    # Keep essential admin functionality
    path('logout/', admin.site.logout, name='logout'),
    path('login/', admin.site.login, name='login'),
    path('password_change/', admin.site.password_change, name='password_change'),
    path('password_change/done/', admin.site.password_change_done, name='password_change_done'),
]

# API URLs
api_patterns = [
    path('v1/', include('dashboard.api.urls')),
]

urlpatterns = [
    path('', include(dashboard_patterns)),
    path('api/', include(api_patterns)),
    
    # Include all other admin URLs (for model admin, etc.)
    # This preserves full admin functionality while our dashboard handles the index
    path('', admin.site.urls),
]
