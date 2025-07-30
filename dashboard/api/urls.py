"""
URL configuration for the dashboard API.
"""

from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    # Widget endpoints
    path('widgets/', views.WidgetListAPI.as_view(), name='widget_list'),
    path('widgets/<str:widget_id>/', views.WidgetDetailAPI.as_view(), name='widget_detail'),
    path('charts/<str:widget_id>/', views.ChartDataAPI.as_view(), name='chart_data'),
    
    # Dashboard stats
    path('stats/', views.DashboardStatsAPI.as_view(), name='dashboard_stats'),
    
    # Legacy endpoints
    path('user-count/', views.UserCountAPI.as_view(), name='user_count'),
    
    # Utility endpoints
    path('refresh-cache/', views.refresh_cache_api, name='refresh_cache'),
    path('health/', views.health_check_api, name='health_check'),
]
