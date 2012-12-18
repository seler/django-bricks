from django.conf import settings


USE_TINYMCE = getattr(settings, 'BRICKS_USE_TINYMCE', 'tinymce' in settings.INSTALLED_APPS)
