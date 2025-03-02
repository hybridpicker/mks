"""
Django settings for mks project.

Generated by 'django-admin startproject' using Django 2.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# Secret Key stored in local_settings
SECRET_KEY = 'jb#172ifl0xe55c9ed(=9i4erh*oj3nj)in%$9s3*1o9hr#$v^'

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
    'django.contrib.sites',
    'django_extensions',
    #'debug_toolbar',
    'users.apps.UsersConfig',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # mks_apps
    'phone_field',
    'location.apps.LocationConfig',
    'students.apps.StudentsConfig',
    'teaching.apps.TeachingConfig',
    'home',
    'ckeditor',
    'ckeditor_uploader',
    'blog.apps.BlogConfig',
    'school.apps.SchoolConfig',
    'instruments.apps.InstrumentsConfig',
    'events.apps.EventsConfig',
    'gallery.apps.GalleryConfig',
    'contact.apps.ContactConfig',
    'controlling.apps.ControllingConfig',
    'downloadsection.apps.DownloadsectionConfig',
    'todo',
    'projects.apps.ProjectsConfig',
    'faq.apps.FaqConfig',
    'invitation.apps.InvitationConfig',
    #sitemaps
    'django.contrib.sitemaps',
    #thumbnails
    'sorl.thumbnail',
    #user-agents
    'django_user_agents',
    #excel-export
    'xlwt',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mks.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mks.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mks',
        'USER': 'postgres',
        'PASSWORD': 'Ax9kl3',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators


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

AUTH_USER_MODEL = 'users.CustomUser'

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",

    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)

SITE_ID = 1

#LOGIN SUCESS TO URL
LOGIN_REDIRECT_URL = '/team/'

#LOGUT
LOGOUT_REDIRECT_URL = '/'

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)
# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'de'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

CKEDITOR_UPLOAD_PATH = "/media/blog_uploads/"

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    #'/var/www/static/',
]

STATIC_ROOT = os.path.join(BASE_DIR, 'static_cdn')

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

FIXTURE_DIRS = [
    os.path.join(BASE_DIR, 'fixtures'),
]

EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_USER_RECEIVER = 'musikschule@st-poelten.gv.at'

DEFAULT_AUTO_FIELD='django.db.models.AutoField' 

THUMBNAIL_FORCE_OVERWRITE = True

USER_AGENTS_CACHE = 'default'

APPEND_SLASH = True

if os.path.isfile(os.path.join(BASE_DIR, 'local_settings.py')):
    from local_settings import *
