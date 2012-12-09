from django.conf.urls import patterns, url

urlpatterns = patterns('',
    # /
    url(r'^$', 'main.views.index'),
	# /tag/XXX
    url(r'^tag/(?P<tagtext>\w+)/$', 'main.views.tag'),
    # /upload/
    url(r'^upload/(?P<tagtext>\w+)/$', 'main.views.upload'),
    # /upload2/
    url(r'^upload2/(?P<tagtext>\w+)/$', 'main.views.upload2'),

)