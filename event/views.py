from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect

from djangbone.views import BackboneAPIView

from gallevent.event import forms
from gallevent.event import models


def post_event(request):
    import logging
    logging.debug('post event')
    if request.method == 'POST':
        form = forms.PostEventForm(request.POST)
        logging.debug('created a form')
        
        if form.is_valid():
            logging.debug('form is valid. the user is: ' + str(request.user.id))
            form.set_request(request);
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

def edit_event(request):
    return render_to_response('post-event.html', {
    'edit': True
    }, context_instance=RequestContext(request))

def show_events(request):
    events = models.Event.objects.filter(user_id=request.user.id)

    return render_to_response('your-posts.html', {
    'selected_page': 'your-posts',
    'events': events,
    }, context_instance=RequestContext(request))

def show_lineup(request):
    return render_to_response('your-posts.html', {
    'selected_page': 'your-events'
    }, context_instance=RequestContext(request))

def manage_events(request):
    return render_to_response('your-posts-manage.html', {
    }, context_instance=RequestContext(request))
    
class EventView(BackboneAPIView):
    base_queryset = models.Event.objects.all()
    
    serialize_fields = ['id', 'user_id', 'address1', 'address2', 'city', 'zipcode',
                        'name', 'ticket_price', 'start_date', 'end_date', 
                        'description', 'latitude', 'longitude']
    
    def dispatch(self, request, *args, **kwargs):
        self.base_queryset = models.objects.filter(user_id=request.user_id)
        return super(EventView, self).dispatch(*args, **kwargs)
