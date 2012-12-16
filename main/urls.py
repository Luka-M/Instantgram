from django.conf.urls import patterns, url

urlpatterns = patterns('',
    # /
    url(r'^$', 'main.views.index'),
	# /tag/XXX
    url(r'^tag/(?P<tagtext>\w+)/$', 'main.views.tag'),
    # /upload/
    url(r'^upload/$', 'main.views.upload'),
    # /upload2/
    url(r'^upload2/$', 'main.views.upload2'),
    # /embed/
    url(r'^embed/(?P<tagtext>\w+)/$','main.views.embed'),
    # /embedtest/
    url(r'^embedtest/$','main.views.embedtest'),

)