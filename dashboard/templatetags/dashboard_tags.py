"""
Template tags for the custom admin dashboard.
"""

from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
import json

from dashboard_config.settings import get_dashboard_settings, get_theme_config, get_chart_colors

register = template.Library()


@register.simple_tag
def dashboard_config(key=None, default=None):
    """Get dashboard configuration value."""
    config = get_dashboard_settings()
    if key:
        return config.get(key, default)
    return config


@register.simple_tag
def theme_class(theme_key, theme=None):
    """Get theme-specific CSS class."""
    theme_config = get_theme_config(theme)
    return theme_config.get(theme_key, '')


@register.simple_tag
def chart_color(color_name):
    """Get chart color by name."""
    colors = get_chart_colors()
    return colors.get(color_name, colors.get('primary', '#4F46E5'))


@register.filter
def to_json(value):
    """Convert value to JSON string."""
    return mark_safe(json.dumps(value))


@register.inclusion_tag('dashboard/widgets/widget_icon.html')
def widget_icon(icon_name, color='blue', size='w-5 h-5'):
    """Render widget icon."""
    return {
        'icon_name': icon_name,
        'color': color,
        'size': size,
    }


@register.simple_tag
def widget_refresh_url(widget_id):
    """Generate widget refresh URL."""
    from django.urls import reverse
    return reverse('dashboard:widget_refresh', kwargs={'widget_id': widget_id})


@register.filter
def widget_grid_class(config):
    """Generate grid CSS classes from widget config."""
    if not config:
        return 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3'
    
    cols = config.get('cols', {})
    gap = config.get('gap', 4)
    
    classes = [f'gap-{gap}']
    
    # Default columns
    classes.append(f"grid-cols-{cols.get('default', 1)}")
    
    # Responsive columns
    for breakpoint, count in cols.items():
        if breakpoint != 'default':
            classes.append(f"{breakpoint}:grid-cols-{count}")
    
    return ' '.join(classes)


@register.filter
def format_number(value):
    """Format large numbers with K, M, B suffixes."""
    if not isinstance(value, (int, float)):
        return value
    
    if value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.1f}B"
    elif value >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"
    elif value >= 1_000:
        return f"{value / 1_000:.1f}K"
    else:
        return str(int(value))


@register.filter
def trend_icon(trend_value):
    """Get trend icon based on value."""
    if not trend_value:
        return ''
    
    if trend_value > 0:
        return mark_safe('''
            <svg class="w-4 h-4 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M3.293 9.707a1 1 0 010-1.414l6-6a1 1 0 011.414 0l6 6a1 1 0 01-1.414 1.414L11 5.414V17a1 1 0 11-2 0V5.414L4.707 9.707a1 1 0 01-1.414 0z" clip-rule="evenodd"></path>
            </svg>
        ''')
    elif trend_value < 0:
        return mark_safe('''
            <svg class="w-4 h-4 text-red-500" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 10.293a1 1 0 010 1.414l-6 6a1 1 0 01-1.414 0l-6-6a1 1 0 111.414-1.414L9 14.586V3a1 1 0 012 0v11.586l4.293-4.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
            </svg>
        ''')
    else:
        return mark_safe('''
            <svg class="w-4 h-4 text-gray-500" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M3 10a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clip-rule="evenodd"></path>
            </svg>
        ''')


@register.filter
def trend_color_class(trend_value):
    """Get CSS color class for trend value."""
    if not trend_value:
        return 'text-gray-500 dark:text-gray-400'
    
    if trend_value > 0:
        return 'text-green-600 dark:text-green-400'
    elif trend_value < 0:
        return 'text-red-600 dark:text-red-400'
    else:
        return 'text-gray-500 dark:text-gray-400'


@register.simple_tag
def status_indicator(status, show_text=True):
    """Render status indicator with optional text."""
    status_config = {
        'healthy': {'color': 'bg-green-500', 'text': 'Healthy'},
        'warning': {'color': 'bg-yellow-500', 'text': 'Warning'},
        'error': {'color': 'bg-red-500', 'text': 'Error'},
        'inactive': {'color': 'bg-gray-500', 'text': 'Inactive'},
        'unknown': {'color': 'bg-gray-400', 'text': 'Unknown'},
    }
    
    config = status_config.get(status.lower(), status_config['unknown'])
    
    html = f'<span class="status-dot {config["color"]}"></span>'
    if show_text:
        html += f'<span>{config["text"]}</span>'
    
    return mark_safe(html)


@register.inclusion_tag('dashboard/components/loading_skeleton.html')
def loading_skeleton(height='h-6', width='w-full', rows=1):
    """Render loading skeleton."""
    return {
        'height': height,
        'width': width,
        'rows': rows,
    }


@register.simple_tag(takes_context=True)
def widget_permission_check(context, widget):
    """Check if current user has permission to view widget."""
    request = context.get('request')
    if not request or not hasattr(widget, 'has_permission'):
        return True
    
    return widget.has_permission(request.user)


@register.filter
def get_item(dictionary, key):
    """Get item from dictionary by key."""
    if not isinstance(dictionary, dict):
        return None
    return dictionary.get(key)


@register.simple_tag
def dashboard_version():
    """Get dashboard version."""
    return "1.0.0"


@register.simple_tag
def feature_enabled(feature_name):
    """Check if a feature is enabled."""
    from dashboard_config.settings import is_feature_enabled
    return is_feature_enabled(feature_name)


@register.filter
def multiply(value, arg):
    """Multiply filter for calculations in templates."""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0


@register.filter
def percentage(value, total):
    """Calculate percentage."""
    try:
        if total == 0:
            return 0
        return round((float(value) / float(total)) * 100, 1)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0
