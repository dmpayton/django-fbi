from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django_fbi.app import apps
from django_fbi.backends import get_backend
from django_fbi.decorators import facebook_request
from django_fbi.models import FacebookAccount
from django_fbi.signals import facebook_deauthorize

FBI_BACKEND = getattr(settings, 'FBI_BACKEND', 'django_fbi.backends.DefaultBackend')

def channel(request):
    return HttpResponse('<script src="//connect.facebook.net/en_US/all.js"></script>')

#@facebook_request
def connect(request):
    facebook_backend = get_backend(FBI_BACKEND)
    return facebook_backend(request).connect_view()

@facebook_request
def deauthorize(request):
    facebook_backend = get_backend(FBI_BACKEND)
    return facebook_backend(request).deauthorize_view()

@facebook_request
def view_app(request, slug, page):
    try:
        ## Check the registry to see if we have Python app.
        app = apps[slug]
        return getattr('%s_view' % page, app)(request)
    except (KeyError, NotImplemented):
        ## Nothing registered, check the database.
        app = get_object_or_404(FacebookApp, namespace=slug)
        context = RequestContext(request, {'app': app})
        page_template = getattr(app, '%s_template' % page)
        if page_template:
            return render_to_response(page_template, context)
        page_content = getattr(app, '%s_content' % page)
        return HttpResponse(Template(page_content).render(context))
