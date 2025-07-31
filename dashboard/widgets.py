"""
Widget system for the custom admin dashboard.
"""

import json
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django.template.loader import render_to_string
from django.conf import settings


class WidgetRegistry:
    """Registry to manage dashboard widgets."""
    
    def __init__(self):
        self._widgets = {}
    
    def register(self, widget_class):
        """Register a widget class."""
        # Try to get the widget_id from a class attribute first
        if hasattr(widget_class, 'widget_id') and isinstance(widget_class.widget_id, str):
            widget_id = widget_class.widget_id
        else:
            # Create an instance to get the widget_id property
            try:
                widget_instance = widget_class()
                widget_id = widget_instance.widget_id
            except:
                # Fallback to lowercase class name
                widget_id = widget_class.__name__.lower()
        
        self._widgets[widget_id] = widget_class
        return widget_class
    
    def get_widget(self, widget_id):
        """Get a widget class by ID."""
        return self._widgets.get(widget_id)
    
    def get_all_widgets(self):
        """Get all registered widgets."""
        return self._widgets.values()
    
    def get_enabled_widgets(self):
        """Get widgets enabled in settings."""
        config = getattr(settings, 'CUSTOM_ADMIN_DASHBOARD_CONFIG', {})
        enabled_widget_names = config.get('WIDGETS', None)
        
        # If WIDGETS is explicitly set to empty list, return empty list
        if enabled_widget_names is not None and not enabled_widget_names:
            return []
        
        # If WIDGETS is not set, return default widgets
        if enabled_widget_names is None:
            return list(self._widgets.values())
        
        enabled_widgets = []
        for widget_name in enabled_widget_names:
            # Support both class name and full path
            if '.' in widget_name:
                widget_class_name = widget_name.split('.')[-1]
            else:
                widget_class_name = widget_name
            
            # Find widget by class name
            for widget_id, widget_class in self._widgets.items():
                if widget_class.__name__ == widget_class_name:
                    enabled_widgets.append(widget_class)
                    break
        
        return enabled_widgets


# Global widget registry
widget_registry = WidgetRegistry()


def register_widget(widget_class):
    """Decorator to register a widget."""
    return widget_registry.register(widget_class)


class BaseWidget(ABC):
    """Base class for all dashboard widgets."""
    
    # Widget metadata
    title = "Untitled Widget"
    description = ""
    icon = "chart-bar"
    color = "blue"
    widget_type = "base"
    template_name = "dashboard/widgets/base.html"
    
    @property
    def widget_id(self):
        """Get the widget ID."""
        return getattr(self, '_widget_id', None) or self.__class__.__name__.lower()
    
    # Widget configuration
    refresh_interval = 300  # 5 minutes in seconds
    cache_timeout = 60  # 1 minute
    requires_permissions = []
    
    def __init__(self, request=None):
        self.request = request
    
    @abstractmethod
    def get_context_data(self):
        """Return context data for the widget template."""
        pass
    
    def get_value(self):
        """Return the main value for simple metric widgets."""
        return None
    
    def get_chart_data(self):
        """Return Chart.js compatible data for chart widgets."""
        return None
    
    def get_api_data(self):
        """Return data for API endpoints."""
        context = self.get_context_data()
        return {
            'title': self.title,
            'value': self.get_value(),
            'chart_data': self.get_chart_data(),
            'context': context,
        }
    
    def render(self):
        """Render the widget HTML."""
        context = {
            'widget': self,
            'title': self.title,
            'description': self.description,
            'icon': self.icon,
            'color': self.color,
            'value': self.get_value(),
            'chart_data': json.dumps(self.get_chart_data()) if self.get_chart_data() else None,
            **self.get_context_data()
        }
        return render_to_string(self.template_name, context, request=self.request)
    
    def has_permission(self, user):
        """Check if user has permission to view this widget."""
        if not self.requires_permissions:
            return user.is_staff
        
        for permission in self.requires_permissions:
            if not user.has_perm(permission):
                return False
        return True


class MetricWidget(BaseWidget):
    """Widget for displaying single metrics with optional trends."""
    
    widget_type = "metric"
    template_name = "dashboard/widgets/metric.html"
    
    def get_trend(self):
        """Return trend percentage (positive/negative)."""
        return None
    
    def get_trend_period(self):
        """Return the period for trend calculation."""
        return "vs last period"
    
    def get_context_data(self):
        return {
            'trend': self.get_trend(),
            'trend_period': self.get_trend_period(),
        }


class ChartWidget(BaseWidget):
    """Widget for displaying charts."""
    
    widget_type = "chart"
    chart_type = "line"  # line, bar, pie, doughnut
    template_name = "dashboard/widgets/chart.html"
    
    def get_context_data(self):
        return {
            'chart_type': self.chart_type,
        }


class TableWidget(BaseWidget):
    """Widget for displaying tabular data."""
    
    widget_type = "table"
    template_name = "dashboard/widgets/table.html"
    max_rows = 10
    
    def get_headers(self):
        """Return table headers."""
        return []
    
    def get_rows(self):
        """Return table rows."""
        return []
    
    def get_context_data(self):
        return {
            'headers': self.get_headers(),
            'rows': self.get_rows()[:self.max_rows],
        }


# Built-in widgets

@register_widget
class UserCountWidget(MetricWidget):
    """Widget showing total user count."""
    
    widget_id = "user_count"
    title = "Total Users"
    description = "Total number of registered users"
    icon = "users"
    color = "blue"
    
    def get_value(self):
        return User.objects.count()
    
    def get_trend(self):
        # Calculate trend compared to last week
        week_ago = timezone.now() - timedelta(days=7)
        current_count = User.objects.count()
        previous_count = User.objects.filter(date_joined__lt=week_ago).count()
        
        if previous_count == 0:
            return 100 if current_count > 0 else 0
        
        return round(((current_count - previous_count) / previous_count) * 100, 1)
    
    def get_context_data(self):
        context = super().get_context_data()
        context.update({
            'active_users': User.objects.filter(is_active=True).count(),
            'new_this_week': User.objects.filter(
                date_joined__gte=timezone.now() - timedelta(days=7)
            ).count(),
        })
        return context


@register_widget
class RecentLoginsWidget(TableWidget):
    """Widget showing recent user logins."""
    
    widget_id = "recent_logins"
    title = "Recent Logins"
    description = "Latest user login activity"
    icon = "login"
    color = "green"
    max_rows = 5
    
    def get_headers(self):
        return ['Username', 'Email', 'Last Login', 'Status']
    
    def get_rows(self):
        recent_users = User.objects.filter(
            last_login__isnull=False
        ).order_by('-last_login')[:self.max_rows]
        
        rows = []
        for user in recent_users:
            status = "Active" if user.is_active else "Inactive"
            last_login = user.last_login.strftime('%Y-%m-%d %H:%M') if user.last_login else 'Never'
            rows.append([
                user.username,
                user.email,
                last_login,
                status
            ])
        
        return rows


@register_widget
class LoginActivityChartWidget(ChartWidget):
    """Widget showing login activity over time."""
    
    widget_id = "login_activity_chart"
    title = "Login Activity"
    description = "Daily login activity for the past week"
    icon = "chart-line"
    color = "purple"
    chart_type = "line"
    
    def get_chart_data(self):
        # Generate daily login data for the past 7 days
        labels = []
        data = []
        
        for i in range(6, -1, -1):
            date = timezone.now().date() - timedelta(days=i)
            labels.append(date.strftime('%m/%d'))
            
            # Count users who logged in on this date
            daily_logins = User.objects.filter(
                last_login__date=date
            ).count()
            data.append(daily_logins)
        
        return {
            'type': 'line',
            'data': {
                'labels': labels,
                'datasets': [{
                    'label': 'Daily Logins',
                    'data': data,
                    'borderColor': '#8B5CF6',
                    'backgroundColor': 'rgba(139, 92, 246, 0.1)',
                    'tension': 0.4,
                    'fill': True
                }]
            },
            'options': {
                'responsive': True,
                'plugins': {
                    'legend': {
                        'display': False
                    }
                },
                'scales': {
                    'y': {
                        'beginAtZero': True,
                        'ticks': {
                            'stepSize': 1
                        }
                    }
                }
            }
        }


@register_widget
class SystemStatusWidget(MetricWidget):
    """Widget showing system status."""
    
    widget_id = "system_status"
    title = "System Status"
    description = "Overall system health"
    icon = "server"
    color = "green"
    
    def get_value(self):
        return "Healthy"
    
    def get_context_data(self):
        # You can add more complex system checks here
        return {
            'uptime': "99.9%",
            'last_backup': timezone.now() - timedelta(hours=2),
            'database_status': "Connected",
            'cache_status': "Active",
        }


@register_widget
class UserRegistrationChartWidget(ChartWidget):
    """Widget showing user registration trends."""
    
    widget_id = "user_registration_chart"
    title = "User Registrations"
    description = "Monthly user registration trends"
    icon = "user-plus"
    color = "indigo"
    chart_type = "bar"
    
    def get_chart_data(self):
        # Get registration data for the past 6 months
        labels = []
        data = []
        
        for i in range(5, -1, -1):
            date = timezone.now().replace(day=1) - timedelta(days=32*i)
            month_start = date.replace(day=1)
            month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            
            labels.append(month_start.strftime('%b %Y'))
            
            monthly_registrations = User.objects.filter(
                date_joined__gte=month_start,
                date_joined__lte=month_end
            ).count()
            data.append(monthly_registrations)
        
        return {
            'type': 'bar',
            'data': {
                'labels': labels,
                'datasets': [{
                    'label': 'New Users',
                    'data': data,
                    'backgroundColor': '#6366F1',
                    'borderColor': '#4F46E5',
                    'borderWidth': 1
                }]
            },
            'options': {
                'responsive': True,
                'plugins': {
                    'legend': {
                        'display': False
                    }
                },
                'scales': {
                    'y': {
                        'beginAtZero': True,
                        'ticks': {
                            'stepSize': 1
                        }
                    }
                }
            }
        }
    
    def get_context_data(self):
        context = super().get_context_data()
        
        # Add summary stats
        this_month = User.objects.filter(
            date_joined__gte=timezone.now().replace(day=1)
        ).count()
        
        last_month_start = (timezone.now().replace(day=1) - timedelta(days=1)).replace(day=1)
        last_month_end = timezone.now().replace(day=1) - timedelta(days=1)
        last_month = User.objects.filter(
            date_joined__gte=last_month_start,
            date_joined__lte=last_month_end
        ).count()
        
        context.update({
            'this_month': this_month,
            'last_month': last_month,
        })
        
        return context


@register_widget
class QuickActionsWidget(BaseWidget):
    """Quick actions widget for common admin tasks."""
    
    widget_id = "quick_actions"
    title = "Quick Actions"
    description = "Common administrative actions"
    icon = "lightning-bolt"
    color = "green"
    template_name = "dashboard/widgets/quick_actions.html"
    
    def get_context_data(self):
        """Return context data for quick actions."""
        actions = [
            {
                'name': 'Add User',
                'url': '/admin/auth/user/add/',
                'icon': 'user-plus',
                'description': 'Create a new user account'
            },
            {
                'name': 'View Users',
                'url': '/admin/auth/user/',
                'icon': 'users',
                'description': 'Manage user accounts'
            },
            {
                'name': 'Site Settings',
                'url': '/admin/',
                'icon': 'cog',
                'description': 'Configure site settings'
            },
        ]
        
        return {
            'actions': actions,
            'total_actions': len(actions)
        }


# Alias for backward compatibility
UserStatsWidget = UserCountWidget


def get_dashboard_widgets():
    """
    Get all registered dashboard widgets.
    Returns a dictionary of widget instances.
    """
    return widget_registry.get_enabled_widgets()


def get_widget_instances():
    """
    Get instances of all registered widgets.
    Returns a dictionary mapping widget_id to widget instance.
    """
    widgets = {}
    for widget_class in widget_registry.get_enabled_widgets():
        try:
            widget = widget_class()
            widgets[widget.widget_id] = widget
        except Exception as e:
            # Skip widgets that can't be instantiated
            continue
    return widgets
