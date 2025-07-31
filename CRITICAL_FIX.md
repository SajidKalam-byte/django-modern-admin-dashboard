# CRITICAL FIX for NoReverseMatch Error

## The Real Problem
The error happens because:
1. You visit `/admin/` but you're not logged in
2. Django tries to redirect to login page using `settings.LOGIN_URL`
3. Django's default LOGIN_URL tries to use 'admin' namespace which we replaced
4. This causes the NoReverseMatch error

## Quick Fix - Add to your settings.py

Add these lines to your `settings.py` file:

```python
# Fix login/logout URLs for dashboard
LOGIN_URL = '/admin/login/'
LOGOUT_URL = '/admin/logout/'
LOGIN_REDIRECT_URL = '/admin/'
LOGOUT_REDIRECT_URL = '/admin/'
```

## Alternative Fix - Keep Both Admin and Dashboard

If you want to keep both interfaces, update your main `urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),        # Original Django admin
    path('dashboard/', include('dashboard.urls')),  # Custom dashboard
    # ... your other URLs
]
```

Then visit:
- Django Admin: `http://127.0.0.1:8000/admin/`
- Custom Dashboard: `http://127.0.0.1:8000/dashboard/`

## Steps to Fix Right Now

1. **Add LOGIN_URL to settings.py**:
```python
LOGIN_URL = '/admin/login/'
LOGIN_REDIRECT_URL = '/admin/'
```

2. **Create a superuser** (if you haven't):
```bash
python manage.py createsuperuser
```

3. **Restart server**:
```bash
python manage.py runserver
```

4. **Go to login first**:
```
http://127.0.0.1:8000/admin/login/
```

5. **Then access dashboard**:
```
http://127.0.0.1:8000/admin/
```

## Root Cause
The `@staff_member_required` decorator redirects unauthenticated users to login, but our URL setup broke the default login flow. The LOGIN_URL setting fixes this.
