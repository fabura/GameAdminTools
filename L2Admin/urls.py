from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
from django.conf import settings

urlpatterns = patterns('',
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon.ico')),
    url(r'^static/(?P<path>.*)$', "django.views.static.serve",
        {'document_root': settings.STATIC_ROOT,
         'show_indexes': True}),
    # Examples:
    # url(r'^$', 'L2Admin.views.home', name='home'),
    # url(r'^L2Admin/', include('L2Admin.foo.urls')),
    url(r'^$', "web.views.index"),
    url(r'^users/', include('web.users.urls')),
    url(r'^actions/', include('blocking.urls')),
    url(r'^monitoring/', include('web.monitoring.urls')),

    #    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root' : settings.STATIC_ROOT})
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)