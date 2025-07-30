# Creating Custom Widgets

## Widget Overview

Widgets are the core components of the dashboard. They display data in various formats like metrics, charts, and tables. The dashboard provides a flexible widget system that allows you to create custom widgets for your specific needs.

## Widget Types

The dashboard includes several base widget types:

- **BaseWidget**: Abstract base class for all widgets
- **MetricWidget**: For displaying single metrics with optional trends
- **ChartWidget**: For displaying charts and graphs
- **TableWidget**: For displaying tabular data with pagination

## Creating Your First Widget

### Using the Management Command

The easiest way to create a new widget is using the built-in management command:

```bash
python manage.py create_dashboard_widget MyCustomWidget --type metric --app myapp
```

This creates a basic widget template that you can customize.

### Manual Widget Creation

Create a new widget by inheriting from one of the base widget classes:

```python
# myapp/widgets.py
from dashboard.widgets import MetricWidget
from django.contrib.auth.models import User

class ActiveUsersWidget(MetricWidget):
    title = "Active Users"
    subtitle = "Users active in the last 24 hours"
    icon = "fa fa-users"
    color = "blue"
    
    def get_value(self):
        from django.utils import timezone
        from datetime import timedelta
        
        yesterday = timezone.now() - timedelta(days=1)
        return User.objects.filter(last_login__gte=yesterday).count()
    
    def get_change(self):
        # Optional: Return percentage change from previous period
        from django.utils import timezone
        from datetime import timedelta
        
        yesterday = timezone.now() - timedelta(days=1)
        day_before = timezone.now() - timedelta(days=2)
        
        current = User.objects.filter(last_login__gte=yesterday).count()
        previous = User.objects.filter(
            last_login__gte=day_before,
            last_login__lt=yesterday
        ).count()
        
        if previous == 0:
            return 0
        return ((current - previous) / previous) * 100
```

## Widget Types in Detail

### MetricWidget

Perfect for displaying single values with optional change indicators:

```python
from dashboard.widgets import MetricWidget

class SalesMetricWidget(MetricWidget):
    title = "Total Sales"
    subtitle = "This month"
    icon = "fa fa-dollar-sign"
    color = "green"
    
    def get_value(self):
        # Return the main metric value
        from myapp.models import Sale
        return Sale.objects.filter(
            created_at__month=timezone.now().month
        ).aggregate(total=Sum('amount'))['total'] or 0
    
    def get_change(self):
        # Return percentage change (optional)
        # Positive values show as green, negative as red
        return 12.5
    
    def get_trend_data(self):
        # Return data for mini trend chart (optional)
        return [10, 15, 8, 22, 18, 25, 30]
```

### ChartWidget

For displaying charts using Chart.js:

```python
from dashboard.widgets import ChartWidget

class UserRegistrationChartWidget(ChartWidget):
    title = "User Registrations"
    subtitle = "Last 7 days"
    chart_type = "line"  # line, bar, pie, doughnut
    
    def get_chart_data(self):
        from django.contrib.auth.models import User
        from django.utils import timezone
        from datetime import timedelta
        
        # Generate data for the last 7 days
        data = []
        labels = []
        
        for i in range(7):
            date = timezone.now() - timedelta(days=i)
            count = User.objects.filter(
                date_joined__date=date.date()
            ).count()
            
            data.append(count)
            labels.append(date.strftime('%m/%d'))
        
        return {
            'labels': list(reversed(labels)),
            'datasets': [{
                'label': 'Registrations',
                'data': list(reversed(data)),
                'borderColor': 'rgb(59, 130, 246)',
                'backgroundColor': 'rgba(59, 130, 246, 0.1)',
                'tension': 0.4
            }]
        }
    
    def get_chart_options(self):
        # Optional: Customize chart appearance
        return {
            'responsive': True,
            'scales': {
                'y': {
                    'beginAtZero': True
                }
            }
        }
```

### TableWidget

For displaying tabular data with pagination:

```python
from dashboard.widgets import TableWidget

class RecentOrdersWidget(TableWidget):
    title = "Recent Orders"
    subtitle = "Last 10 orders"
    
    def get_headers(self):
        return ['Order ID', 'Customer', 'Amount', 'Status', 'Date']
    
    def get_data(self):
        from myapp.models import Order
        
        orders = Order.objects.select_related('customer').order_by('-created_at')[:10]
        
        return [
            [
                order.id,
                order.customer.username,
                f"${order.total_amount}",
                order.get_status_display(),
                order.created_at.strftime('%m/%d/%Y')
            ]
            for order in orders
        ]
    
    def get_row_actions(self):
        # Optional: Add action buttons to each row
        return [
            {
                'name': 'view',
                'label': 'View',
                'url_pattern': '/admin/orders/{}/view/',
                'icon': 'fa fa-eye',
                'css_class': 'btn-primary'
            },
            {
                'name': 'edit',
                'label': 'Edit',
                'url_pattern': '/admin/orders/{}/edit/',
                'icon': 'fa fa-edit',
                'css_class': 'btn-secondary'
            }
        ]
```

## Advanced Widget Features

### Caching

Enable caching to improve performance:

```python
class ExpensiveWidget(MetricWidget):
    title = "Complex Calculation"
    cache_timeout = 900  # Cache for 15 minutes
    
    def get_value(self):
        # This expensive calculation will be cached
        return self.expensive_calculation()
```

### Permissions

Control widget visibility based on user permissions:

```python
class AdminOnlyWidget(MetricWidget):
    title = "Admin Data"
    required_permissions = ['auth.view_user', 'auth.change_user']
    
    def has_permission(self, user):
        # Custom permission logic
        return user.is_superuser
```

### AJAX Updates

Make widgets update dynamically:

```python
class LiveWidget(MetricWidget):
    title = "Live Data"
    refresh_interval = 30  # Refresh every 30 seconds
    auto_refresh = True
```

### Custom Templates

Override the default widget template:

```python
class CustomWidget(MetricWidget):
    template_name = 'dashboard/widgets/custom_widget.html'
    
    def get_context_data(self):
        context = super().get_context_data()
        context['custom_data'] = self.get_custom_data()
        return context
```

## Registering Widgets

### Manual Registration

Register widgets in your app's `ready()` method:

```python
# myapp/apps.py
from django.apps import AppConfig

class MyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'
    
    def ready(self):
        from dashboard.widgets import widget_registry
        from .widgets import ActiveUsersWidget, SalesMetricWidget
        
        widget_registry.register('active_users', ActiveUsersWidget)
        widget_registry.register('sales_metric', SalesMetricWidget)
```

### Configuration Registration

Add widgets to your settings:

```python
CUSTOM_ADMIN_DASHBOARD_CONFIG = {
    'WIDGETS': [
        'myapp.widgets.ActiveUsersWidget',
        'myapp.widgets.SalesMetricWidget',
    ]
}
```

## Widget Best Practices

### Performance

1. **Use caching** for expensive operations:
   ```python
   cache_timeout = 300  # 5 minutes
   ```

2. **Optimize database queries**:
   ```python
   def get_value(self):
       return User.objects.select_related('profile').count()
   ```

3. **Use aggregation** instead of Python loops:
   ```python
   def get_value(self):
       return Order.objects.aggregate(total=Sum('amount'))['total']
   ```

### User Experience

1. **Provide meaningful titles and subtitles**:
   ```python
   title = "Active Sessions"
   subtitle = "Users currently online"
   ```

2. **Use appropriate colors and icons**:
   ```python
   icon = "fa fa-chart-line"
   color = "green"  # or "blue", "red", "yellow", "purple"
   ```

3. **Include trend indicators** when relevant:
   ```python
   def get_change(self):
       return 15.3  # +15.3% change
   ```

### Error Handling

1. **Handle errors gracefully**:
   ```python
   def get_value(self):
       try:
           return self.expensive_calculation()
       except Exception as e:
           logger.error(f"Widget error: {e}")
           return 0
   ```

2. **Provide fallback values**:
   ```python
   def get_value(self):
       result = Model.objects.aggregate(total=Sum('field'))['total']
       return result or 0
   ```

## Testing Widgets

Create tests for your widgets:

```python
# tests/test_widgets.py
from django.test import TestCase
from django.contrib.auth.models import User
from myapp.widgets import ActiveUsersWidget

class ActiveUsersWidgetTest(TestCase):
    def setUp(self):
        self.widget = ActiveUsersWidget()
        
    def test_widget_value(self):
        User.objects.create_user('test', 'test@example.com', 'password')
        self.assertEqual(self.widget.get_value(), 1)
        
    def test_widget_rendering(self):
        html = self.widget.render()
        self.assertIn('Active Users', html)
```

## Widget Examples

Check the `dashboard/widgets.py` file for complete examples of all widget types, including:

- `UserCountWidget` - Simple metric widget
- `RecentLoginsWidget` - Table widget with user data
- `LoginActivityChartWidget` - Chart widget with time series data
- `SystemStatusWidget` - Custom widget with health checks

These examples demonstrate best practices and can serve as templates for your own widgets.
