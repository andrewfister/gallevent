from django.shortcuts import render_to_response
from django.template import RequestContext

def show_profile(request):
    return render_to_response('your-profile.html', {
    }, context_instance=RequestContext(request))
