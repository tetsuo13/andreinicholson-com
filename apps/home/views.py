from django.http import HttpResponse
from django.template import Context, loader, RequestContext

def index(request):
    dictionary = {
        'current_nav': 'home'
    }

    t = loader.get_template('index.html')
    c = RequestContext(request, dictionary)
    response = HttpResponse(t.render(c), mimetype='text/html; charset=utf-8')
    response['X-UA-Compatible'] = 'IE=edge,chrome=1'
    return response
