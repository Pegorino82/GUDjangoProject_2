"""
Django settings for myshop project.

Generated by 'django-admin startproject' using Django 2.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import json

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'db+wxw4oi9c3vn78!__!qfxijw6&e$1_2g8!lj9h2usidfl-4$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',
    'contacts',
    'products',
    'images',
    'customers',
    'myshopadmin',
    'basket',
    'authapp',
    'ordersapp',

    'social_django',
    'rest_framework',
    'debug_toolbar',
    'template_profiler_panel',
    'django_extensions',
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.vk.VKOAuth2',
)

SOCIAL_AUTH_URL_NAMESPACE = 'social'

# Google+ загружаем секреты из файла
with open('./googleAuthSecret.json', 'r') as f:
    GOOGLE_PLUS = json.load(f)

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = GOOGLE_PLUS['client_id']
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = GOOGLE_PLUS['client_secret']

# VK загружаем секреты из файла
with open('./vkAuthSecret.json', 'r') as f:
    VK = json.load(f)

SOCIAL_AUTH_VK_OAUTH2_KEY = VK['client_id']
SOCIAL_AUTH_VK_OAUTH2_SECRET = VK['client_secret']

# SOCIAL_AUTH_VK_OAUTH2_SCOPE = ['friends']


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

if DEBUG:
    def show_toolbar(request):
        return True

    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': show_toolbar,
    }

    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
        'debug_toolbar.panels.profiling.ProfilingPanel',
        'template_profiler_panel.panels.template.TemplateProfilerPanel',
    ]

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 3,

    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

ROOT_URLCONF = 'myshop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'myshop', 'templates'),  # здесь шаблоны
        ],
        'APP_DIRS': True,  # позволяет искать шаблоны внутри установленных приложений
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'basket.context_processors.basket',  # свой контекстный процессор
            ],
        },
    },
]

WSGI_APPLICATION = 'myshop.wsgi.application'

# Email settings

DOMAIN_NAME = 'http://localhost:8000'
EMAIL_HOST = 'localhost'
# EMAIL_HOST = 'smtp'  # Для docker контейнера
EMAIL_PORT = '25'
EMAIL_HOST_USER = None
EMAIL_HOST_PASSWORD = None
EMAIL_USE_SSL = False


# with open('./smtpSecret.json', 'r') as f:
#     smtp = json.load(f)
#
# DOMAIN_NAME = '192.168.1.98'
# EMAIL_HOST = smtp['email_host']
# EMAIL_PORT = smtp['email_port']
# EMAIL_HOST_USER = smtp['email_host_user']
# EMAIL_HOST_PASSWORD = smtp['email_host_password']
# EMAIL_USE_SSL = True

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

with open('./postgresqlSecret.json', 'r') as f:
    postgres = json.load(f)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }

    # VM:
    #     'default': {
    #         'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #         'NAME': 'myshop',
    #         'USER': postgres['user'],
    #         'PASSWORD': postgres['password'],
    #         'HOST': 'localhost',
    #         'PORT': 5432  # для связи с контейнером docker
    #     }

    # docker:
    #     'default': {
    #         'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #         'NAME': 'postgres',
    #         'USER': 'postgres',
    #         'HOST': 'database',  # для связи с контейнером docker
    #         'PORT': 5432  # для связи с контейнером docker
    #     }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'customers.Customer'

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'myshop', 'static'),
)

# LOGIN_REDIRECT_URL = 'articlesapp:list'  # переделать на перенаправление в контроллере
# done
# def get_success_url(self):
#     return reverse_lazy('articlesapp:list')