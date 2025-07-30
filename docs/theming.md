# Theming and Customization Guide

## Overview

The Custom Admin Dashboard is designed to be highly customizable. You can modify colors, layouts, fonts, and overall appearance to match your brand or preferences.

## Theme Configuration

### Basic Theme Settings

Configure the basic theme through settings:

```python
CUSTOM_ADMIN_DASHBOARD_CONFIG = {
    'THEME': 'dark',  # 'light' or 'dark'
    'TITLE': 'My Company Dashboard',
    'SUBTITLE': 'Administrative Portal',
    'LOGO_URL': '/static/images/my-logo.png',
}
```

### Dark and Light Mode

The dashboard automatically supports both dark and light themes. Users can toggle between them using the theme switcher in the header.

#### Customizing Theme Colors

Create a custom CSS file to override default theme colors:

```css
/* static/dashboard/css/custom-theme.css */

:root {
    /* Light theme colors */
    --primary-50: #eff6ff;
    --primary-100: #dbeafe;
    --primary-500: #3b82f6;
    --primary-600: #2563eb;
    --primary-700: #1d4ed8;
    
    /* Success colors */
    --success-50: #f0fdf4;
    --success-500: #22c55e;
    --success-600: #16a34a;
    
    /* Warning colors */
    --warning-50: #fffbeb;
    --warning-500: #f59e0b;
    --warning-600: #d97706;
    
    /* Error colors */
    --error-50: #fef2f2;
    --error-500: #ef4444;
    --error-600: #dc2626;
}

[data-theme="dark"] {
    /* Dark theme colors */
    --primary-50: #1e293b;
    --primary-100: #334155;
    --primary-500: #6366f1;
    --primary-600: #4f46e5;
    --primary-700: #4338ca;
    
    /* Background colors for dark theme */
    --bg-primary: #0f172a;
    --bg-secondary: #1e293b;
    --text-primary: #f8fafc;
    --text-secondary: #cbd5e1;
}
```

Include your custom CSS:

```python
CUSTOM_ADMIN_DASHBOARD_CONFIG = {
    'EXTRA_CSS': [
        'dashboard/css/custom-theme.css',
    ],
}
```

## Custom Templates

### Override Base Template

Create your own base template to customize the overall layout:

```html
<!-- templates/dashboard/base.html -->
{% extends "dashboard/base.html" %}

{% block extra_head %}
    <link rel="stylesheet" href="{% static 'dashboard/css/custom.css' %}">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
{% endblock %}

{% block header_brand %}
    <div class="flex items-center space-x-3">
        <img src="{% static 'images/logo.png' %}" alt="Logo" class="h-8 w-8">
        <div>
            <h1 class="text-xl font-bold text-gray-900 dark:text-white">
                {{ config.TITLE|default:"My Dashboard" }}
            </h1>
            <p class="text-sm text-gray-500 dark:text-gray-400">
                {{ config.SUBTITLE|default:"Admin Portal" }}
            </p>
        </div>
    </div>
{% endblock %}

{% block footer %}
    <footer class="bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 py-4">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center">
                <p class="text-sm text-gray-500 dark:text-gray-400">
                    © 2024 My Company. All rights reserved.
                </p>
                <div class="flex space-x-4">
                    <a href="#" class="text-sm text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200">
                        Privacy Policy
                    </a>
                    <a href="#" class="text-sm text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200">
                        Terms of Service
                    </a>
                </div>
            </div>
        </div>
    </footer>
{% endblock %}
```

### Custom Dashboard Layout

Override the main dashboard template:

```html
<!-- templates/dashboard/dashboard.html -->
{% extends "dashboard/base.html" %}
{% load static %}

{% block title %}{{ config.TITLE|default:"Dashboard" }}{% endblock %}

{% block content %}
<div class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <!-- Custom header section -->
    <div class="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700 mb-6">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
            <div class="flex justify-between items-center">
                <div>
                    <h1 class="text-2xl font-bold text-gray-900 dark:text-white">
                        Welcome to {{ config.TITLE|default:"Dashboard" }}
                    </h1>
                    <p class="text-gray-600 dark:text-gray-400">
                        Monitor and manage your application
                    </p>
                </div>
                <div class="flex space-x-3">
                    <button class="btn btn-primary">
                        <i class="fas fa-plus mr-2"></i>
                        Add New
                    </button>
                    <button class="btn btn-secondary">
                        <i class="fas fa-download mr-2"></i>
                        Export
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- Widgets grid -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-{{ config.WIDGET_GRID_COLS|default:3 }} gap-6">
            {% for widget in widgets %}
                <div class="widget-container" data-widget-id="{{ widget.id }}">
                    {{ widget.render }}
                </div>
            {% endfor %}
        </div>
    </div>
</div>
{% endblock %}
```

## Custom Widget Templates

### Override Widget Templates

Create custom templates for specific widget types:

```html
<!-- templates/dashboard/widgets/metric_widget.html -->
<div class="bg-gradient-to-br from-{{ widget.color }}-500 to-{{ widget.color }}-600 rounded-lg shadow-lg p-6 text-white">
    <div class="flex items-center justify-between">
        <div>
            <h3 class="text-lg font-semibold opacity-90">{{ widget.title }}</h3>
            <p class="text-sm opacity-75">{{ widget.subtitle }}</p>
        </div>
        <div class="p-3 bg-white bg-opacity-20 rounded-full">
            <i class="{{ widget.icon }} text-2xl"></i>
        </div>
    </div>
    
    <div class="mt-4">
        <div class="text-3xl font-bold">{{ widget.data.value }}</div>
        {% if widget.data.change %}
            <div class="flex items-center mt-2">
                <i class="fas fa-trending-{% if widget.data.change >= 0 %}up text-green-300{% else %}down text-red-300{% endif %} mr-2"></i>
                <span class="text-sm font-medium">
                    {{ widget.data.change|floatformat:1 }}% from last period
                </span>
            </div>
        {% endif %}
    </div>
    
    {% if widget.data.trend %}
        <div class="mt-4">
            <canvas id="trend-{{ widget.id }}" width="200" height="50"></canvas>
        </div>
        <script>
            // Mini trend chart
            const ctx = document.getElementById('trend-{{ widget.id }}').getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: Array.from({length: {{ widget.data.trend|length }}}, (_, i) => i),
                    datasets: [{
                        data: {{ widget.data.trend|safe }},
                        borderColor: 'rgba(255, 255, 255, 0.8)',
                        backgroundColor: 'rgba(255, 255, 255, 0.1)',
                        borderWidth: 2,
                        fill: true,
                        tension: 0.4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: {
                        x: { display: false },
                        y: { display: false }
                    },
                    elements: { point: { radius: 0 } }
                }
            });
        </script>
    {% endif %}
</div>
```

## Custom CSS and JavaScript

### Adding Custom Styles

Create a comprehensive custom stylesheet:

```css
/* static/dashboard/css/custom.css */

/* Custom fonts */
body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Custom button styles */
.btn-custom {
    @apply inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm;
    @apply bg-gradient-to-r from-purple-600 to-blue-600 text-white;
    @apply hover:from-purple-700 hover:to-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500;
    transition: all 0.2s ease-in-out;
}

/* Custom widget animations */
.widget-container {
    transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}

.widget-container:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

/* Custom loading animations */
.loading-spinner {
    animation: spin 1s linear infinite;
}

@keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

/* Custom scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    @apply bg-gray-100 dark:bg-gray-800;
}

::-webkit-scrollbar-thumb {
    @apply bg-gray-300 dark:bg-gray-600 rounded-full;
}

::-webkit-scrollbar-thumb:hover {
    @apply bg-gray-400 dark:bg-gray-500;
}

/* Custom card styles */
.card-hover {
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.card-hover:hover {
    transform: scale(1.02);
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

/* Glassmorphism effect */
.glass {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
}

[data-theme="dark"] .glass {
    background: rgba(0, 0, 0, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.1);
}
```

### Adding Custom JavaScript

```javascript
// static/dashboard/js/custom.js

// Custom dashboard enhancements
document.addEventListener('DOMContentLoaded', function() {
    // Initialize custom components
    initializeCustomWidgets();
    initializeAnimations();
    initializeKeyboardShortcuts();
});

function initializeCustomWidgets() {
    // Add custom interactions to widgets
    document.querySelectorAll('.widget-container').forEach(widget => {
        widget.addEventListener('click', function() {
            // Custom click handler
            console.log('Widget clicked:', this.dataset.widgetId);
        });
    });
}

function initializeAnimations() {
    // Animate widgets on scroll
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in');
            }
        });
    });

    document.querySelectorAll('.widget-container').forEach(widget => {
        observer.observe(widget);
    });
}

function initializeKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // Custom keyboard shortcuts
        if (e.ctrlKey || e.metaKey) {
            switch(e.key) {
                case 'r':
                    e.preventDefault();
                    refreshAllWidgets();
                    break;
                case 'd':
                    e.preventDefault();
                    toggleDarkMode();
                    break;
            }
        }
    });
}

function refreshAllWidgets() {
    document.querySelectorAll('.widget-container').forEach(widget => {
        const widgetId = widget.dataset.widgetId;
        fetch(`/admin/dashboard/api/widgets/${widgetId}/data/`)
            .then(response => response.json())
            .then(data => updateWidgetDisplay(widget, data))
            .catch(error => console.error('Error refreshing widget:', error));
    });
}

function updateWidgetDisplay(widget, data) {
    // Update widget with new data
    const valueElement = widget.querySelector('.widget-value');
    if (valueElement && data.value !== undefined) {
        animateValueChange(valueElement, data.value);
    }
}

function animateValueChange(element, newValue) {
    element.style.transform = 'scale(1.1)';
    element.style.color = '#10b981';
    
    setTimeout(() => {
        element.textContent = newValue;
        element.style.transform = 'scale(1)';
        element.style.color = '';
    }, 150);
}
```

## Responsive Design Customization

### Custom Breakpoints

```css
/* Custom responsive utilities */
@media (min-width: 1440px) {
    .xl\:grid-cols-5 {
        grid-template-columns: repeat(5, minmax(0, 1fr));
    }
}

@media (max-width: 768px) {
    .mobile-stack {
        grid-template-columns: 1fr;
        gap: 1rem;
    }
    
    .mobile-hide {
        display: none;
    }
}
```

### Widget Responsive Behavior

```python
# Custom widget with responsive configuration
class ResponsiveWidget(MetricWidget):
    title = "Responsive Widget"
    
    def get_responsive_config(self):
        return {
            'mobile': {'cols': 1, 'order': 1},
            'tablet': {'cols': 2, 'order': 2},
            'desktop': {'cols': 3, 'order': 3},
        }
```

## Color Scheme Customization

### Custom Color Palette

```python
CUSTOM_ADMIN_DASHBOARD_CONFIG = {
    'COLOR_SCHEME': {
        'primary': '#6366f1',      # Indigo
        'secondary': '#ec4899',    # Pink
        'success': '#10b981',      # Emerald
        'warning': '#f59e0b',      # Amber
        'error': '#ef4444',        # Red
        'info': '#06b6d4',         # Cyan
    },
    'WIDGET_COLORS': {
        'default': 'blue',
        'users': 'green',
        'sales': 'purple',
        'analytics': 'orange',
        'system': 'gray',
    }
}
```

## Advanced Customization

### Custom Dashboard Layout Engine

```python
# dashboard_custom/layout.py
class CustomLayoutEngine:
    def __init__(self, config):
        self.config = config
    
    def render_layout(self, widgets):
        # Custom layout logic
        layout = self.calculate_optimal_layout(widgets)
        return self.render_grid(layout)
    
    def calculate_optimal_layout(self, widgets):
        # Implement custom layout algorithm
        pass
```

### Dynamic Theming

```javascript
// Dynamic theme switching based on time of day
function autoThemeSwitch() {
    const hour = new Date().getHours();
    const isDaytime = hour >= 6 && hour < 18;
    const theme = isDaytime ? 'light' : 'dark';
    
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('dashboard-theme', theme);
}

// Initialize auto-theme switching
setInterval(autoThemeSwitch, 60000); // Check every minute
```

## Best Practices

1. **Maintain Consistency**: Use consistent spacing, colors, and typography
2. **Mobile First**: Design for mobile devices first, then enhance for larger screens
3. **Performance**: Optimize images and minimize custom CSS/JS
4. **Accessibility**: Ensure proper contrast ratios and keyboard navigation
5. **Progressive Enhancement**: Ensure basic functionality works without JavaScript
6. **Testing**: Test your customizations across different browsers and devices

## Troubleshooting

### Common Issues

**Custom CSS not loading:**
- Ensure `STATICFILES_DIRS` is configured correctly
- Run `python manage.py collectstatic`
- Check browser developer tools for 404 errors

**Theme toggle not working:**
- Verify JavaScript is enabled
- Check for console errors
- Ensure theme CSS variables are defined

**Widget layout broken:**
- Validate your grid CSS classes
- Check for conflicting CSS rules
- Test on different screen sizes
