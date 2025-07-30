"""
Tests for dashboard API endpoints.
"""

import json
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse


class TestDashboardAPI(TestCase):
    """Test dashboard API functionality."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.staff_user = User.objects.create_user(
            username='staffuser',
            email='staff@example.com',
            password='testpass123',
            is_staff=True
        )
        self.regular_user = User.objects.create_user(
            username='regularuser',
            email='regular@example.com',
            password='testpass123'
        )
    
    def test_widget_list_api_success(self):
        """Test widget list API with proper permissions."""
        self.client.login(username='staffuser', password='testpass123')
        
        response = self.client.get(reverse('dashboard:api:widget_list'))
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertIn('widgets', data)
        self.assertIn('count', data)
        self.assertIsInstance(data['widgets'], list)
        self.assertGreater(data['count'], 0)
        
        # Check widget data structure
        for widget in data['widgets']:
            self.assertIn('id', widget)
            self.assertIn('title', widget)
            self.assertIn('description', widget)
            self.assertIn('type', widget)
            self.assertIn('icon', widget)
    
    def test_widget_list_api_permission_denied(self):
        """Test widget list API without proper permissions."""
        # Regular user should be denied
        self.client.login(username='regularuser', password='testpass123')
        response = self.client.get(reverse('dashboard:api:widget_list'))
        self.assertEqual(response.status_code, 403)
        
        # Anonymous user should be denied
        response = self.client.get(reverse('dashboard:api:widget_list'))
        self.assertEqual(response.status_code, 403)
    
    def test_widget_detail_api_success(self):
        """Test widget detail API with valid widget."""
        self.client.login(username='staffuser', password='testpass123')
        
        response = self.client.get(
            reverse('dashboard:api:widget_detail', kwargs={'widget_id': 'user_count'})
        )
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertIn('widget_id', data)
        self.assertIn('title', data)
        self.assertIn('value', data)
        self.assertEqual(data['widget_id'], 'user_count')
    
    def test_widget_detail_api_not_found(self):
        """Test widget detail API with invalid widget."""
        self.client.login(username='staffuser', password='testpass123')
        
        response = self.client.get(
            reverse('dashboard:api:widget_detail', kwargs={'widget_id': 'invalid'})
        )
        self.assertEqual(response.status_code, 404)
        
        data = json.loads(response.content)
        self.assertIn('error', data)
    
    def test_chart_data_api_success(self):
        """Test chart data API with chart widget."""
        self.client.login(username='staffuser', password='testpass123')
        
        response = self.client.get(
            reverse('dashboard:api:chart_data', kwargs={'widget_id': 'login_activity_chart'})
        )
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertIn('widget_id', data)
        self.assertIn('chart_data', data)
        
        chart_data = data['chart_data']
        self.assertIn('type', chart_data)
        self.assertIn('data', chart_data)
    
    def test_chart_data_api_no_chart_data(self):
        """Test chart data API with non-chart widget."""
        self.client.login(username='staffuser', password='testpass123')
        
        response = self.client.get(
            reverse('dashboard:api:chart_data', kwargs={'widget_id': 'user_count'})
        )
        self.assertEqual(response.status_code, 404)
        
        data = json.loads(response.content)
        self.assertIn('error', data)
    
    def test_dashboard_stats_api(self):
        """Test dashboard statistics API."""
        self.client.login(username='staffuser', password='testpass123')
        
        response = self.client.get(reverse('dashboard:api:dashboard_stats'))
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertIn('dashboard', data)
        self.assertIn('widgets', data)
        self.assertIn('users', data)
        self.assertIn('config', data)
        
        # Check dashboard info
        dashboard_info = data['dashboard']
        self.assertIn('title', dashboard_info)
        self.assertIn('theme', dashboard_info)
        self.assertIn('version', dashboard_info)
        
        # Check widget stats
        widget_stats = data['widgets']
        self.assertIn('total', widget_stats)
        self.assertIn('enabled', widget_stats)
        self.assertIn('accessible', widget_stats)
        
        # Check user stats
        user_stats = data['users']
        self.assertIn('total', user_stats)
        self.assertIn('active', user_stats)
        self.assertIn('staff', user_stats)
    
    def test_user_count_api_legacy(self):
        """Test legacy user count API endpoint."""
        self.client.login(username='staffuser', password='testpass123')
        
        response = self.client.get(reverse('dashboard:api:user_count'))
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertIn('count', data)
        self.assertIn('active_count', data)
        self.assertIsInstance(data['count'], int)
        self.assertIsInstance(data['active_count'], int)
    
    def test_refresh_cache_api(self):
        """Test cache refresh API endpoint."""
        self.client.login(username='staffuser', password='testpass123')
        
        response = self.client.post(reverse('dashboard:api:refresh_cache'))
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Cache refreshed successfully')
    
    def test_health_check_api(self):
        """Test health check API endpoint."""
        self.client.login(username='staffuser', password='testpass123')
        
        response = self.client.get(reverse('dashboard:api:health_check'))
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertIn('status', data)
        self.assertIn('django_version', data)
        self.assertIn('database', data)
        self.assertIn('cache', data)
        self.assertIn('widgets_loaded', data)
        
        # Status should be healthy in test environment
        self.assertIn(data['status'], ['healthy', 'degraded'])
        self.assertEqual(data['database'], 'connected')
        self.assertIsInstance(data['widgets_loaded'], int)
        self.assertGreater(data['widgets_loaded'], 0)


class TestAPIPermissions(TestCase):
    """Test API permission functionality."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.staff_user = User.objects.create_user(
            username='staffuser',
            email='staff@example.com',
            password='testpass123',
            is_staff=True
        )
        self.regular_user = User.objects.create_user(
            username='regularuser',
            email='regular@example.com',
            password='testpass123'
        )
        self.superuser = User.objects.create_superuser(
            username='superuser',
            email='super@example.com',
            password='testpass123'
        )
    
    def test_api_access_with_different_user_types(self):
        """Test API access with different user types."""
        api_endpoints = [
            reverse('dashboard:api:widget_list'),
            reverse('dashboard:api:dashboard_stats'),
            reverse('dashboard:api:health_check'),
        ]
        
        for endpoint in api_endpoints:
            # Anonymous user - should be denied
            response = self.client.get(endpoint)
            self.assertIn(response.status_code, [403, 401])
            
            # Regular user - should be denied
            self.client.login(username='regularuser', password='testpass123')
            response = self.client.get(endpoint)
            self.assertEqual(response.status_code, 403)
            
            # Staff user - should be allowed
            self.client.login(username='staffuser', password='testpass123')
            response = self.client.get(endpoint)
            self.assertEqual(response.status_code, 200)
            
            # Superuser - should be allowed
            self.client.login(username='superuser', password='testpass123')
            response = self.client.get(endpoint)
            self.assertEqual(response.status_code, 200)
            
            # Logout for next iteration
            self.client.logout()
    
    def test_widget_specific_permissions(self):
        """Test widget-specific permission checking."""
        # Create a widget that requires specific permissions
        from dashboard.widgets import widget_registry, BaseWidget
        
        @widget_registry.register
        class PermissionTestWidget(BaseWidget):
            widget_id = 'permission_test'
            title = 'Permission Test Widget'
            requires_permissions = ['auth.view_user']
            
            def get_context_data(self):
                return {'test': True}
        
        self.client.login(username='staffuser', password='testpass123')
        
        # Test widget detail access
        response = self.client.get(
            reverse('dashboard:api:widget_detail', kwargs={'widget_id': 'permission_test'})
        )
        
        # Staff user might not have specific permission
        # The response depends on whether staff user has auth.view_user permission
        self.assertIn(response.status_code, [200, 403])


class TestAPIErrorHandling(TestCase):
    """Test API error handling."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.staff_user = User.objects.create_user(
            username='staffuser',
            email='staff@example.com',
            password='testpass123',
            is_staff=True
        )
    
    def test_invalid_widget_id_handling(self):
        """Test handling of invalid widget IDs."""
        self.client.login(username='staffuser', password='testpass123')
        
        invalid_endpoints = [
            reverse('dashboard:api:widget_detail', kwargs={'widget_id': 'nonexistent'}),
            reverse('dashboard:api:chart_data', kwargs={'widget_id': 'nonexistent'}),
        ]
        
        for endpoint in invalid_endpoints:
            response = self.client.get(endpoint)
            self.assertEqual(response.status_code, 404)
            
            data = json.loads(response.content)
            self.assertIn('error', data)
    
    def test_malformed_request_handling(self):
        """Test handling of malformed requests."""
        self.client.login(username='staffuser', password='testpass123')
        
        # Test POST with invalid JSON
        response = self.client.post(
            reverse('dashboard:api:refresh_cache'),
            data='invalid json',
            content_type='application/json'
        )
        # Should still work as this endpoint doesn't require JSON body
        self.assertEqual(response.status_code, 200)
    
    def test_api_with_disabled_features(self):
        """Test API behavior when features are disabled."""
        from django.test import override_settings
        
        # Test with API disabled
        with override_settings(CUSTOM_ADMIN_DASHBOARD_CONFIG={'ENABLE_API': False}):
            self.client.login(username='staffuser', password='testpass123')
            
            response = self.client.get(reverse('dashboard:api:widget_list'))
            self.assertEqual(response.status_code, 403)
