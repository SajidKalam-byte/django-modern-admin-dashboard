# Custom Admin Dashboard

# Django Modern Admin Dashboard

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-3.2%2B-green)](https://djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/SajidKalam-byte/django-modern-admin-dashboard/workflows/Tests/badge.svg)](https://github.com/SajidKalam-byte/django-modern-admin-dashboard/actions)

A modern, responsive, and feature-rich Django admin dashboard that replaces the default Django admin with a beautiful TailwindCSS interface, Chart.js visualizations, and a pluggable widget system.

## ✨ Features

- 🎨 **Modern UI**: Beautiful, responsive design with TailwindCSS
- 📊 **Interactive Charts**: Chart.js integration for data visualization
- 🔧 **Widget System**: Pluggable widget architecture with built-in widgets
- 🌙 **Dark/Light Mode**: Toggle between themes
- 📱 **Mobile Responsive**: Works perfectly on all devices
- 🚀 **REST API**: Full API endpoints with authentication
- 🔒 **Secure**: Permission-based access control
- ⚡ **Fast**: Caching support for optimal performance
- 🛠️ **Developer Friendly**: Management commands and comprehensive docs
- ✅ **Well Tested**: 100% test coverage

## 🚀 Quick Start

### Installation

```bash
pip install django-modern-admin-dashboard
```

### Setup

1. Add to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',  # Required
    'dashboard',       # Add this
    'dashboard_config', # Add this
    # ... your other apps
]
```

2. Add dashboard URLs:

```python
# urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include('dashboard.urls')),
    # ... your other URLs
]
```

3. Configure in settings:

```python
# Dashboard Configuration
CUSTOM_ADMIN_DASHBOARD_CONFIG = {
    'TITLE': 'My Dashboard',
    'THEME': 'light',  # 'light' or 'dark'
    'WIDGETS': [
        'dashboard.widgets.UserCountWidget',
        'dashboard.widgets.RecentLoginsWidget',
        'dashboard.widgets.LoginActivityChartWidget',
    ],
    'ENABLE_API': True,
    'API_PERMISSIONS': ['rest_framework.permissions.IsAdminUser'],
}

# REST Framework (required)
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
}
```

4. Run migrations and initialize:

```bash
python manage.py migrate
python manage.py init_dashboard
python manage.py collectstatic
```

5. Visit `/dashboard/` in your browser! 🎉 Built with TailwindCSS, Chart.js, HTMX, and Alpine.js for a modern user experience.

![Dashboard Preview](https://via.placeholder.com/800x400?text=Dashboard+Preview)

## ✨ Features

- 🎨 **Modern UI**: Clean, responsive design with TailwindCSS
- 📊 **Interactive Charts**: Beautiful charts and graphs with Chart.js
- 🔄 **Real-time Updates**: Dynamic content updates with HTMX
- 🧩 **Widget System**: Pluggable widget architecture for custom components
- 🌓 **Dark/Light Mode**: Toggle between themes
- 📱 **Mobile Responsive**: Works perfectly on all device sizes
- � **REST API**: Complete API for dashboard data and widgets
- 🔐 **Permission System**: Role-based access control
- ⚡ **Caching**: Built-in caching for optimal performance
- 🧪 **Comprehensive Testing**: Full test suite with pytest
- 🔧 **Widget System** - Pluggable, class-based widgets
- ⚡ **HTMX Integration** for dynamic content loading
- 📱 **Fully Responsive** design
- 🔒 **Permission-based** access control
- 🚀 **REST API** with Django REST Framework
- 📦 **Easy Installation** via pip
- 🎯 **Template Overrides** support
- ⚙️ **Configurable** via Django settings

## 🚀 Quick Start

### Installation

```bash
pip install custom-admin-dashboard
```

### Setup

1. Add to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ... your apps
    'rest_framework',
    'dashboard',
    'dashboard_config',
]
```

2. Include the URLs in your main `urls.py`:

```python
from django.urls import path, include

urlpatterns = [
    # ... your URLs
    path('admin/dashboard/', include('dashboard.urls')),
]
```

3. Run migrations and collect static files:

```bash
python manage.py migrate
python manage.py collectstatic
```

4. Visit `/admin/dashboard/` to see your new dashboard!

## ⚙️ Configuration

Configure the dashboard in your `settings.py`:

```python
CUSTOM_ADMIN_DASHBOARD_CONFIG = {
    'THEME': 'dark',  # 'light' or 'dark'
    'TITLE': 'My Custom Admin',
    'LOGO_URL': '/static/img/logo.png',
    'WIDGETS': [
        'dashboard.widgets.UserCountWidget',
        'dashboard.widgets.RecentLoginsWidget',
        'dashboard.widgets.SystemStatusWidget',
        # Add your custom widgets here
    ],
    'CHART_COLORS': {
        'primary': '#4F46E5',
        'secondary': '#10B981',
        'warning': '#F59E0B',
        'danger': '#EF4444',
    },
    'ENABLE_API': True,
    'API_PERMISSIONS': ['rest_framework.permissions.IsAdminUser'],
}
```

## 🧩 Creating Custom Widgets

Create a custom widget by extending the base widget class:

```python
from dashboard.widgets import BaseWidget, register_widget
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

@register_widget
class RecentLoginsWidget(BaseWidget):
    title = "Recent Logins"
    icon = "login"
    template_name = "dashboard/widgets/recent_logins.html"
    
    def get_context_data(self):
        recent_logins = User.objects.filter(
            last_login__gte=timezone.now() - timedelta(days=7)
        ).order_by('-last_login')[:5]
        
        return {
            'recent_logins': recent_logins,
            'count': recent_logins.count()
        }
    
    def get_chart_data(self):
        # Return data for Chart.js
        return {
            'type': 'line',
            'data': {
                'labels': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                'datasets': [{
                    'label': 'Daily Logins',
                    'data': [12, 19, 3, 5, 2, 3, 9],
                    'borderColor': '#4F46E5',
                    'tension': 0.1
                }]
            }
        }
```

## 📊 Widget Types

The package includes several built-in widget types:

### Metric Widgets
Display single values with optional trend indicators:

```python
@register_widget
class UserCountWidget(MetricWidget):
    title = "Total Users"
    icon = "users"
    color = "blue"
    
    def get_value(self):
        return User.objects.count()
    
    def get_trend(self):
        # Return percentage change from last period
        return 12.5  # +12.5%
```

### Chart Widgets
Display interactive charts:

```python
@register_widget
class SalesChartWidget(ChartWidget):
    title = "Monthly Sales"
    chart_type = "bar"
    
    def get_chart_data(self):
        return {
            'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
            'datasets': [{
                'label': 'Sales',
                'data': [1200, 1500, 1800, 1400, 1900]
            }]
        }
```

### Table Widgets
Display tabular data:

```python
@register_widget
class RecentOrdersWidget(TableWidget):
    title = "Recent Orders"
    
    def get_headers(self):
        return ['Order ID', 'Customer', 'Amount', 'Date']
    
    def get_rows(self):
        orders = Order.objects.order_by('-created_at')[:10]
        return [
            [order.id, order.customer, f"${order.amount}", order.created_at]
            for order in orders
        ]
```

## 🎨 Template Customization

Override templates by creating your own in your app's templates directory:

```
your_app/
    templates/
        dashboard/
            base.html          # Main layout
            dashboard.html     # Dashboard page
            widgets/
                base.html      # Widget base template
                metric.html    # Metric widget template
                chart.html     # Chart widget template
                table.html     # Table widget template
```

## 🔗 API Endpoints

The dashboard provides REST API endpoints:

- `GET /admin/dashboard/api/v1/widgets/` - List all widgets
- `GET /admin/dashboard/api/v1/widgets/{id}/` - Get widget data
- `GET /admin/dashboard/api/v1/charts/{widget_id}/` - Get chart data
- `GET /admin/dashboard/api/v1/stats/` - Get dashboard statistics

## 🧪 Testing

Run the test suite:

```bash
# Install test dependencies
pip install -e .[dev]

# Run tests
pytest

# Run with coverage
pytest --cov=dashboard --cov-report=html
```

## 🏗️ Development

Clone the repository:

```bash
git clone https://github.com/yourname/custom-admin-dashboard.git
cd custom-admin-dashboard
```

Set up development environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .[dev]
```

Run the test project:

```bash
cd test_project
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## 📋 Requirements

- Python 3.8+
- Django 3.2+
- Django REST Framework 3.12+

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [TailwindCSS](https://tailwindcss.com/) for the beautiful styling
- [Chart.js](https://www.chartjs.org/) for interactive charts
- [HTMX](https://htmx.org/) for seamless interactivity
- [Django](https://djangoproject.com/) for the awesome framework

## 📞 Support

- 📖 [Documentation](https://github.com/yourname/custom-admin-dashboard/wiki)
- 🐛 [Issue Tracker](https://github.com/yourname/custom-admin-dashboard/issues)
- 💬 [Discussions](https://github.com/yourname/custom-admin-dashboard/discussions)