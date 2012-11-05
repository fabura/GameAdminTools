__author__ = 'bulat.fattahov'

from django.conf.urls import patterns, url

urlpatterns = patterns('',
    # Examples:
    url(r'^block/?$', "blocking.views.block", name='block'),
    url(r'^block/json?$', "blocking.views.json", name='block'),
)