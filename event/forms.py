import re
import datetime

from django import forms
from django.forms.util import ErrorList
from haystack.utils.geo import Point, D

from haystack.forms import SearchForm

from gallevent.event import models


class PostEventForm(forms.ModelForm):
    class Meta:
        model = models.Event
        exclude = ('status','user_id',)
    
    date_input_formats = [
        '%m/%d/%Y',       # '10/25/2006'
        '%b %d, %Y',      # 'Oct 25, 2006'
        '%Y-%m-%d',       # '2006-10-25'
        '%m/%d/%y',       # '10/25/06'
        '%b %m %d',       # 'Oct 25 2006'
        '%d %b %Y',       # '25 Oct 2006'
        '%d %b, %Y',      # '25 Oct, 2006'
        '%B %d %Y',       # 'October 25 2006'
        '%B %d, %Y',      # 'October 25, 2006'
        '%d %B %Y',       # '25 October 2006'
        '%d %B, %Y',      # '25 October, 2006'
    ]
    
    address = forms.CharField(max_length=1000)
    street_number = forms.CharField(max_length=64)
    street = forms.CharField(max_length=255)
    subpremise = forms.CharField(max_length=64, initial="")
    city = forms.CharField(max_length=64, initial="")
    state = forms.CharField(max_length=2, initial="") 
    zipcode = forms.CharField(max_length=16, initial="")
    category = forms.CharField(max_length=64, initial="")
    keywords = forms.CharField(max_length=255, required=False, initial="")
    start_date = forms.DateField(initial="", input_formats=date_input_formats)
    start_time = forms.TimeField(initial="", input_formats=['%I:%M%p', '%I:%M %p'])
    end_date = forms.DateField(initial="", input_formats=date_input_formats)
    end_time = forms.TimeField(initial="", input_formats=['%I:%M%p', '%I:%M %p', '%I%p', '%I %p'])
    name = forms.CharField(max_length=64, initial="")
    description = forms.CharField(max_length=1000, initial="")
    event_url = forms.URLField(required=False, initial="")
    rsvp_limit = forms.IntegerField(required=False, initial="")
    rsvp_end_date = forms.DateField(required=False, initial="", input_formats=date_input_formats)
    rsvp_end_time = forms.TimeField(required=False, initial="", input_formats=['%I:%M%p', '%I:%M %p', '%I%p', '%I %p'])
    organizer_email = forms.CharField(max_length=64, required=False, initial="")
    organizer_phone = forms.CharField(max_length=24, required=False, initial="")
    organizer_url = forms.URLField(max_length=200, required=False, initial="")
    purchase_tickets = forms.BooleanField(initial=False, required=False)
    ticket_type = forms.CharField(max_length=32, required=False, initial="")
    ticket_price = forms.DecimalField(required=False, decimal_places=2, initial="")
    ticket_url = forms.URLField(required=False, initial="")
    
    def clean_purchase_tickets(self):
        return self.cleaned_data['purchase_tickets'] == "yes"
    
    def clean_ticket_price(self):
        return self.cleaned_data['ticket_price'] or 0
    
    def clean_rsvp_limit(self):
        return self.cleaned_data['rsvp_limit'] or 0

class ArchiveEventForm(forms.ModelForm):
    class Meta:
        model = models.Event

    def set_request(self, request):
        self.request = request

class EventSearchForm(SearchForm):
    date_input_formats = [
        '%m/%d/%Y',       # '10/25/2006'
        '%b %d, %Y',      # 'Oct 25, 2006'
        '%Y-%m-%d',       # '2006-10-25'
        '%m/%d/%y',       # '10/25/06'
        '%b %m %d',       # 'Oct 25 2006'
        '%d %b %Y',       # '25 Oct 2006'
        '%d %b, %Y',      # '25 Oct, 2006'
        '%B %d %Y',       # 'October 25 2006'
        '%B %d, %Y',      # 'October 25, 2006'
        '%d %B %Y',       # '25 October 2006'
        '%d %B, %Y',      # '25 October, 2006'
    ]

    start_date = forms.DateField(required=False, initial="", input_formats=date_input_formats)
    end_date = forms.DateField(required=False, initial="", input_formats=date_input_formats)
    latitude = forms.FloatField(initial=37.774929)
    longitude = forms.FloatField(initial=-122.2644)
    distance = forms.FloatField(initial=5.08)
    
    def search(self):
        sqs = super(EventSearchForm, self).search()
        
        # First, store the SearchQuerySet received from other processing.
        import logging
        logging.debug('sqs: ' + str(sqs.all()))

        if self.cleaned_data['longitude'] and self.cleaned_data['latitude'] and self.cleaned_data['distance']:
            map_center = Point(self.cleaned_data['longitude'], self.cleaned_data['latitude'])
            distance = D(mi=self.cleaned_data['distance'])
            sqs = sqs.dwithin('location', map_center, distance)

        # Check to see if a start_date was chosen.
        if self.cleaned_data['start_date']:
            sqs = sqs.filter(end_date__gte=self.cleaned_data['start_date'])

        # Check to see if an end_date was chosen.
        if self.cleaned_data['end_date']:
            sqs = sqs.filter(start_date__lte=self.cleaned_data['end_date'])

        return sqs
