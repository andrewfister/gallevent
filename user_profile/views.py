import logging
from copy import copy

from django.views.generic.base import TemplateView
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from django_extra.login_required import LoginRequiredMixin

from models import UserProfile
from forms import UserProfileBioForm, UserProfileBasicInfoForm, UserProfileContactForm, UserProfileEducationForm, UserProfileWorkForm

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
        
        logger.info("profile: {} {} {} {} {} {} {} {} {} {}".format(profile.fname, profile.lname, profile.city, profile.state, profile.bio, profile.twitter, profile.facebook, profile.website, profile.email, profile.phone))
        profile_view_info = {'profile': profile}
        form_edit = request.GET.get("form_edit", "no_form")
        logger.info('form edit thing: {}'.format(form_edit))
        if form_edit == 'bio' or not (profile.fname and profile.lname and profile.city and profile.state and profile.bio and profile.twitter and profile.facebook and profile.website):
            profile_view_info['form_edit_bio'] = True
        if form_edit == 'basic_info' or not (profile.gender and profile.interests and profile.relationship):
            profile_view_info['form_edit_basic_info'] = True
        if form_edit == 'contact' or not (profile.email and profile.phone):
            profile_view_info['form_edit_contact'] = True
        if form_edit == 'education' or not (profile.school and profile.study_field):
            profile_view_info['form_edit_education'] = True
        if form_edit == 'work' or not (profile.job_title and profile.company):
            profile_view_info['form_edit_work'] = True
        
        logger.info("profile_view_info: {}".format(profile_view_info))
        return self.render_to_response(profile_view_info)
    
    def post(self, request):
        profile = UserProfile.objects.get(user_id=request.user.id)
        logger.debug("posty: {}".format(request.POST))
        
        form_type = request.POST.get('form_type')
        
        if form_type == 'bio':
            profile_form = UserProfileBioForm(request.POST, instance=profile)
        elif form_type == 'basic_info':
            interests = ','.join(request.POST.getlist('interests'))
            modified_post = copy(request.POST)
            modified_post.__setitem__('interests', interests)
            logger.info('modified_post: {}'.format(modified_post))
            profile_form = UserProfileBasicInfoForm(modified_post, instance=profile)
        elif form_type == 'contact':
            profile_form = UserProfileContactForm(request.POST, instance=profile)
        elif form_type == 'education':
            profile_form = UserProfileEducationForm(request.POST, instance=profile)
        elif form_type == 'work':
            profile_form = UserProfileWorkForm(request.POST, instance=profile)
        
        if profile_form.is_valid():
            profile_form.save()
            profile = UserProfile.objects.get(user_id=request.user.id)
        else:
            logger.info('UserProfile validation errors: {}'.format(profile_form.errors))
        
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
