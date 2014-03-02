import logging

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView, View

from event import forms
from event import models
from gallevent import settings

logger = logging.getLogger('gallevent')

class FrontPageView(TemplateView):
    template_name = "index.html"
    
    def get(self, request):
        try:
            timeSpan = request.GET['timeSpan']
        except KeyError:
            timeSpan = "day_of"

        return self.render_to_response({
            'timeSpan': timeSpan
            })


class SearchView(View):
    searchForms = [forms.EventSearchForm, forms.EventBriteSearchForm, forms.MeetupSearchForm]

    def get(self, request):        
        events = []

        for SearchForm in self.searchForms:
            if len(events) >= settings.MIN_EVENTS:
                break
            
            form = SearchForm(request.GET)
            if form.is_valid():
                events.extend(form.search(settings.MAX_EVENTS - len(events)))
        
        if len(events) == 0:
            events_json = "[]"
        
        eventJSONSerializer = models.EventJSONSerializer()
        events_json = eventJSONSerializer.serialize(events)

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
            logger.debug(form.errors)
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

