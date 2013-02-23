from django.conf import settings
from django.conf.urls import patterns, include, url
from django.http import HttpResponse

import os

urlpatterns = patterns('',
    url(r'^$', 'apps.home.views.index', name='index'),
    #url(r'^notes/(?P<path>.*)$', 'apps.notes.views.index', name='notes'),

    url(r'^robots\.txt$', 'apps.base.views.robots_txt'),
    url(r'^sitemap\.xml$', 'apps.base.views.sitemap'),
    url(r'^google8af796f5e4581853\.html$', 'apps.base.views.google_verification'),
    url(r'^' + settings.STATIC_URL[1:-1] + '/(?P<path>.*)$',
        'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    url(r'^project/(?P<path>.*)$', 'apps.base.views.project_access'),
)
