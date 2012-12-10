from django.conf.urls import patterns, url, include

from bricks.core.views import tie_detail

_patterns = (
    url(r'^(?P<path>.*)/$', tie_detail, name='bricks_tie_detail'),
)

urlpatterns = patterns('', *_patterns)
