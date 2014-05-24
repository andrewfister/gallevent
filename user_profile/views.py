import logging

from django.views.generic.base import TemplateView
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from django_extra.login_required import LoginRequiredMixin

from models import UserProfile
from forms import UserProfileForm

logger = logging.getLogger("gallevent")

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "profile.html"
    
    def get(self, request):
        try:
            profile = UserProfile.objects.get(user_id=request.user.id)
        except UserProfile.DoesNotExist:
            profile = UserProfile()
            profile.create_profile_for_user(request.user)
            logger.info("Created profile for user {} at {}".format(request.user.id, request.user.email))
        
        return self.render_to_response({'profile': profile})
    
    def post(self, request):
        profile = UserProfile.objects.get(user_id=request.user.id)
        logger.debug("posty: {}".format(request.POST))
        profile_form = UserProfileForm(request.POST, instance=profile)
        profile_form.save()
        
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
