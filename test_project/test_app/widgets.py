"""
Custom widgets for the test app.
"""

from django.utils import timezone
from django.db import models
from datetime import timedelta
from dashboard.widgets import (
    register_widget, 
    MetricWidget, 
    ChartWidget, 
    TableWidget
)
from .models import Order, Product


@register_widget
class OrderCountWidget(MetricWidget):
    """Widget showing total order count."""
    
    widget_id = "order_count"
    title = "Total Orders"
    description = "Total number of orders in the system"
    icon = "cart"
    color = "green"
    
    def get_value(self):
        return Order.objects.count()
    
    def get_trend(self):
        # Calculate trend compared to last week
        week_ago = timezone.now() - timedelta(days=7)
        current_count = Order.objects.count()
        previous_count = Order.objects.filter(created_at__lt=week_ago).count()
        
        if previous_count == 0:
            return 100 if current_count > 0 else 0
        
        return round(((current_count - previous_count) / previous_count) * 100, 1)
    
    def get_context_data(self):
        context = super().get_context_data()
        context.update({
            'pending_orders': Order.objects.filter(status='pending').count(),
            'this_week_orders': Order.objects.filter(
                created_at__gte=timezone.now() - timedelta(days=7)
            ).count(),
        })
        return context


@register_widget
class RecentOrdersWidget(TableWidget):
    """Widget showing recent orders."""
    
    widget_id = "recent_orders"
    title = "Recent Orders"
    description = "Latest order activity"
    icon = "list"
    color = "blue"
    max_rows = 5
    
    def get_headers(self):
        return ['Order #', 'Customer', 'Amount', 'Status', 'Date']
    
    def get_rows(self):
        recent_orders = Order.objects.select_related('customer').order_by('-created_at')[:self.max_rows]
        
        rows = []
        for order in recent_orders:
            status_display = order.get_status_display()
            created_date = order.created_at.strftime('%Y-%m-%d %H:%M')
            rows.append([
                order.order_number,
                order.customer.username,
                f"${order.amount}",
                status_display,
                created_date
            ])
        
        return rows


@register_widget
class SalesChartWidget(ChartWidget):
    """Widget showing sales trends."""
    
    widget_id = "sales_chart"
    title = "Sales Trends"
    description = "Daily sales for the past week"
    icon = "chart-line"
    color = "purple"
    chart_type = "line"
    
    def get_chart_data(self):
        # Generate daily sales data for the past 7 days
        labels = []
        data = []
        
        for i in range(6, -1, -1):
            date = timezone.now().date() - timedelta(days=i)
            labels.append(date.strftime('%m/%d'))
            
            # Calculate total sales for this date
            daily_sales = Order.objects.filter(
                created_at__date=date,
                status__in=['shipped', 'delivered']
            ).aggregate(
                total=models.Sum('amount')
            )['total'] or 0
            
            data.append(float(daily_sales))
        
        return {
            'type': 'line',
            'data': {
                'labels': labels,
                'datasets': [{
                    'label': 'Daily Sales ($)',
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
                        'display': True,
                        'position': 'top'
                    },
                    'title': {
                        'display': True,
                        'text': 'Daily Sales Trend'
                    }
                },
                'scales': {
                    'y': {
                        'beginAtZero': True,
                        'ticks': {
                            'callback': 'function(value, index, values) { return "$" + value; }'
                        }
                    }
                },
                'interaction': {
                    'intersect': False,
                    'mode': 'index'
                }
            }
        }


@register_widget
class ProductStockWidget(MetricWidget):
    """Widget showing low stock products."""
    
    widget_id = "product_stock"
    title = "Low Stock Alert"
    description = "Products with low inventory"
    icon = "warning"
    color = "yellow"
    
    def get_value(self):
        return Product.objects.filter(stock_quantity__lt=10, is_active=True).count()
    
    def get_context_data(self):
        context = super().get_context_data()
        
        low_stock_products = Product.objects.filter(
            stock_quantity__lt=10, 
            is_active=True
        ).order_by('stock_quantity')[:5]
        
        context.update({
            'low_stock_products': low_stock_products,
            'total_products': Product.objects.filter(is_active=True).count(),
        })
        return context


@register_widget
class OrderStatusChartWidget(ChartWidget):
    """Widget showing order status distribution."""
    
    widget_id = "order_status_chart"
    title = "Order Status Distribution"
    description = "Current orders by status"
    icon = "chart-pie"
    color = "indigo"
    chart_type = "doughnut"
    
    def get_chart_data(self):
        from django.db import models
        
        # Get order counts by status
        status_counts = Order.objects.values('status').annotate(
            count=models.Count('id')
        ).order_by('status')
        
        labels = []
        data = []
        colors = {
            'pending': '#F59E0B',
            'processing': '#3B82F6',
            'shipped': '#8B5CF6',
            'delivered': '#10B981',
            'cancelled': '#EF4444',
        }
        background_colors = []
        
        for item in status_counts:
            status = item['status']
            count = item['count']
            
            labels.append(status.title())
            data.append(count)
            background_colors.append(colors.get(status, '#6B7280'))
        
        return {
            'type': 'doughnut',
            'data': {
                'labels': labels,
                'datasets': [{
                    'data': data,
                    'backgroundColor': background_colors,
                    'borderWidth': 2,
                    'borderColor': '#FFFFFF'
                }]
            },
            'options': {
                'responsive': True,
                'plugins': {
                    'legend': {
                        'position': 'bottom'
                    },
                    'title': {
                        'display': True,
                        'text': 'Orders by Status'
                    }
                },
                'cutout': '50%'
            }
        }


@register_widget
class RevenueWidget(MetricWidget):
    """Widget showing total revenue."""
    
    widget_id = "revenue"
    title = "Total Revenue"
    description = "Revenue from completed orders"
    icon = "currency"
    color = "green"
    
    def get_value(self):
        from django.db import models
        
        total_revenue = Order.objects.filter(
            status__in=['delivered']
        ).aggregate(
            total=models.Sum('amount')
        )['total'] or 0
        
        # Format as currency
        return f"${total_revenue:,.2f}"
    
    def get_trend(self):
        from django.db import models
        
        # Calculate revenue for this month vs last month
        now = timezone.now()
        this_month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        last_month_start = (this_month_start - timedelta(days=1)).replace(day=1)
        last_month_end = this_month_start - timedelta(seconds=1)
        
        this_month_revenue = Order.objects.filter(
            status='delivered',
            created_at__gte=this_month_start
        ).aggregate(total=models.Sum('amount'))['total'] or 0
        
        last_month_revenue = Order.objects.filter(
            status='delivered',
            created_at__gte=last_month_start,
            created_at__lte=last_month_end
        ).aggregate(total=models.Sum('amount'))['total'] or 0
        
        if last_month_revenue == 0:
            return 100 if this_month_revenue > 0 else 0
        
        return round(((this_month_revenue - last_month_revenue) / last_month_revenue) * 100, 1)
    
    def get_context_data(self):
        from django.db import models
        
        context = super().get_context_data()
        
        # Revenue this month
        now = timezone.now()
        this_month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        this_month_revenue = Order.objects.filter(
            status='delivered',
            created_at__gte=this_month_start
        ).aggregate(total=models.Sum('amount'))['total'] or 0
        
        context.update({
            'this_month_revenue': f"${this_month_revenue:,.2f}",
            'completed_orders': Order.objects.filter(status='delivered').count(),
        })
        
        return context
