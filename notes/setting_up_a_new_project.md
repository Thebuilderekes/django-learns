# Django Project Setup Checklist & Troubleshooting Guide

A comprehensive guide based on common issues and best practices for setting up a Django project.

---

## Phase 1: Environment Setup

### 1.1 Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Verify activation (should show venv path)
which python  # Mac/Linux
where python  # Windows
```

**✅ Check:** Your terminal prompt should show `(venv)` prefix

### 1.2 Install Django
```bash
# Install Django
pip install django

# Verify installation
python -m django --version

# Install other common packages
pip install pillow  # For image handling
pip install python-decouple  # For environment variables
pip install django-crispy-forms  # For better form styling (optional)

# Create requirements.txt
pip freeze > requirements.txt
```

**✅ Check:** Django version should display (e.g., 5.0.1)

---

## Phase 2: Project Creation

### 2.1 Create Project and App
```bash
# Create project
django-admin startproject myproject .
# Note: The dot (.) creates project in current directory

# Create app
python manage.py startapp myapp

# Directory structure should look like:
# myproject/
#   ├── myproject/
#   │   ├── __init__.py
#   │   ├── settings.py
#   │   ├── urls.py
#   │   ├── asgi.py
#   │   └── wsgi.py
#   ├── myapp/
#   │   ├── migrations/
#   │   ├── __init__.py
#   │   ├── admin.py
#   │   ├── apps.py
#   │   ├── models.py
#   │   ├── tests.py
#   │   └── views.py
#   ├── manage.py
#   └── venv/
```

**✅ Check:** `manage.py` exists in root directory

---

## Phase 3: Settings Configuration

### 3.1 Update INSTALLED_APPS
```python
# myproject/settings.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',      # ← Required for sessions
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp',  # ← Add your app here
]
```

**✅ Check:** Your app name matches the app directory name

**⚠️ Common Issue:** Forgetting to add your app causes "No module named 'myapp'" errors

### 3.2 Configure Middleware
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # ← Required
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',  # ← Required for forms
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # ← Required
    'django.contrib.messages.middleware.MessageMiddleware',  # ← Required
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

**✅ Check:** All default middleware present, especially SessionMiddleware

**⚠️ Common Issue:** Missing SessionMiddleware causes session-related errors

### 3.3 Configure Templates
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # ← Add this for project-level templates
        'APP_DIRS': True,  # ← Must be True for app templates
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # ← Required
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

**✅ Check:** 'request' context processor is included

**⚠️ Common Issue:** Missing context processors causes template variable errors

### 3.4 Configure Static Files
```python
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']  # Development static files
STATIC_ROOT = BASE_DIR / 'staticfiles'    # Production collected static files

# For media files (user uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

**✅ Check:** Create `static` and `media` directories in project root

### 3.5 Configure Database
```python
# Default SQLite (good for development)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# For PostgreSQL (production):
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'mydb',
#         'USER': 'myuser',
#         'PASSWORD': 'mypassword',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }
```

### 3.6 Configure Session Settings
```python
# Session configuration (prevents session errors)
SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # ← Use database sessions
SESSION_COOKIE_AGE = 1209600  # 2 weeks
SESSION_SAVE_EVERY_REQUEST = False
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
```

**⚠️ Common Issue:** Session errors if session backend not configured

### 3.7 Configure Messages Framework
```python
from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',  # Bootstrap class
}
```

### 3.8 Configure Authentication
```python
# Login/Logout URLs
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Password validation (keep default for security)
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
```

### 3.9 Other Important Settings
```python
# Timezone and Language
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'  # Or your timezone: 'America/New_York', 'Europe/London', etc.
USE_I18N = True
USE_TZ = True  # ← Keep this True for timezone awareness

# Security settings (for production)
# DEBUG = False  # Set to False in production
# ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
```

---

## Phase 4: Directory Structure Setup

### 4.1 Create Template Directories
```bash
# Create template directories
mkdir -p templates
mkdir -p myapp/templates/myapp

# Structure:
# templates/           ← Project-level templates (base.html, etc.)
# myapp/templates/myapp/  ← App-specific templates
```

**✅ Check:** Templates directory exists and is in TEMPLATES DIRS

### 4.2 Create Static Directories
```bash
# Create static directories
mkdir -p static/css
mkdir -p static/js
mkdir -p static/images

# Create media directory
mkdir -p media
```

### 4.3 Create Management Commands Directory (Optional)
```bash
# For custom management commands
mkdir -p myapp/management/commands
touch myapp/management/__init__.py
touch myapp/management/commands/__init__.py
```

---

## Phase 5: Initial Migrations

### 5.1 Create and Run Migrations
```bash
# Create initial migrations
python manage.py makemigrations

# Check migration plan (optional)
python manage.py showmigrations

# Run migrations
python manage.py migrate

# Expected output:
# Running migrations:
#   Applying contenttypes.0001_initial... OK
#   Applying auth.0001_initial... OK
#   Applying admin.0001_initial... OK
#   Applying sessions.0001_initial... OK
#   ...
```

**✅ Check:** `db.sqlite3` file created in project root

**⚠️ Common Issue:** "no such table: django_session"
- **Solution:** Run `python manage.py migrate` to create session table

### 5.2 Create Superuser
```bash
python manage.py createsuperuser

# Follow prompts:
# Username: admin
# Email: admin@example.com
# Password: ******** (minimum 8 characters)
```

**✅ Check:** You can login at `http://127.0.0.1:8000/admin/`

---

## Phase 6: URL Configuration

### 6.1 Project URLs
```python
# myproject/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),  # ← Include app URLs
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

### 6.2 App URLs
```python
# myapp/urls.py (create this file)
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
]
```

**✅ Check:** Create `urls.py` in your app directory if it doesn't exist

**⚠️ Common Issue:** "ModuleNotFoundError: No module named 'myapp.urls'"
- **Solution:** Create `myapp/urls.py` file

---

## Phase 7: Create Base Templates

### 7.1 Base Template
```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}My Site{% endblock %}</title>
    
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    
    <!-- Custom CSS -->
    {% load static %}
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
    
    {% block extra_css %}{% endblock %}
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="{% url 'home' %}">My Site</a>
            <div class="navbar-nav ms-auto">
                {% if user.is_authenticated %}
                    <span class="navbar-text me-3">Hello, {{ user.username }}</span>
                    <a class="nav-link" href="{% url 'admin:logout' %}">Logout</a>
                {% else %}
                    <a class="nav-link" href="{% url 'admin:login' %}">Login</a>
                {% endif %}
            </div>
        </div>
    </nav>

    <!-- Messages -->
    {% if messages %}
    <div class="container mt-3">
        {% for message in messages %}
        <div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
            {{ message }}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
        {% endfor %}
    </div>
    {% endif %}

    <!-- Main Content -->
    <main>
        {% block content %}{% endblock %}
    </main>

    <!-- Footer -->
    <footer class="bg-dark text-white text-center py-3 mt-5">
        <p>&copy; 2024 My Site. All rights reserved.</p>
    </footer>

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    
    {% block extra_js %}{% endblock %}
</body>
</html>
```

**✅ Check:** Template loads without errors

---

## Phase 8: Create Initial Views

### 8.1 Basic View
```python
# myapp/views.py
from django.shortcuts import render

def home(request):
    context = {
        'title': 'Home Page',
    }
    return render(request, 'myapp/home.html', context)
```

### 8.2 Template for View
```html
<!-- myapp/templates/myapp/home.html -->
{% extends 'base.html' %}

{% block title %}{{ title }}{% endblock %}

{% block content %}
<div class="container mt-5">
    <h1>Welcome to My Site!</h1>
    <p>This is the home page.</p>
</div>
{% endblock %}
```

---

## Phase 9: Test the Setup

### 9.1 Run Development Server
```bash
python manage.py runserver

# Expected output:
# Watching for file changes with StatReloader
# Performing system checks...
# System check identified no issues (0 silenced).
# December 15, 2024 - 15:30:45
# Django version 5.0.1, using settings 'myproject.settings'
# Starting development server at http://127.0.0.1:8000/
# Quit the server with CTRL-BREAK.
```

**✅ Check:** No errors in console

### 9.2 Test These URLs
1. `http://127.0.0.1:8000/` - Home page
2. `http://127.0.0.1:8000/admin/` - Admin login
3. Login with superuser credentials

**✅ Check:** All pages load without errors

---

## Phase 10: Version Control Setup

### 10.1 Create .gitignore
```bash
# Create .gitignore file
cat > .gitignore << EOF
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# Django
*.log
db.sqlite3
db.sqlite3-journal
/media/
/staticfiles/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Environment variables
.env
EOF
```

### 10.2 Initialize Git
```bash
git init
git add .
git commit -m "Initial Django project setup"
```

---

## Common Issues & Solutions

### Issue 1: "No such table: django_session"
**Symptoms:** Session-related errors, admin login fails
**Solution:**
```bash
python manage.py migrate
python manage.py migrate sessions
```

### Issue 2: "AttributeError: 'SessionStore' object has no attribute '_session_cache'"
**Symptoms:** Session errors after Django upgrade
**Solution:**
```bash
python manage.py clearsessions
python manage.py migrate
# Restart server
# Clear browser cookies
```

### Issue 3: "CSRF verification failed"
**Symptoms:** Form submission fails
**Solution:**
- Add `{% csrf_token %}` in every form
- Check CSRF middleware is enabled
- Check 'django.template.context_processors.csrf' in context processors

### Issue 4: "Template does not exist"
**Symptoms:** TemplateDoesNotExist error
**Solution:**
- Check template path matches: `myapp/templates/myapp/home.html`
- Verify `APP_DIRS = True` in TEMPLATES
- Check app is in INSTALLED_APPS
- Restart development server

### Issue 5: "No reverse match for 'url_name'"
**Symptoms:** {% url %} tag fails
**Solution:**
- Check URL name in urls.py matches
- Verify namespace if using `include()`
- Check URL pattern arguments match

### Issue 6: Static files not loading
**Symptoms:** CSS/JS/Images don't appear
**Solution:**
```python
# settings.py
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# In template
{% load static %}
<link rel="stylesheet" href="{% static 'css/style.css' %}">
```

### Issue 7: "Class 'Model' has no 'objects' member"
**Symptoms:** Pylint/PyRight errors
**Solution:**
- This is a false positive from type checkers
- Add `# type: ignore` or `# pylint: disable=no-member`
- Or install `django-stubs`: `pip install django-stubs`

### Issue 8: "Can't find '__main__' module"
**Symptoms:** Running wrong Python file
**Solution:**
- Always run `python manage.py runserver`
- Don't run Python files directly in Django projects

### Issue 9: Database locked error (SQLite)
**Symptoms:** "database is locked" when saving
**Solution:**
- Close other database connections
- Use PostgreSQL for production
- Restart development server

### Issue 10: Port already in use
**Symptoms:** "Error: That port is already in use"
**Solution:**
```bash
# Use different port
python manage.py runserver 8001

# Or kill process using port 8000
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux:
lsof -ti:8000 | xargs kill -9
```

---

## Pre-Deployment Checklist

### Security Settings
```python
# In production settings
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
SECRET_KEY = os.environ.get('SECRET_KEY')  # Use environment variable
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
```

### Collect Static Files
```bash
python manage.py collectstatic
```

### Check for Issues
```bash
python manage.py check
python manage.py check --deploy
```

---

## Useful Commands Reference

```bash
# Create project
django-admin startproject projectname

# Create app
python manage.py startapp appname

# Migrations
python manage.py makemigrations
python manage.py migrate
python manage.py showmigrations
python manage.py sqlmigrate appname 0001

# User management
python manage.py createsuperuser
python manage.py changepassword username

# Shell
python manage.py shell
python manage.py dbshell

# Static files
python manage.py collectstatic
python manage.py findstatic filename.css

# Testing
python manage.py test
python manage.py test appname

# Database
python manage.py dumpdata > backup.json
python manage.py loaddata backup.json
python manage.py flush  # Clear database

# Sessions
python manage.py clearsessions

# Development
python manage.py runserver
python manage.py runserver 8001  # Different port
python manage.py runserver 0.0.0.0:8000  # External access
```

---

## Quick Setup Script

Save this as `setup.sh` (Mac/Linux) or `setup.bat` (Windows):

```bash
#!/bin/bash
# Quick Django setup script

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install Django
pip install django pillow

# Create project
django-admin startproject myproject .

# Create app
python manage.py startapp myapp

# Create directories
mkdir -p templates static/css static/js media

# Run migrations
python manage.py migrate

# Create superuser
echo "Creating superuser..."
python manage.py createsuperuser

# Start server
python manage.py runserver
```

---

## Resources

- **Official Django Documentation:** https://docs.djangoproject.com/
- **Django Tutorial:** https://docs.djangoproject.com/en/stable/intro/tutorial01/
- **Django Best Practices:** https://django-best-practices.readthedocs.io/
- **Two Scoops of Django:** Book on Django best practices
- **Real Python Django Tutorials:** https://realpython.com/tutorials/django/

Remember: When in doubt, check the official Django documentation first!
