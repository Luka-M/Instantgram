from django.conf.urls import patterns, include, url
from main.api.resources import ImageResource, TagResource
from tastypie.api import Api

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(ImageResource())
v1_api.register(TagResource())


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'instantgram.views.home', name='home'),
    # url(r'^instantgram/', include('instantgram.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^api/', include(v1_api.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^static/(?P<path>.*)$', 'serve'),
    url(r'^', include('main.urls')),
)
