"""
Views for the custom admin dashboard.
"""

from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.admin import site
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.response import TemplateResponse
from django.utils.translation import gettext as _

# Import dashboard widgets and utilities
from .widgets import (
    UserCountWidget, 
    QuickActionsWidget,
    SystemStatusWidget,
    get_dashboard_widgets
)


@staff_member_required
def admin_index_view(request, extra_context=None):
    """
    Custom admin index view that uses the dashboard template.
    This replaces Django's default admin index.
    """
    # Get the standard admin context
    app_list = site.get_app_list(request)
    
    context = {
        'title': _('Site administration'),
        'app_list': app_list,
        'available_apps': app_list,  # For backward compatibility
        'has_permission': request.user.is_active and request.user.is_staff,
        'site_title': site.site_title,
        'site_header': site.site_header,
        'site_url': site.site_url,
        'site_index_title': _('Site administration'),
    }
    
    # Add extra context if provided
    if extra_context:
        context.update(extra_context)
    
    return TemplateResponse(request, 'admin/index.html', context)


@login_required
def dashboard_view(request):
    """
    Main dashboard view with widgets (for /dashboard/widgets/ URL).
    """
    widgets = get_dashboard_widgets()
    context = {
        'title': 'Dashboard',
        'widgets': widgets,
        'user_stats': UserCountWidget().get_context(),
        'quick_actions': QuickActionsWidget().get_context(),
        'system_status': SystemStatusWidget().get_context(),
    }
    return render(request, 'dashboard/dashboard.html', context)


class DashboardView(LoginRequiredMixin, TemplateView):
    """
    Class-based dashboard view.
    """
    template_name = 'dashboard/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Dashboard',
            'widgets': get_dashboard_widgets(),
            'user_stats': UserCountWidget().get_context(),
            'quick_actions': QuickActionsWidget().get_context(),
            'system_status': SystemStatusWidget().get_context(),
        })
        return context


@staff_member_required
def dashboard_settings_view(request):
    """
    Dashboard settings view.
    """
    context = {
        'title': 'Dashboard Settings',
    }
    return render(request, 'dashboard/settings.html', context)


@staff_member_required
def export_dashboard_data_view(request):
    """
    Export dashboard data as JSON.
    """
    data = {
        'user_stats': UserCountWidget().get_context(),
        'quick_actions': QuickActionsWidget().get_context(),
        'system_status': SystemStatusWidget().get_context(),
        'export_timestamp': request.GET.get('timestamp', 'now'),
    }
    return JsonResponse(data)


@staff_member_required
def widget_data_view(request, widget_id):
    """
    Get data for a specific widget.
    """
    widgets = {
        'user_stats': UserCountWidget(),
        'quick_actions': QuickActionsWidget(),
        'system_status': SystemStatusWidget(),
    }
    
    widget = widgets.get(widget_id)
    if widget:
        data = widget.get_context()
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Widget not found'}, status=404)


@staff_member_required
def refresh_widget_view(request, widget_id):
    """
    Refresh data for a specific widget.
    """
    # This would typically refresh cached data
    return widget_data_view(request, widget_id)

import json
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.conf import settings
from django.core.cache import cache
from django.utils import timezone

from .widgets import widget_registry
from dashboard_config.settings import get_dashboard_settings


@staff_member_required
def admin_index_view(request):
    """Admin index view with dashboard integration."""
    from django.contrib.admin import site
    from django.contrib.admin.models import LogEntry
    
    # Get Django admin context
    app_list = site.get_app_list(request)
    
    # Get dashboard widgets
    config = get_dashboard_settings()
    enabled_widgets = widget_registry.get_enabled_widgets()
    
    widgets = []
    for widget_class in enabled_widgets:
        widget_instance = widget_class(request=request)
        if widget_instance.has_permission(request.user):
            widgets.append(widget_instance)
    
    # Get recent admin log entries (what Django's admin expects)
    log_entries = LogEntry.objects.filter(
        user=request.user
    ).select_related('content_type', 'user')[:10]
    
    context = {
        'title': config.get('SITE_TITLE', 'Administration Dashboard'),
        'site_title': config.get('SITE_TITLE', 'Django administration'), 
        'site_header': config.get('SITE_HEADER', 'Administration Dashboard'),
        'site_index_title': config.get('INDEX_TITLE', 'Welcome to Dashboard'),
        'available_apps': app_list,
        'app_list': app_list,  # Django admin expects this
        'widgets': widgets,
        'config': config,
        'log_entries': log_entries,  # Fix for the KeyError
        'user': request.user,
        'has_permission': True,  # User is already staff (checked by decorator)
    }
    
    # Use our dashboard template instead of Django's default admin template
    return render(request, 'dashboard/dashboard.html', context)


@staff_member_required
def dashboard_view(request):
    """Main dashboard view."""
    config = get_dashboard_settings()
    
    # Get enabled widgets
    enabled_widgets = widget_registry.get_enabled_widgets()
    
    # Initialize widgets with request context
    widgets = []
    for widget_class in enabled_widgets:
        widget_instance = widget_class(request=request)
        
        # Check permissions
        if widget_instance.has_permission(request.user):
            widgets.append(widget_instance)
    
    # Theme configuration
    theme = config.get('THEME', 'light')
    title = config.get('TITLE', 'Admin Dashboard')
    logo_url = config.get('LOGO_URL', None)
    
    context = {
        'widgets': widgets,
        'theme': theme,
        'title': title,
        'logo_url': logo_url,
        'config': config,
    }
    
    return render(request, 'dashboard/dashboard.html', context)


@method_decorator(staff_member_required, name='dispatch')
class DashboardView(TemplateView):
    """Class-based dashboard view for more complex scenarios."""
    
    template_name = 'dashboard/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        config = get_dashboard_settings()
        
        # Get enabled widgets
        enabled_widgets = widget_registry.get_enabled_widgets()
        
        # Initialize widgets with request context
        widgets = []
        for widget_class in enabled_widgets:
            widget_instance = widget_class(request=self.request)
            
            # Check permissions
            if widget_instance.has_permission(self.request.user):
                widgets.append(widget_instance)
        
        context.update({
            'widgets': widgets,
            'theme': config.get('THEME', 'light'),
            'title': config.get('TITLE', 'Admin Dashboard'),
            'logo_url': config.get('LOGO_URL', None),
            'config': config,
        })
        
        return context


@staff_member_required
def widget_data_view(request, widget_id):
    """HTMX endpoint for loading widget data asynchronously."""
    
    widget_class = widget_registry.get_widget(widget_id)
    if not widget_class:
        return JsonResponse({'error': 'Widget not found'}, status=404)
    
    widget_instance = widget_class(request=request)
    
    # Check permissions
    if not widget_instance.has_permission(request.user):
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    # Check cache first
    cache_key = f"widget_data_{widget_id}_{request.user.id}"
    cached_data = cache.get(cache_key)
    
    if cached_data is None:
        try:
            data = widget_instance.get_api_data()
            cache.set(cache_key, data, timeout=widget_instance.cache_timeout)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        data = cached_data
    
    if request.headers.get('HX-Request'):
        # Return rendered HTML for HTMX
        html = widget_instance.render()
        return JsonResponse({'html': html})
    else:
        # Return JSON data for API calls
        return JsonResponse(data)


@staff_member_required
def refresh_widget_view(request, widget_id):
    """Refresh a specific widget's data."""
    
    widget_class = widget_registry.get_widget(widget_id)
    if not widget_class:
        return JsonResponse({'error': 'Widget not found'}, status=404)
    
    widget_instance = widget_class(request=request)
    
    # Check permissions
    if not widget_instance.has_permission(request.user):
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    # Clear cache and get fresh data
    cache_key = f"widget_data_{widget_id}_{request.user.id}"
    cache.delete(cache_key)
    
    try:
        data = widget_instance.get_api_data()
        cache.set(cache_key, data, timeout=widget_instance.cache_timeout)
        
        if request.headers.get('HX-Request'):
            # Return rendered HTML for HTMX
            html = widget_instance.render()
            return JsonResponse({'html': html})
        else:
            # Return JSON data
            return JsonResponse(data)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@staff_member_required
def dashboard_settings_view(request):
    """View for dashboard settings and configuration."""
    
    if request.method == 'POST':
        # Handle settings updates
        try:
            data = json.loads(request.body)
            theme = data.get('theme', 'light')
            
            # Store user preferences (you might want to use a UserProfile model)
            request.session['dashboard_theme'] = theme
            
            return JsonResponse({'success': True})
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    # Get current settings
    config = get_dashboard_settings()
    user_theme = request.session.get('dashboard_theme', config.get('THEME', 'light'))
    
    return JsonResponse({
        'theme': user_theme,
        'config': config,
    })


@staff_member_required
def export_dashboard_data_view(request):
    """Export dashboard data as JSON."""
    
    config = get_dashboard_settings()
    enabled_widgets = widget_registry.get_enabled_widgets()
    
    export_data = {
        'config': config,
        'widgets': [],
        'timestamp': timezone.now().isoformat(),
    }
    
    for widget_class in enabled_widgets:
        widget_instance = widget_class(request=request)
        
        if widget_instance.has_permission(request.user):
            try:
                widget_data = widget_instance.get_api_data()
                widget_data['widget_id'] = getattr(widget_class, 'widget_id', widget_class.__name__)
                export_data['widgets'].append(widget_data)
            except Exception:
                # Skip widgets that fail to load
                continue
    
    response = JsonResponse(export_data)
    response['Content-Disposition'] = 'attachment; filename="dashboard_export.json"'
    return response
