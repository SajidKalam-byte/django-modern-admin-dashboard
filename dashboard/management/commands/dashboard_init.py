"""
Management command to initialize dashboard setup.
"""

import os
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Initialize dashboard setup and configuration'

    def add_arguments(self, parser):
        parser.add_argument(
            '--create-superuser',
            action='store_true',
            help='Create a superuser for dashboard access'
        )
        parser.add_argument(
            '--load-sample-data',
            action='store_true',
            help='Load sample data for demonstration'
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Initializing Custom Admin Dashboard...'))
        
        # Check if dashboard is properly configured
        self.check_configuration()
        
        # Run migrations
        self.stdout.write('Running migrations...')
        self.call_command('migrate')
        
        # Collect static files
        self.stdout.write('Collecting static files...')
        self.call_command('collectstatic', '--noinput')
        
        # Create superuser if requested
        if options['create_superuser']:
            self.create_superuser()
        
        # Load sample data if requested
        if options['load_sample_data']:
            self.load_sample_data()
        
        # Display next steps
        self.display_next_steps()

    def call_command(self, command, *args, **kwargs):
        """Call a Django management command."""
        from django.core.management import call_command as django_call_command
        django_call_command(command, *args, **kwargs)

    def check_configuration(self):
        """Check if dashboard is properly configured."""
        self.stdout.write('Checking configuration...')
        
        # Check if apps are installed
        required_apps = ['dashboard', 'dashboard_config', 'rest_framework']
        installed_apps = settings.INSTALLED_APPS
        
        missing_apps = [app for app in required_apps if app not in installed_apps]
        if missing_apps:
            self.stdout.write(
                self.style.WARNING(f"Missing apps in INSTALLED_APPS: {', '.join(missing_apps)}")
            )
        
        # Check dashboard configuration
        config = getattr(settings, 'CUSTOM_ADMIN_DASHBOARD_CONFIG', None)
        if not config:
            self.stdout.write(
                self.style.WARNING("CUSTOM_ADMIN_DASHBOARD_CONFIG not found in settings")
            )
        
        # Check if widgets are configured
        if config and not config.get('WIDGETS'):
            self.stdout.write(
                self.style.WARNING("No widgets configured in CUSTOM_ADMIN_DASHBOARD_CONFIG")
            )
        
        self.stdout.write(self.style.SUCCESS('Configuration check completed.'))

    def create_superuser(self):
        """Create a superuser for dashboard access."""
        from django.contrib.auth.models import User
        
        self.stdout.write('Creating superuser...')
        
        # Check if superuser already exists
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(
                self.style.WARNING('Superuser already exists. Skipping creation.')
            )
            return
        
        try:
            self.call_command('createsuperuser')
            self.stdout.write(self.style.SUCCESS('Superuser created successfully.'))
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING('Superuser creation cancelled.'))

    def load_sample_data(self):
        """Load sample data for demonstration."""
        from django.contrib.auth.models import User
        import random
        from decimal import Decimal
        
        self.stdout.write('Loading sample data...')
        
        # Create sample users
        sample_users = []
        for i in range(1, 11):
            user, created = User.objects.get_or_create(
                username=f'user{i}',
                defaults={
                    'first_name': f'User',
                    'last_name': f'{i}',
                    'email': f'user{i}@example.com',
                    'is_active': True,
                }
            )
            if created:
                user.set_password('demo123')
                user.save()
                sample_users.append(user)
        
        if sample_users:
            self.stdout.write(f'Created {len(sample_users)} sample users.')
        
        # Try to create sample orders if test_app is available
        try:
            from test_app.models import Order, Product, OrderItem
            
            # Create sample products
            sample_products = []
            product_names = ['Laptop', 'Phone', 'Tablet', 'Headphones', 'Camera']
            for name in product_names:
                product, created = Product.objects.get_or_create(
                    name=name,
                    defaults={
                        'description': f'Sample {name.lower()}',
                        'price': Decimal(str(random.randint(100, 1000))),
                        'stock_quantity': random.randint(5, 50),
                        'is_active': True,
                    }
                )
                if created:
                    sample_products.append(product)
            
            if sample_products:
                self.stdout.write(f'Created {len(sample_products)} sample products.')
            
            # Create sample orders
            all_users = list(User.objects.all())
            all_products = list(Product.objects.all())
            sample_orders = []
            
            for i in range(1, 21):
                order, created = Order.objects.get_or_create(
                    order_number=f'ORD-{i:04d}',
                    defaults={
                        'customer': random.choice(all_users),
                        'amount': Decimal(str(random.randint(50, 500))),
                        'status': random.choice(['pending', 'processing', 'shipped', 'delivered']),
                    }
                )
                if created:
                    sample_orders.append(order)
                    
                    # Create order items
                    num_items = random.randint(1, 3)
                    for _ in range(num_items):
                        product = random.choice(all_products)
                        OrderItem.objects.create(
                            order=order,
                            product=product,
                            quantity=random.randint(1, 3),
                            price=product.price,
                        )
            
            if sample_orders:
                self.stdout.write(f'Created {len(sample_orders)} sample orders.')
        
        except ImportError:
            self.stdout.write(
                self.style.WARNING('test_app not available. Skipping sample orders/products.')
            )
        
        self.stdout.write(self.style.SUCCESS('Sample data loaded successfully.'))

    def display_next_steps(self):
        """Display next steps for the user."""
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('Dashboard initialization completed!'))
        self.stdout.write('')
        self.stdout.write('Next steps:')
        self.stdout.write('1. Start your Django development server:')
        self.stdout.write('   python manage.py runserver')
        self.stdout.write('')
        self.stdout.write('2. Visit the dashboard at:')
        self.stdout.write('   http://127.0.0.1:8000/dashboard/')
        self.stdout.write('')
        self.stdout.write('3. Log in with your admin credentials')
        self.stdout.write('')
        self.stdout.write('4. Customize your dashboard by:')
        self.stdout.write('   - Adding widgets to CUSTOM_ADMIN_DASHBOARD_CONFIG')
        self.stdout.write('   - Creating custom widgets with: python manage.py create_dashboard_widget')
        self.stdout.write('   - Modifying the theme and settings')
        self.stdout.write('')
        self.stdout.write('For more information, see the documentation at:')
        self.stdout.write('https://github.com/yourname/custom-admin-dashboard')
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('Happy dashboard building! 🚀'))
