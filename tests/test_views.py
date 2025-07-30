"""
Tests for dashboard views.
"""

import json
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.cache import cache


class TestDashboardViews(TestCase):
    """Test dashboard view functionality."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.staff_user = User.objects.create_user(
            username='staffuser',
            email='staff@example.com',
            password='testpass123',
            is_staff=True
        )
    
    def test_dashboard_view_requires_staff(self):
        """Test that dashboard view requires staff permission."""
        # Anonymous user should be redirected
        response = self.client.get(reverse('dashboard:dashboard'))
        self.assertEqual(response.status_code, 302)
        
        # Regular user should be redirected
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard:dashboard'))
        self.assertEqual(response.status_code, 302)
    
    def test_dashboard_view_success(self):
        """Test successful dashboard view access."""
        self.client.login(username='staffuser', password='testpass123')
        response = self.client.get(reverse('dashboard:dashboard'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dashboard Overview')
        self.assertContains(response, 'widget-card')
    
    def test_dashboard_context(self):
        """Test dashboard view context."""
        self.client.login(username='staffuser', password='testpass123')
        response = self.client.get(reverse('dashboard:dashboard'))
        
        # Check context variables
        self.assertIn('widgets', response.context)
        self.assertIn('theme', response.context)
        self.assertIn('title', response.context)
        self.assertIn('config', response.context)
        
        # Check widgets are properly initialized
        widgets = response.context['widgets']
        self.assertIsInstance(widgets, list)
        
        for widget in widgets:
            # Each widget should have required attributes
            self.assertTrue(hasattr(widget, 'title'))
            self.assertTrue(hasattr(widget, 'widget_type'))
            self.assertTrue(hasattr(widget, 'get_context_data'))
    
    def test_widget_data_view(self):
        """Test widget data API endpoint."""
        self.client.login(username='staffuser', password='testpass123')
        
        # Test valid widget
        response = self.client.get(
            reverse('dashboard:widget_data', kwargs={'widget_id': 'user_count'})
        )
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertIn('title', data)
        self.assertIn('value', data)
    
    def test_widget_data_view_not_found(self):
        """Test widget data view with invalid widget ID."""
        self.client.login(username='staffuser', password='testpass123')
        
        response = self.client.get(
            reverse('dashboard:widget_data', kwargs={'widget_id': 'invalid_widget'})
        )
        self.assertEqual(response.status_code, 404)
    
    def test_widget_data_view_permission_denied(self):
        """Test widget data view with insufficient permissions."""
        # Regular user should be denied
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.get(
            reverse('dashboard:widget_data', kwargs={'widget_id': 'user_count'})
        )
        self.assertEqual(response.status_code, 302)  # Redirected by staff_member_required
    
    def test_refresh_widget_view(self):
        """Test widget refresh functionality."""
        self.client.login(username='staffuser', password='testpass123')
        
        # Set up cache
        cache_key = f"widget_data_user_count_{self.staff_user.id}"
        cache.set(cache_key, {'cached': True}, 60)
        
        # Refresh widget
        response = self.client.get(
            reverse('dashboard:widget_refresh', kwargs={'widget_id': 'user_count'})
        )
        self.assertEqual(response.status_code, 200)
        
        # Cache should be cleared
        cached_data = cache.get(cache_key)
        # Cache might be reset or updated with new data
        if cached_data:
            self.assertNotEqual(cached_data, {'cached': True})
    
    def test_dashboard_settings_view_get(self):
        """Test dashboard settings GET request."""
        self.client.login(username='staffuser', password='testpass123')
        
        response = self.client.get(reverse('dashboard:settings'))
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertIn('theme', data)
        self.assertIn('config', data)
    
    def test_dashboard_settings_view_post(self):
        """Test dashboard settings POST request."""
        self.client.login(username='staffuser', password='testpass123')
        
        # Post theme change
        response = self.client.post(
            reverse('dashboard:settings'),
            data=json.dumps({'theme': 'dark'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertTrue(data.get('success'))
        
        # Check session was updated
        session = self.client.session
        self.assertEqual(session.get('dashboard_theme'), 'dark')
    
    def test_export_dashboard_data_view(self):
        """Test dashboard data export."""
        self.client.login(username='staffuser', password='testpass123')
        
        response = self.client.get(reverse('dashboard:export'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertIn('attachment', response['Content-Disposition'])
        
        data = json.loads(response.content)
        self.assertIn('config', data)
        self.assertIn('widgets', data)
        self.assertIn('timestamp', data)
        
        # Check widgets data structure
        widgets = data['widgets']
        self.assertIsInstance(widgets, list)
        
        for widget_data in widgets:
            self.assertIn('widget_id', widget_data)
            self.assertIn('title', widget_data)


class TestDashboardIntegration(TestCase):
    """Integration tests for dashboard functionality."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.staff_user = User.objects.create_user(
            username='staffuser',
            email='staff@example.com',
            password='testpass123',
            is_staff=True
        )
        
        # Create test data
        for i in range(10):
            User.objects.create_user(
                username=f'user{i}',
                email=f'user{i}@example.com',
                password='testpass123'
            )
    
    def test_complete_dashboard_workflow(self):
        """Test complete dashboard workflow."""
        self.client.login(username='staffuser', password='testpass123')
        
        # 1. Access main dashboard
        response = self.client.get(reverse('dashboard:dashboard'))
        self.assertEqual(response.status_code, 200)
        
        # 2. Check widget data
        response = self.client.get(
            reverse('dashboard:widget_data', kwargs={'widget_id': 'user_count'})
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertGreater(data['value'], 0)  # Should have users
        
        # 3. Refresh widget
        response = self.client.get(
            reverse('dashboard:widget_refresh', kwargs={'widget_id': 'user_count'})
        )
        self.assertEqual(response.status_code, 200)
        
        # 4. Change theme
        response = self.client.post(
            reverse('dashboard:settings'),
            data=json.dumps({'theme': 'dark'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        
        # 5. Export data
        response = self.client.get(reverse('dashboard:export'))
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertGreater(len(data['widgets']), 0)
    
    def test_dashboard_with_no_widgets(self):
        """Test dashboard behavior with no enabled widgets."""
        # Temporarily override settings to disable all widgets
        from django.test import override_settings
        
        with override_settings(CUSTOM_ADMIN_DASHBOARD_CONFIG={'WIDGETS': []}):
            self.client.login(username='staffuser', password='testpass123')
            response = self.client.get(reverse('dashboard:dashboard'))
            
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'No widgets available')
    
    def test_dashboard_caching_behavior(self):
        """Test dashboard caching functionality."""
        self.client.login(username='staffuser', password='testpass123')
        
        # Clear cache
        cache.clear()
        
        # First request - should populate cache
        response1 = self.client.get(
            reverse('dashboard:widget_data', kwargs={'widget_id': 'user_count'})
        )
        self.assertEqual(response1.status_code, 200)
        
        # Second request - should use cache
        response2 = self.client.get(
            reverse('dashboard:widget_data', kwargs={'widget_id': 'user_count'})
        )
        self.assertEqual(response2.status_code, 200)
        
        # Responses should be identical (from cache)
        self.assertEqual(response1.content, response2.content)
        
        # Refresh should clear cache and return fresh data
        response3 = self.client.get(
            reverse('dashboard:widget_refresh', kwargs={'widget_id': 'user_count'})
        )
        self.assertEqual(response3.status_code, 200)
