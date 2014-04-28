from django.views.generic.base import TemplateView
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from django_extra.login_required import LoginRequiredMixin

from models import UserProfile

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "profile.html"
    
    def get(self, request):
        try:
            profile = UserProfile.objects.get(user_id=request.user.id)
        except UserProfile.DoesNotExist:
            profile = UserProfile()
            profile.create_profile_for_user(request.user)
        
        return self.render_to_response({'profile': profile})

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
