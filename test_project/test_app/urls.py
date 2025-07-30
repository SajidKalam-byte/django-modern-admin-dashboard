"""
Test app URLs.
"""

from django.urls import path
from . import views

app_name = 'test_app'

urlpatterns = [
    path('dashboard/', views.test_dashboard, name='dashboard'),
    path('api/data/', views.api_test_data, name='api_data'),
]
