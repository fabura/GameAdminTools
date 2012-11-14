from django.conf.urls import patterns, include, url
import django.views.static

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
from settings import STATIC_URL
import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'L2Admin.views.home', name='home'),
    # url(r'^L2Admin/', include('L2Admin.foo.urls')),
    url(r'^$', "web.views.index"),
    url(r'^users/', include('web.users.urls')),
    url(r'^actions/', include('blocking.urls')),
    url(r'^monitoring/', include('web.monitoring.urls')),
    url(r'^static/(?P<path>.*)$', django.views.static.serve,
            {'document_root': settings.STATIC_ROOT}),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)