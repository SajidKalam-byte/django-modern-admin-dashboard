"""
Management command to create a new dashboard widget.
"""

import os
from django.core.management.base import BaseCommand, CommandError
from django.template import Template, Context
from django.conf import settings


class Command(BaseCommand):
    help = 'Create a new dashboard widget'

    def add_arguments(self, parser):
        parser.add_argument(
            'widget_name',
            type=str,
            help='Name of the widget to create (e.g., SalesWidget)'
        )
        parser.add_argument(
            '--type',
            choices=['metric', 'chart', 'table', 'base'],
            default='metric',
            help='Type of widget to create (default: metric)'
        )
        parser.add_argument(
            '--app',
            type=str,
            help='Django app where to create the widget (default: current app)'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Overwrite existing files'
        )

    def handle(self, *args, **options):
        widget_name = options['widget_name']
        widget_type = options['type']
        app_name = options['app']
        force = options['force']

        # Validate widget name
        if not widget_name.endswith('Widget'):
            widget_name += 'Widget'

        if not widget_name[0].isupper():
            widget_name = widget_name.capitalize()

        # Determine app directory
        if app_name:
            app_dir = self.find_app_directory(app_name)
        else:
            app_dir = os.getcwd()

        if not app_dir:
            raise CommandError(f"Could not find app directory for '{app_name}'")

        # Create widget file
        widget_file_path = os.path.join(app_dir, 'widgets.py')
        
        if os.path.exists(widget_file_path) and not force:
            self.stdout.write(
                self.style.WARNING(f"Widget file already exists: {widget_file_path}")
            )
            self.stdout.write("Add the following widget to your existing widgets.py file:")
            self.stdout.write("")
        else:
            # Create or overwrite the file
            with open(widget_file_path, 'w' if force else 'a') as f:
                if force or not os.path.exists(widget_file_path):
                    f.write(self.get_widget_file_header())
                f.write(self.get_widget_code(widget_name, widget_type))

        # Output the widget code
        self.stdout.write(self.get_widget_code(widget_name, widget_type))
        
        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(f"Widget '{widget_name}' created successfully!"))
        self.stdout.write("")
        self.stdout.write("Next steps:")
        self.stdout.write("1. Add your widget to CUSTOM_ADMIN_DASHBOARD_CONFIG['WIDGETS'] in settings.py")
        self.stdout.write("2. Implement the required methods in your widget class")
        self.stdout.write("3. Restart your Django server")

    def find_app_directory(self, app_name):
        """Find the directory for a Django app."""
        for app_config in settings.INSTALLED_APPS:
            if app_config.split('.')[-1] == app_name:
                try:
                    module = __import__(app_config, fromlist=[''])
                    return os.path.dirname(module.__file__)
                except ImportError:
                    continue
        return None

    def get_widget_file_header(self):
        """Get the header for a new widgets.py file."""
        return '''"""
Custom dashboard widgets.
"""

from dashboard.widgets import register_widget, MetricWidget, ChartWidget, TableWidget
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


'''

    def get_widget_code(self, widget_name, widget_type):
        """Generate widget code based on type."""
        
        templates = {
            'metric': '''@register_widget
class {{ widget_name }}(MetricWidget):
    """{{ widget_description }}"""
    
    widget_id = "{{ widget_id }}"
    title = "{{ widget_title }}"
    description = "{{ widget_description }}"
    icon = "chart-bar"
    color = "blue"
    
    def get_value(self):
        """Return the metric value."""
        # TODO: Implement your metric calculation
        return 42
    
    def get_trend(self):
        """Return trend percentage (optional)."""
        # TODO: Calculate trend compared to previous period
        return 5.2  # +5.2%
    
    def get_context_data(self):
        """Return additional context data."""
        context = super().get_context_data()
        context.update({
            # TODO: Add any additional context data
            'additional_info': 'Some extra information'
        })
        return context


''',
            'chart': '''@register_widget
class {{ widget_name }}(ChartWidget):
    """{{ widget_description }}"""
    
    widget_id = "{{ widget_id }}"
    title = "{{ widget_title }}"
    description = "{{ widget_description }}"
    icon = "chart-line"
    color = "purple"
    chart_type = "line"  # line, bar, pie, doughnut
    
    def get_chart_data(self):
        """Return Chart.js compatible data."""
        # TODO: Implement your chart data
        return {
            'type': self.chart_type,
            'data': {
                'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
                'datasets': [{
                    'label': 'Sample Data',
                    'data': [12, 19, 3, 5, 2],
                    'borderColor': '#8B5CF6',
                    'backgroundColor': 'rgba(139, 92, 246, 0.1)',
                }]
            },
            'options': {
                'responsive': True,
                'plugins': {
                    'legend': {
                        'display': True
                    }
                }
            }
        }


''',
            'table': '''@register_widget
class {{ widget_name }}(TableWidget):
    """{{ widget_description }}"""
    
    widget_id = "{{ widget_id }}"
    title = "{{ widget_title }}"
    description = "{{ widget_description }}"
    icon = "table"
    color = "green"
    max_rows = 10
    
    def get_headers(self):
        """Return table headers."""
        # TODO: Define your table headers
        return ['Column 1', 'Column 2', 'Column 3']
    
    def get_rows(self):
        """Return table rows."""
        # TODO: Implement your table data
        return [
            ['Row 1 Col 1', 'Row 1 Col 2', 'Row 1 Col 3'],
            ['Row 2 Col 1', 'Row 2 Col 2', 'Row 2 Col 3'],
            ['Row 3 Col 1', 'Row 3 Col 2', 'Row 3 Col 3'],
        ]


''',
            'base': '''@register_widget
class {{ widget_name }}(BaseWidget):
    """{{ widget_description }}"""
    
    widget_id = "{{ widget_id }}"
    title = "{{ widget_title }}"
    description = "{{ widget_description }}"
    icon = "cog"
    color = "gray"
    template_name = "dashboard/widgets/custom.html"  # Create your own template
    
    def get_context_data(self):
        """Return context data for the widget template."""
        return {
            # TODO: Add your context data
            'custom_data': 'Your custom data here'
        }
    
    def get_api_data(self):
        """Return data for API endpoints (optional)."""
        data = super().get_api_data()
        # TODO: Add any additional API data
        data['custom_field'] = 'Custom API data'
        return data


'''
        }

        template_str = templates[widget_type]
        template = Template(template_str)
        
        context = Context({
            'widget_name': widget_name,
            'widget_id': self.camel_to_snake(widget_name),
            'widget_title': self.camel_to_title(widget_name),
            'widget_description': f"Custom {widget_type} widget: {self.camel_to_title(widget_name)}",
        })
        
        return template.render(context)

    def camel_to_snake(self, name):
        """Convert CamelCase to snake_case."""
        import re
        # Remove 'Widget' suffix and convert to snake_case
        name = re.sub(r'Widget$', '', name)
        return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()

    def camel_to_title(self, name):
        """Convert CamelCase to Title Case."""
        import re
        # Remove 'Widget' suffix and add spaces before capitals
        name = re.sub(r'Widget$', '', name)
        return re.sub(r'(?<!^)(?=[A-Z])', ' ', name)
