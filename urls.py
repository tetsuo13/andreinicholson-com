from django.conf import settings
from django.conf.urls import patterns, include, url
from django.http import HttpResponse

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

def robots_txt():
    return HttpResponse("""User-agent: *
Disallow:
Sitemap: http://andreinicholson.com/sitemap.xml""")

def sitemap():
    return HttpResponse("""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>http://andreinicholson.com</loc>
        <changefreq>monthly</changefreq>
    </url>
</urlset>""")

def google_verification():
    return HttpResponse('google-site-verification: google8af796f5e4581853.html')

urlpatterns = patterns('',
    url(r'^$', 'home.views.index', name='index'),

    url(r'^robots\.txt$', lambda r: robots_txt()),
    url(r'^sitemap\.xml$', lambda r: sitemap()),
    url(r'^google8af796f5e4581853\.html$', lambda r: google_verification()),

    url(r'^' + settings.STATIC_URL[1:-1] + '/(?P<path>.*)$',
        'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
