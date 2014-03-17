import logging

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import FormView

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


class PostEventView(FormView):
    template_name = "post-event.html"
    form_class = forms.PostEventForm
    success_url = '/'
 
    def form_valid(self, form):
        print("Post event form GOOD!")
        form.save()

        return super(PostEventView, self).form_valid(form)

    def form_invalid(self, form):
        logger.debug(form.errors)
        print(form.errors)

        return super(PostEventView, self).form_invalid(form)


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

