# API Reference

## Overview

The Custom Admin Dashboard provides a comprehensive REST API for accessing dashboard data, widget information, and system statistics. The API follows RESTful conventions and returns JSON responses.

## Authentication

All API endpoints require authentication. The dashboard uses Django's session authentication by default, but you can configure custom authentication methods.

### Default Authentication

```python
# Built-in authentication
# Users must be logged in and have staff privileges
```

### Custom Authentication

Configure custom authentication in settings:

```python
CUSTOM_ADMIN_DASHBOARD_CONFIG = {
    'API_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
        'myapp.permissions.CustomPermission',
    ]
}
```

## Base URL

All API endpoints are prefixed with:
```
/admin/dashboard/api/
```

## Endpoints

### Dashboard Statistics

#### GET /stats/
Get overall dashboard statistics.

**Response:**
```json
{
    "total_widgets": 5,
    "active_widgets": 4,
    "last_updated": "2024-01-15T10:30:00Z",
    "user_count": 150,
    "system_status": "healthy"
}
```

**Example:**
```javascript
fetch('/admin/dashboard/api/stats/')
    .then(response => response.json())
    .then(data => console.log(data));
```

### Widgets

#### GET /widgets/
List all available widgets.

**Parameters:**
- `active` (boolean): Filter by active widgets only

**Response:**
```json
{
    "count": 4,
    "results": [
        {
            "id": "user_count",
            "title": "User Count",
            "subtitle": "Total registered users",
            "type": "metric",
            "is_active": true,
            "last_updated": "2024-01-15T10:30:00Z"
        },
        {
            "id": "recent_logins",
            "title": "Recent Logins",
            "subtitle": "Users logged in today",
            "type": "table",
            "is_active": true,
            "last_updated": "2024-01-15T10:25:00Z"
        }
    ]
}
```

#### GET /widgets/{widget_id}/
Get detailed information about a specific widget.

**Response:**
```json
{
    "id": "user_count",
    "title": "User Count",
    "subtitle": "Total registered users",
    "type": "metric",
    "is_active": true,
    "data": {
        "value": 150,
        "change": 12.5,
        "trend": [140, 142, 145, 148, 150]
    },
    "last_updated": "2024-01-15T10:30:00Z",
    "cache_timeout": 300
}
```

#### GET /widgets/{widget_id}/data/
Get only the data for a specific widget (useful for AJAX updates).

**Response:**
```json
{
    "value": 150,
    "change": 12.5,
    "trend": [140, 142, 145, 148, 150],
    "last_updated": "2024-01-15T10:30:00Z"
}
```

### Chart Data

#### GET /charts/{widget_id}/
Get chart data for chart widgets.

**Response:**
```json
{
    "data": {
        "labels": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "datasets": [{
            "label": "User Registrations",
            "data": [12, 19, 3, 5, 2, 3, 9],
            "borderColor": "rgb(59, 130, 246)",
            "backgroundColor": "rgba(59, 130, 246, 0.1)"
        }]
    },
    "options": {
        "responsive": true,
        "scales": {
            "y": {
                "beginAtZero": true
            }
        }
    }
}
```

### Health Check

#### GET /health/
Check the health status of the dashboard API.

**Response:**
```json
{
    "status": "healthy",
    "timestamp": "2024-01-15T10:30:00Z",
    "version": "1.0.0",
    "database": "connected",
    "cache": "available"
}
```

## Error Responses

The API returns standard HTTP status codes and error messages:

### 400 Bad Request
```json
{
    "error": "Invalid widget_id provided",
    "code": "INVALID_WIDGET"
}
```

### 401 Unauthorized
```json
{
    "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
    "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
    "error": "Widget not found",
    "code": "WIDGET_NOT_FOUND"
}
```

### 500 Internal Server Error
```json
{
    "error": "Internal server error",
    "code": "INTERNAL_ERROR"
}
```

## JavaScript Client Examples

### Fetch Widget Data

```javascript
async function getWidgetData(widgetId) {
    try {
        const response = await fetch(`/admin/dashboard/api/widgets/${widgetId}/data/`);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return await response.json();
    } catch (error) {
        console.error('Error fetching widget data:', error);
        return null;
    }
}

// Usage
getWidgetData('user_count').then(data => {
    if (data) {
        document.getElementById('user-count-value').textContent = data.value;
    }
});
```

### Update Chart

```javascript
async function updateChart(widgetId, chartInstance) {
    const data = await fetch(`/admin/dashboard/api/charts/${widgetId}/`)
        .then(response => response.json());
    
    chartInstance.data = data.data;
    chartInstance.options = { ...chartInstance.options, ...data.options };
    chartInstance.update();
}
```

### Refresh All Widgets

```javascript
async function refreshAllWidgets() {
    const widgets = await fetch('/admin/dashboard/api/widgets/')
        .then(response => response.json());
    
    for (const widget of widgets.results) {
        if (widget.is_active) {
            const data = await getWidgetData(widget.id);
            updateWidgetDisplay(widget.id, data);
        }
    }
}

function updateWidgetDisplay(widgetId, data) {
    const element = document.querySelector(`[data-widget-id="${widgetId}"]`);
    if (element && data) {
        // Update the widget display with new data
        const valueElement = element.querySelector('.widget-value');
        if (valueElement) {
            valueElement.textContent = data.value;
        }
        
        const changeElement = element.querySelector('.widget-change');
        if (changeElement && data.change !== undefined) {
            changeElement.textContent = `${data.change > 0 ? '+' : ''}${data.change.toFixed(1)}%`;
            changeElement.className = `widget-change ${data.change >= 0 ? 'positive' : 'negative'}`;
        }
    }
}
```

## Python Client Examples

### Using requests

```python
import requests
from django.conf import settings

class DashboardAPIClient:
    def __init__(self, base_url=None, session=None):
        self.base_url = base_url or '/admin/dashboard/api/'
        self.session = session or requests.Session()
    
    def get_widgets(self, active_only=True):
        params = {'active': 'true'} if active_only else {}
        response = self.session.get(f'{self.base_url}widgets/', params=params)
        response.raise_for_status()
        return response.json()
    
    def get_widget_data(self, widget_id):
        response = self.session.get(f'{self.base_url}widgets/{widget_id}/data/')
        response.raise_for_status()
        return response.json()
    
    def get_dashboard_stats(self):
        response = self.session.get(f'{self.base_url}stats/')
        response.raise_for_status()
        return response.json()

# Usage
client = DashboardAPIClient()
widgets = client.get_widgets()
user_count_data = client.get_widget_data('user_count')
```

### Using Django's test client

```python
from django.test import TestCase, Client
from django.contrib.auth.models import User

class APITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('admin', 'admin@example.com', 'password')
        self.user.is_staff = True
        self.user.save()
        self.client.login(username='admin', password='password')
    
    def test_get_widgets(self):
        response = self.client.get('/admin/dashboard/api/widgets/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('results', data)
    
    def test_get_widget_data(self):
        response = self.client.get('/admin/dashboard/api/widgets/user_count/data/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('value', data)
```

## Rate Limiting

The API includes basic rate limiting to prevent abuse:

- **Default**: 100 requests per minute per user
- **Burst**: Up to 20 requests in 10 seconds

Configure rate limiting in settings:

```python
CUSTOM_ADMIN_DASHBOARD_CONFIG = {
    'API_RATE_LIMIT': '100/min',
    'API_BURST_LIMIT': '20/10s',
}
```

## Pagination

List endpoints support pagination:

```json
{
    "count": 50,
    "next": "http://example.com/admin/dashboard/api/widgets/?page=2",
    "previous": null,
    "results": [...]
}
```

**Parameters:**
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20, max: 100)

## Filtering and Searching

### Widget Filtering

```http
GET /admin/dashboard/api/widgets/?type=metric&active=true
```

**Available filters:**
- `type`: metric, chart, table
- `active`: true, false
- `search`: Search in title and subtitle

### Date Range Filtering

For widgets that support time-based data:

```http
GET /admin/dashboard/api/widgets/chart_widget/data/?start_date=2024-01-01&end_date=2024-01-31
```

## Webhooks

Configure webhooks to receive notifications when widget data changes:

```python
CUSTOM_ADMIN_DASHBOARD_CONFIG = {
    'WEBHOOKS': {
        'widget_updated': 'https://your-app.com/webhook/widget-updated/',
        'dashboard_error': 'https://your-app.com/webhook/error/',
    }
}
```

## API Versioning

The API supports versioning through URL paths:

- `/admin/dashboard/api/v1/` - Version 1 (current)
- `/admin/dashboard/api/v2/` - Version 2 (future)

Default version is v1. Specify version in requests:

```javascript
fetch('/admin/dashboard/api/v1/widgets/')
```

## CORS Configuration

For cross-origin requests, configure CORS:

```python
# settings.py
INSTALLED_APPS = [
    'corsheaders',
    # ... other apps
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    # ... other middleware
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://your-frontend.com",
]

# Or for development
CORS_ALLOW_ALL_ORIGINS = True
```

## Security Considerations

1. **Always use HTTPS** in production
2. **Validate API keys** if using token authentication
3. **Implement proper CORS** settings
4. **Monitor API usage** for unusual patterns
5. **Keep dependencies updated** for security patches

## OpenAPI Schema

The API provides an OpenAPI/Swagger schema:

```http
GET /admin/dashboard/api/schema/
```

Use this with tools like Swagger UI or Postman for interactive API documentation.
