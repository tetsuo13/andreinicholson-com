from django.http import HttpResponse
from django.template import Context, loader, RequestContext

from random import choice

def index(request):
    instagram_links = [
        'http://instagr.am/p/azDxS/',
        'http://instagr.am/p/cmgaZ/',
        'http://instagr.am/p/cml3y/',
        'http://instagr.am/p/cvTrP/',
        'http://instagr.am/p/G7Bh1/',
        'http://instagr.am/p/HlCpW/',
        'http://instagr.am/p/hSP_R/',
        'http://instagr.am/p/Hy7S0/',
        'http://instagr.am/p/J_a6d/',
        'http://instagr.am/p/JvDu0/',
        'http://instagr.am/p/KH35z/',
        'http://instagr.am/p/KRHvL/',
        'http://instagr.am/p/KLmWp/',
        'http://instagr.am/p/Kztpg/',
        'http://instagr.am/p/X__k_/',
        'http://instagr.am/p/Zgi5n/'
    ]

    dictionary = {
        'instagram_link': choice(instagram_links),
        'current_nav': 'home'
    }

    t = loader.get_template('index.html')
    c = RequestContext(request, dictionary)
    response = HttpResponse(t.render(c), mimetype='text/html; charset=utf-8')
    response['X-UA-Compatible'] = 'IE=edge,chrome=1'
    return response
