import logging
import json

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from django.views.generic.base import TemplateView, View

from event import forms
from event import models


class FrontPageView(TemplateView):
    template_name = "index.html"
    
    def get(self, request):
        logging.debug('front page')
        
        try:
            timeSpan = request.GET['timeSpan']
        except KeyError:
            timeSpan = ""

        return self.render_to_response({
            'timeSpan': timeSpan
            })


class SearchView(View):
    def get(self, request):
        logging.debug('search')
        #events = models.Event.objects.filter(status=1) \
        #        .extra(where=['end_date >= CURRENT_TIMESTAMP']) \
        #        .order_by('start_date','start_time').reverse()

        if request.GET.get('q'):
            form = forms.EventBriteSearchForm(request.GET)
            if form.is_valid():
                logging.debug('doing a search')
                events = form.search()
        
        logging.debug('request data: ' + str(request.GET))
        
        if len(events) == 0:
            events = "[]"

        events_json = json.dumps(events)

        return HttpResponse(events_json, content_type="application/json")

@login_required
def post_event(request, event_id=None, edit=False):
    if request.method == 'POST':
        if event_id != None and edit == True:
            event = models.Event.objects.get(id=event_id)
        else:
            event = models.Event(user_id=request.user.id)
        form = forms.PostEventForm(request.POST, instance=event)
        
        if form.is_valid():
            form.save()
            
            return HttpResponseRedirect('/event/show')
        else:
            logging.debug(form.errors)
    elif event_id != None and edit == True:
        event = models.Event.objects.get(id=event_id)
        form = forms.PostEventForm(instance=event)
    else:
        form = forms.PostEventForm()

    return render_to_response('post-event.html', {
    'edit': edit,
    'form': form,
    }, context_instance=RequestContext(request))

@login_required
def edit_event(request, event_id):
    return post_event(request, event_id=event_id, edit=True)

@login_required
def show_events(request):
    events = models.Event.objects.filter(user_id=request.user.id).exclude(status=0).order_by('start_date', 'start_time', 'end_date', 'end_time').reverse()

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

#class EventSearchView(BackboneAPIView):
#    base_queryset = models.Event.objects.filter(status=1).extra(where=['end_date >= CURRENT_TIMESTAMP']).order_by('start_date','start_time').reverse()
#    
#    edit_form_class = forms.ArchiveEventForm
#    
#    serialize_fields = ['id', 'user_id', 'address', 'subpremise',
#    'city', 'state', 'zipcode', 'name', 'category', 'ticket_price', 'start_date', 
#    'start_time', 'end_date', 'end_time', 'description', 'organizer_email', 
#    'organizer_phone', 'organizer_url', 'latitude', 'longitude', 'status']
#    
#    def dispatch(self, request, *args, **kwargs):
#        if request.GET.has_key('userId'):
#            self.base_queryset = models.Event.objects.filter(user_id=request.GET['userId']).exclude(status=0)
#        elif request.GET.has_key('category'):
#            self.base_queryset = models.Event.objects.filter(user_id=request.GET['category']).exclude(status=0)
#        else:
#            form = forms.EventSearchForm(request.GET)
#            if form.is_valid():
#                events = form.search()
#        
#        return super(EventSearchView, self).dispatch(request, *args, **kwargs)
#    
#    def validation_error_response(self, form_errors):
#        logging.debug(form_errors)
#        return str(form_errors)
