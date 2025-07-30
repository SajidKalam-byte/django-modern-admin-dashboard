"""
Views for the custom admin dashboard.
"""

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
