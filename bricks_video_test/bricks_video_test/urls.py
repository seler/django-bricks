from django.conf.urls import include, url
from django.conf.urls import patterns as _patterns

from django.contrib import admin
admin.autodiscover()

patterns = (
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    # musi byc ostatnie jezeli puste
    url(r'^', include('bricks.urls')),
)

urlpatterns = _patterns('', *patterns)
