from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from d3_analytics.actions import Analytics
analytics = Analytics()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'd3_analytics.views.home', name='home'),
    url(r'^analytics/', include(analytics.urls)),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
