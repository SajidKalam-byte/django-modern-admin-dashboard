"""
Test app views.
"""

from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from .models import Order, Product


@staff_member_required
def test_dashboard(request):
    """Test dashboard view."""
    context = {
        'orders': Order.objects.count(),
        'products': Product.objects.count(),
    }
    return render(request, 'test_app/dashboard.html', context)


def api_test_data(request):
    """API endpoint for test data."""
    data = {
        'orders': Order.objects.count(),
        'products': Product.objects.count(),
        'recent_orders': list(
            Order.objects.values('order_number', 'amount', 'status')[:5]
        )
    }
    return JsonResponse(data)
