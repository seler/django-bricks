from django.conf import settings

# b
USE_TINYMCE = getattr(settings, 'BRICKS_USE_TINYMCE', 'tinymce' in settings.INSTALLED_APPS)
