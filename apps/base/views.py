from django.conf import settings
from django.views.static import serve
from django.http import HttpResponse

import os

def robots_txt(request):
    robots = ['User-agent: *']

    if request.get_host().startswith('beta.'):
        robots.append('Disallow: /')
    else:
        robots.append('Disallow:')
        robots.append('Sitemap: http://andreinicholson.com/sitemap.xml')

    return HttpResponse('\n'.join(robots))

def google_verification(request):
    return HttpResponse('google-site-verification: google8af796f5e4581853.html')

def sitemap(request):
    return HttpResponse("""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>http://andreinicholson.com</loc>
        <changefreq>monthly</changefreq>
    </url>
</urlset>""")

def project_access(request, path):
    from piwikapi.tracking import PiwikTracker

    pt = PiwikTracker(9, request)
    pt.set_api_url('http://analytics.andreinicholson.com/piwik.php')
    pt.set_ip(request.META['REMOTE_ADDR'])
    pt.set_token_auth(request.session.get('piwik_token_auth',
                                          get_piwik_token_auth()))
    pt.do_track_page_view(path)

    show_indexes = False

    if len(path) > 1:
        # Allow showing directory indexes for select projects.
        if path[0:12] == 'keepasstordp':
            show_indexes = True

    return serve(request, path, os.path.join(settings.ROOT, 'project'),
                 show_indexes)

def get_piwik_token_auth():
    """Get the Piwik token auth from the static file if exists
    """
    try:
        auth = open(os.path.join(settings.STATIC_ROOT, 'piwik_token_auth.txt'),
                    'r').read().strip()
    except IOError:
        # Match default value from PiwikTracker.
        auth = False
    return auth

