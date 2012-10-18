# -*- coding: utf-8 -*-
# Django settings for bricks_video_test project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    (u'Rafał Selewońko', 'rafal@selewonko.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '../../bricks_video_test.db3',
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

import os
import manage
PROJECT_PATH = os.path.dirname(manage.__file__)

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'gn^2v*l9w(alc(3fzmh@!r^9)6!w$(cv&amp;erdq=0a57a!je)y@4'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'bricks_video_test.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'bricks_video_test.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'bricks.media.videos',
    'djcelery',
)

import djcelery
djcelery.setup_loader()

BROKER_HOST = "localhost"
BROKER_PORT = 5672
BROKER_USER = "guest"
BROKER_PASSWORD = "guest"
BROKER_VHOST = "/"

CELERYD_CONCURRENCY = 2
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
CELERY_QUEUES = {
    "default": {
        "exchange": "celery",
        "queue_arguments": {"x-ha-policy": "all"},
        "binding_key": "celery"
    },
}

CELERY_DEFAULT_QUEUE = "default"

BRICKS_USE_CELERY = True
FFMPEG = '/usr/bin/avconv'
GREP = '/bin/grep'
GREP = '/bin/grep'
QT_FASTSTART = '/usr/bin/qt-faststart'
BRICKS_ALLOWED_VIDEO_FORMATS = ('3gp', 'avi', 'flv', 'mkv', 'mov', 'mp4', 'mpeg',
                         'mpg', 'ogg', 'ogv', 'wmv')
BRICKS_DEFAULT_CONVERTEDVIDEO_FORMATS = (5, 6, 7)
BRICKS_DEFAULT_CONVERTEDVIDEO_FORMAT = 6

BRICKS_VIDEO_ASPECT_RATIO_CHOICES = (
    (1.33, u'4:3'),
    (1.78, u'16:9')
)

BRICKS_VIDEO_FORMATS = {
    1: {
        'name': '270p',
        'slug': '270p',
        'codec': 'mp4',
        'extension': '.mp4',
        1.78: {  # 16:9
            'width': 480,
            'height': 270},
        1.33: {  # 4:3
            'width': 360,
            'height': 270},
#        'command': '{ffmpeg} -y -i {filename} -s {format_width}x{format_height} -vcodec libx264 -vprofile baseline '
#                   '-b:v 300k -r 30 -acodec copy -b:a 64k -ac 2 -strict -2 -moov_size 30000 {format_filename}',
        'command': '{ffmpeg} -y -i {filename} -s {format_width}x{format_height} -vcodec libx264 -vprofile baseline '
                   '-b:v 300k -r 30 -acodec copy -b:a 64k -ac 2 -strict -2 {format_filename}',
        'fallback': None,
    },

    2: {
        'name': '360p',
        'slug': '360p',
        'codec': 'mp4',
        'extension': '.mp4',
        1.78: {  # 16:9
            'width': 640,
            'height': 360},
        1.33: {  # 4:3
            'width': 478,
            'height': 360},
#        'command': '{ffmpeg} -y -i {filename} -s {format_width}x{format_height} -vcodec libx264 -vprofile baseline '
#                   '-b:v 512k -r 30 -acodec copy -b:a 96k -ac 2 -strict -2 -moov_size 30000 {format_filename}',
        'command': '{ffmpeg} -y -i {filename} -s {format_width}x{format_height} -vcodec libx264 -vprofile baseline '
                   '-b:v 512k -r 30 -acodec copy -b:a 96k -ac 2 -strict -2 {format_filename}',
        'fallback': 1,
    },

    3: {
        'name': '576p',
        'slug': '576p',
        'codec': 'mp4',
        'extension': '.mp4',
        1.78: {  # 16:9
            'width': 1024,
            'height': 576},
        1.33: {  # 4:3
            'width': 768,
            'height': 576},
#        'command': '{ffmpeg} -y -i {filename} -s {format_width}x{format_height} -vcodec libx264 -vprofile baseline '
#                   '-b:v 1600k -r 30 -acodec copy -b:a 112k -ac 2 -strict -2 -moov_size 30000 {format_filename}',
        'command': '{ffmpeg} -y -i {filename} -s {format_width}x{format_height} -vcodec libx264 -vprofile baseline '
                   '-b:v 1600k -r 30 -acodec copy -b:a 112k -ac 2 -strict -2 {format_filename}',
        'fallback': 1,
    },
}

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
