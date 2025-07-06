# djangoProject/settings.py

from pathlib import Path
import os
from dotenv import load_dotenv

# BASE_DIR is correct. It points to the project root (where manage.py is).
BASE_DIR = Path(__file__).resolve().parent.parent

# --- NO LONGER NEEDED ---
# TEMPLATE_URL = ... (We will define this directly below)

# --- CORRECTED STATIC FILES PATH ---
STATICFILES_DIRS = [
    BASE_DIR / 'static', # Looks for a folder named 'static' in the project root.
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

load_dotenv(os.path.join(BASE_DIR, '.env'))

# --- The rest of your settings are mostly fine ---
DEBUG = os.getenv('DEBUG', 'False') == 'True'
SECRET_KEY = os.getenv('SECRET_KEY')
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "user",
    "nutrition",
    "exercise",
    "reminder",
    "suggestion",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "djangoProject.urls"

# --- CORRECTED TEMPLATES CONFIGURATION ---
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # This tells Django to look for a folder named 'templates' in the project root.
        'DIRS': [BASE_DIR / 'templates'], 
        'APP_DIRS': True, # This also lets Django find templates inside each app's 'templates' folder.
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'user.user_context.user_context_data',
            ],
        },
    },
]

WSGI_APPLICATION = "djangoProject.wsgi.application"

# ... (Your DATABASES, AUTH_PASSWORD_VALIDATORS, etc. remain the same) ...
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'health_tracker_db',
        'USER': 'health_tracker_user',
        'PASSWORD': 'Het2209#',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = False