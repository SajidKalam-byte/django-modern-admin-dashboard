"""
API views for the custom admin dashboard.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from django.core.cache import cache
from django.conf import settings

from ..widgets import widget_registry
from dashboard_config.settings import get_dashboard_settings


class DashboardAPIPermission(permissions.BasePermission):
    """
    Custom permission for dashboard API access.
    """
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        config = get_dashboard_settings()
        api_permissions = config.get('API_PERMISSIONS', ['rest_framework.permissions.IsAdminUser'])
        
        # Check if API is enabled
        if not config.get('ENABLE_API', True):
            return False
        
        # Default to admin users if no permissions specified
        if not api_permissions:
            return request.user.is_staff
        
        # Check each permission
        for permission_path in api_permissions:
            try:
                module_path, class_name = permission_path.rsplit('.', 1)
                module = __import__(module_path, fromlist=[class_name])
                permission_class = getattr(module, class_name)
                permission_instance = permission_class()
                
                if permission_instance.has_permission(request, view):
                    return True
            except (ImportError, AttributeError):
                continue
        
        return False


class WidgetListAPI(APIView):
    """
    API endpoint to list all available widgets.
    """
    permission_classes = [DashboardAPIPermission]
    
    def get(self, request):
        enabled_widgets = widget_registry.get_enabled_widgets()
        
        widgets_data = []
        for widget_class in enabled_widgets:
            widget_instance = widget_class(request=request)
            
            if widget_instance.has_permission(request.user):
                widgets_data.append({
                    'id': getattr(widget_class, 'widget_id', widget_class.__name__),
                    'title': widget_instance.title,
                    'description': widget_instance.description,
                    'type': widget_instance.widget_type,
                    'icon': widget_instance.icon,
                    'color': widget_instance.color,
                    'refresh_interval': widget_instance.refresh_interval,
                })
        
        return Response({
            'widgets': widgets_data,
            'count': len(widgets_data)
        })


class WidgetDetailAPI(APIView):
    """
    API endpoint to get specific widget data.
    """
    permission_classes = [DashboardAPIPermission]
    
    def get(self, request, widget_id):
        widget_class = widget_registry.get_widget(widget_id)
        if not widget_class:
            return Response(
                {'error': 'Widget not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        widget_instance = widget_class(request=request)
        
        if not widget_instance.has_permission(request.user):
            return Response(
                {'error': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Check cache
        cache_key = f"api_widget_data_{widget_id}_{request.user.id}"
        cached_data = cache.get(cache_key)
        
        if cached_data is None:
            try:
                data = widget_instance.get_api_data()
                data['widget_id'] = widget_id
                cache.set(cache_key, data, timeout=widget_instance.cache_timeout)
            except Exception as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            data = cached_data
        
        return Response(data)


class ChartDataAPI(APIView):
    """
    API endpoint to get chart data for a specific widget.
    """
    permission_classes = [DashboardAPIPermission]
    
    def get(self, request, widget_id):
        widget_class = widget_registry.get_widget(widget_id)
        if not widget_class:
            return Response(
                {'error': 'Widget not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        widget_instance = widget_class(request=request)
        
        if not widget_instance.has_permission(request.user):
            return Response(
                {'error': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        chart_data = widget_instance.get_chart_data()
        if chart_data is None:
            return Response(
                {'error': 'Widget does not provide chart data'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        return Response({
            'widget_id': widget_id,
            'chart_data': chart_data
        })


class DashboardStatsAPI(APIView):
    """
    API endpoint to get overall dashboard statistics.
    """
    permission_classes = [DashboardAPIPermission]
    
    def get(self, request):
        config = get_dashboard_settings()
        enabled_widgets = widget_registry.get_enabled_widgets()
        
        # Calculate basic stats
        total_widgets = len(widget_registry.get_all_widgets())
        enabled_widget_count = len(enabled_widgets)
        accessible_widgets = 0
        
        for widget_class in enabled_widgets:
            widget_instance = widget_class(request=request)
            if widget_instance.has_permission(request.user):
                accessible_widgets += 1
        
        # Get user stats
        total_users = User.objects.count()
        active_users = User.objects.filter(is_active=True).count()
        staff_users = User.objects.filter(is_staff=True).count()
        
        return Response({
            'dashboard': {
                'title': config.get('TITLE', 'Admin Dashboard'),
                'theme': config.get('THEME', 'light'),
                'version': '1.0.0',
            },
            'widgets': {
                'total': total_widgets,
                'enabled': enabled_widget_count,
                'accessible': accessible_widgets,
            },
            'users': {
                'total': total_users,
                'active': active_users,
                'staff': staff_users,
            },
            'config': {
                'api_enabled': config.get('ENABLE_API', True),
                'cache_enabled': bool(cache),
            }
        })


class UserCountAPI(APIView):
    """
    Legacy API endpoint for user count (backward compatibility).
    """
    permission_classes = [DashboardAPIPermission]
    
    def get(self, request):
        return Response({
            'count': User.objects.count(),
            'active_count': User.objects.filter(is_active=True).count(),
        })


@api_view(['POST'])
@permission_classes([DashboardAPIPermission])
def refresh_cache_api(request):
    """
    API endpoint to refresh dashboard cache.
    """
    try:
        # Clear all widget caches for the current user
        cache.delete_many([
            f"widget_data_{widget_id}_{request.user.id}"
            for widget_id in widget_registry._widgets.keys()
        ])
        
        # Clear API caches too
        cache.delete_many([
            f"api_widget_data_{widget_id}_{request.user.id}"
            for widget_id in widget_registry._widgets.keys()
        ])
        
        return Response({'message': 'Cache refreshed successfully'})
    
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([DashboardAPIPermission])
def health_check_api(request):
    """
    API endpoint for health check.
    """
    import django
    from django.db import connection
    
    health_data = {
        'status': 'healthy',
        'django_version': django.get_version(),
        'database': 'connected',
        'cache': 'active' if cache else 'inactive',
        'widgets_loaded': len(widget_registry.get_all_widgets()),
    }
    
    try:
        # Test database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
    except Exception:
        health_data['database'] = 'error'
        health_data['status'] = 'degraded'
    
    try:
        # Test cache
        cache.set('health_check', 'ok', 10)
        if cache.get('health_check') != 'ok':
            health_data['cache'] = 'error'
            health_data['status'] = 'degraded'
    except Exception:
        health_data['cache'] = 'error'
        health_data['status'] = 'degraded'
    
    return Response(health_data)
