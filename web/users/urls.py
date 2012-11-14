__author__ = 'Bulat'

from django.conf.urls import patterns, url
from django.contrib.auth.views import login

urlpatterns = patterns('',
    # Examples:
    url(r'^register/?$', "web.users.views.register", name='register'),
    url(r'^login/?$', "web.users.views.user_login", name='login'),
    url(r'^logout/?$', "django.contrib.auth.views.logout", {'template_name': 'users/logout.html'}, name='logout'),
    url(r'^info/?$', "web.users.views.user_info", name='user_info'),
    url(r'^$', "web.users.views.index", name='index'),
)