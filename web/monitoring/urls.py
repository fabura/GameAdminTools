__author__ = 'Bulat'

from django.conf.urls import patterns, url
from django.contrib.auth.views import login

urlpatterns = patterns('',
    # Examples:
    url(r'^/?(?P<server>.*)$', "web.monitoring.views.server", name='server'),
)