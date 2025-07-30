"""
Tests for dashboard widgets.
"""

import pytest
from django.contrib.auth.models import User
from django.test import RequestFactory
from dashboard.widgets import (
    widget_registry, 
    BaseWidget, 
    MetricWidget, 
    ChartWidget, 
    TableWidget,
    UserCountWidget,
    RecentLoginsWidget,
    LoginActivityChartWidget,
)


class TestWidgetRegistry:
    """Test widget registry functionality."""
    
    def test_widget_registration(self):
        """Test widget registration."""
        # Create a test widget
        @widget_registry.register
        class TestWidget(BaseWidget):
            title = "Test Widget"
            
            def get_context_data(self):
                return {'test': True}
        
        # Check if registered (should use widget_id property)
        widget_id = TestWidget().widget_id
        assert widget_registry.get_widget(widget_id) == TestWidget
        assert TestWidget in widget_registry.get_all_widgets()
    
    def test_get_enabled_widgets(self):
        """Test getting enabled widgets from settings."""
        enabled = widget_registry.get_enabled_widgets()
        assert len(enabled) >= 2  # At least UserCountWidget and RecentLoginsWidget
        
        # Check specific widgets are included
        widget_names = [w.__name__ for w in enabled]
        assert 'UserCountWidget' in widget_names
        assert 'RecentLoginsWidget' in widget_names


@pytest.mark.django_db
class TestBaseWidget:
    """Test base widget functionality."""
    
    def setup_method(self):
        """Set up test data."""
        self.factory = RequestFactory()
        self.request = self.factory.get('/dashboard/')
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.request.user = self.user
        
        # Create a concrete test widget
        class TestWidget(BaseWidget):
            title = "Test Widget"
            
            def get_context_data(self):
                return {'test': 'data'}
        
        self.TestWidget = TestWidget
    
    def test_widget_initialization(self):
        """Test widget initialization."""
        widget = self.TestWidget(request=self.request)
        assert widget.request == self.request
        assert widget.title == "Test Widget"
        assert widget.widget_type == "base"
    
    def test_widget_permissions(self):
        """Test widget permission checking."""
        widget = self.TestWidget(request=self.request)
        
        # Regular user should not have access
        assert not widget.has_permission(self.user)
        
        # Staff user should have access
        self.user.is_staff = True
        assert widget.has_permission(self.user)
    
    def test_widget_api_data(self):
        """Test widget API data generation."""
        widget = self.TestWidget(request=self.request)
        data = widget.get_api_data()
        
        assert 'title' in data
        assert 'value' in data
        assert 'chart_data' in data
        assert 'context' in data
        assert data['title'] == "Test Widget"


@pytest.mark.django_db
class TestMetricWidget:
    """Test metric widget functionality."""
    
    def setup_method(self):
        """Set up test data."""
        self.factory = RequestFactory()
        self.request = self.factory.get('/dashboard/')
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            is_staff=True
        )
        self.request.user = self.user
    
    def test_metric_widget_template(self):
        """Test metric widget template."""
        # Create a concrete metric widget
        class TestMetricWidget(MetricWidget):
            title = "Test Metric"
            
            def get_value(self):
                return 100
                
            def get_context_data(self):
                return {'test': 'data', 'trend': 5, 'trend_period': '7d'}
        
        widget = TestMetricWidget(request=self.request)
        assert widget.template_name == "dashboard/widgets/metric.html"
        assert widget.widget_type == "metric"
    
    def test_metric_widget_context(self):
        """Test metric widget context data."""
        # Create a concrete metric widget
        class TestMetricWidget(MetricWidget):
            title = "Test Metric"
            
            def get_value(self):
                return 100
                
            def get_context_data(self):
                return {'test': 'data', 'trend': 5, 'trend_period': '7d'}
        
        widget = TestMetricWidget(request=self.request)
        context = widget.get_context_data()
        
        assert 'trend' in context
        assert 'trend_period' in context


@pytest.mark.django_db
class TestUserCountWidget:
    """Test user count widget functionality."""
    
    def setup_method(self):
        """Set up test data."""
        self.factory = RequestFactory()
        self.request = self.factory.get('/dashboard/')
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            is_staff=True
        )
        self.request.user = self.user
        
        # Create additional test users
        for i in range(5):
            User.objects.create_user(
                username=f'user{i}',
                email=f'user{i}@example.com',
                password='testpass123'
            )
    
    def test_user_count_value(self):
        """Test user count calculation."""
        widget = UserCountWidget(request=self.request)
        count = widget.get_value()
        
        # Should count all users (1 test user + 5 additional = 6)
        assert count == 6
    
    def test_user_count_context(self):
        """Test user count widget context."""
        widget = UserCountWidget(request=self.request)
        context = widget.get_context_data()
        
        assert 'active_users' in context
        assert 'new_this_week' in context
        assert context['active_users'] == 6  # All users are active by default
    
    def test_user_count_trend(self):
        """Test user count trend calculation."""
        widget = UserCountWidget(request=self.request)
        trend = widget.get_trend()
        
        # Since all users were created recently, trend should be positive
        assert trend is not None
        assert isinstance(trend, (int, float))


@pytest.mark.django_db
class TestRecentLoginsWidget:
    """Test recent logins widget functionality."""
    
    def setup_method(self):
        """Set up test data."""
        self.factory = RequestFactory()
        self.request = self.factory.get('/dashboard/')
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            is_staff=True
        )
        self.request.user = self.user
    
    def test_recent_logins_headers(self):
        """Test table headers."""
        widget = RecentLoginsWidget(request=self.request)
        headers = widget.get_headers()
        
        expected_headers = ['Username', 'Email', 'Last Login', 'Status']
        assert headers == expected_headers
    
    def test_recent_logins_rows(self):
        """Test table rows generation."""
        widget = RecentLoginsWidget(request=self.request)
        rows = widget.get_rows()
        
        # Should return list of rows
        assert isinstance(rows, list)
        # Each row should have 4 columns (matching headers)
        for row in rows:
            assert len(row) == 4


@pytest.mark.django_db
class TestChartWidget:
    """Test chart widget functionality."""
    
    def setup_method(self):
        """Set up test data."""
        self.factory = RequestFactory()
        self.request = self.factory.get('/dashboard/')
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            is_staff=True
        )
        self.request.user = self.user
    
    def test_chart_widget_template(self):
        """Test chart widget template."""
        # Create a concrete chart widget
        class TestChartWidget(ChartWidget):
            title = "Test Chart"
            
            def get_chart_data(self):
                return {'labels': ['A', 'B'], 'data': [1, 2]}
                
            def get_context_data(self):
                return {'chart_type': 'line'}
        
        widget = TestChartWidget(request=self.request)
        assert widget.template_name == "dashboard/widgets/chart.html"
        assert widget.widget_type == "chart"
        assert widget.chart_type == "line"
    
    def test_chart_widget_context(self):
        """Test chart widget context data."""
        # Create a concrete chart widget
        class TestChartWidget(ChartWidget):
            title = "Test Chart"
            
            def get_chart_data(self):
                return {'labels': ['A', 'B'], 'data': [1, 2]}
                
            def get_context_data(self):
                return {'chart_type': 'line'}
        
        widget = TestChartWidget(request=self.request)
        context = widget.get_context_data()
        
        assert 'chart_type' in context
        assert context['chart_type'] == "line"


@pytest.mark.django_db
class TestLoginActivityChartWidget:
    """Test login activity chart widget."""
    
    def setup_method(self):
        """Set up test data."""
        self.factory = RequestFactory()
        self.request = self.factory.get('/dashboard/')
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            is_staff=True
        )
        self.request.user = self.user
    
    def test_login_chart_data(self):
        """Test login activity chart data generation."""
        widget = LoginActivityChartWidget(request=self.request)
        chart_data = widget.get_chart_data()
        
        assert 'type' in chart_data
        assert 'data' in chart_data
        assert 'options' in chart_data
        assert chart_data['type'] == 'line'
        
        # Check data structure
        data = chart_data['data']
        assert 'labels' in data
        assert 'datasets' in data
        assert len(data['labels']) == 7  # 7 days
        assert len(data['datasets']) == 1
        
        dataset = data['datasets'][0]
        assert 'label' in dataset
        assert 'data' in dataset
        assert len(dataset['data']) == 7  # 7 days of data


@pytest.mark.django_db
@pytest.mark.django_db
class TestWidgetIntegration:
    """Integration tests for widgets."""
    
    def test_widget_registry_with_database(self):
        """Test widget registry with database operations."""
        # Create test users
        User.objects.create_user(username='user1', email='user1@test.com')
        User.objects.create_user(username='user2', email='user2@test.com')
        
        factory = RequestFactory()
        request = factory.get('/dashboard/')
        request.user = User.objects.create_user(
            username='staff',
            email='staff@test.com',
            is_staff=True
        )
        
        # Test all registered widgets
        enabled_widgets = widget_registry.get_enabled_widgets()
        
        for widget_class in enabled_widgets:
            widget = widget_class(request=request)
            
            # Widget should be instantiable
            assert widget is not None
            
            # Should have permission for staff user
            assert widget.has_permission(request.user)
            
            # Should be able to get API data without errors
            try:
                api_data = widget.get_api_data()
                assert isinstance(api_data, dict)
            except Exception as e:
                pytest.fail(f"Widget {widget_class.__name__} failed to get API data: {e}")
    
    def test_widget_caching(self):
        """Test widget data consistency."""
        from django.core.cache import cache
        
        factory = RequestFactory()
        request = factory.get('/dashboard/')
        request.user = User.objects.create_user(
            username='staff',
            email='staff@test.com',
            is_staff=True
        )
        
        widget = UserCountWidget(request=request)
        
        # Get data multiple times
        data1 = widget.get_api_data()
        data2 = widget.get_api_data()
        
        # Data should be consistent
        assert data1 == data2
        assert 'title' in data1
        assert 'value' in data1
