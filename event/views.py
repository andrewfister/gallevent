from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core import serializers

from djangbone.views import BackboneAPIView

from gallevent.event import forms
from gallevent.event import models

def show_front_page_events(request):
    events = models.Event.objects.filter(status=1)

    return render_to_response('index.html', {
    'events': events,
    }, context_instance=RequestContext(request))

@login_required
def post_event(request):
    import logging
    logging.debug('post event')
    if request.method == 'POST':
        form = forms.PostEventForm(request.POST)
        logging.debug('created a form')
        
        if form.is_valid():
            logging.debug('form is valid. the user is: ' + str(request.user.id))
            form.save()
            
            return HttpResponseRedirect('/event/show')
        else:
            logging.debug(form.errors)
    else:
        form = forms.PostEventForm()

    return render_to_response('post-event.html', {
    'edit': False,
    'form': form,
    }, context_instance=RequestContext(request))

@login_required
def edit_event(request):
    return render_to_response('post-event.html', {
    'edit': True
    }, context_instance=RequestContext(request))

@login_required
def show_events(request):
    events = models.Event.objects.filter(user_id=request.user.id).exclude(status=0)

    return render_to_response('your-posts.html', {
    'selected_page': 'your-posts',
    'events': events,
    }, context_instance=RequestContext(request))

@login_required
def show_lineup(request):
    return render_to_response('your-posts.html', {
    'selected_page': 'your-events'
    }, context_instance=RequestContext(request))

@login_required
def manage_events(request):
    return render_to_response('your-posts-manage.html', {
    }, context_instance=RequestContext(request))
    
class EventView(BackboneAPIView):
    base_queryset = models.Event.objects.exclude(status=0)
    
    edit_form_class = forms.ArchiveEventForm
    
    serialize_fields = ['id', 'user_id', 'address1', 'address2', 'city', 'state',
    'zipcode', 'name', 'category', 'ticket_price', 'start_date', 'start_time',
    'end_date', 'end_time', 'description', 'organizer_email', 'organizer_phone',
    'organizer_url', 'latitude', 'longitude', 'status']
    
    def dispatch(self, request, *args, **kwargs):
        if request.GET.has_key('userId'):
            self.base_queryset = models.Event.objects.filter(user_id=request.GET['userId']).exclude(status=0)
        elif request.GET.has_key('category'):
            self.base_queryset = models.Event.objects.filter(user_id=request.GET['category']).exclude(status=0)
        
        return super(EventView, self).dispatch(request, *args, **kwargs)
    
    def validation_error_response(self, form_errors):
        import logging
        logging.debug(form_errors)
        return str(form_errors)
