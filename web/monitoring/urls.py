__author__ = 'Bulat'

from django.conf.urls import patterns, url
from django.contrib.auth.views import login

urlpatterns = patterns('',
    # Examples:
    url(r'^/?savesettings$', "web.monitoring.views.savesettings", name='server'),
    url(r'^/?$', "web.monitoring.views.index", name="server"),
    url(r'^/?(?P<server>.*)$', "web.monitoring.views.server", name='server'),
)
