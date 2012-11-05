from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from settings import STATIC_ROOT

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'L2Admin.views.home', name='home'),
    # url(r'^L2Admin/', include('L2Admin.foo.urls')),
    url(r'^users/', include('web.users.urls')),
    url(r'^actions/', include('blocking.urls')),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': STATIC_ROOT}),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

)
