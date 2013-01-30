from django.conf import settings
from django.views.static import serve
from django.http import HttpResponse

import os

def project_access(request, path):
    from piwikapi.tracking import PiwikTracker

    pt = PiwikTracker(9, request)
    pt.set_api_url('http://analytics.andreinicholson.com/piwik.php')

    # TODO: Using server IP address unfortunately. Piwik token auth is secret.
    #pt.set_ip(request.META['REMOTE_ADDR'])
    #pt.set_token_auth('')

    pt.do_track_page_view(path)

    show_indexes = False

    if len(path) > 1:
        # Allow showing directory indexes for select projects.
        if path[0:12] == 'keepasstordp':
            show_indexes = True

    return serve(request, path, os.path.join(settings.ROOT, 'project'),
                 show_indexes)
