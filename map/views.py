from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.template import RequestContext


def show(request):

    return render_to_response('index.html', {
    }, context_instance=RequestContext(request))
