from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User

#from djangbone.views import BackboneAPIView

def show_profile(request):
    return render_to_response('profile.html', {
    }, context_instance=RequestContext(request))
	
def show_datebook(request):
    return render_to_response('datebook.html', {
    }, context_instance=RequestContext(request))

def show_posts(request):
    return render_to_response('posts.html', {
    }, context_instance=RequestContext(request))

def show_groups(request):
    return render_to_response('groups.html', {
    }, context_instance=RequestContext(request))