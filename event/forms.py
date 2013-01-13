import re
import datetime
import logging
import cgi

import eventbrite

from django import forms
from django.forms.util import ErrorList

from haystack.utils.geo import Point, D
from haystack.forms import SearchForm

from gallevent.event import models
from gallevent import settings


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
    
    eb_category_map = {
        'seminars': 'education',
        'social': 'parties',
        'entertainment': 'fairs',
        'music': 'art',
        'sports': 'athletic',
    }
    
    gallevent_categories = ['art', 'athletic', 'dancing', 'dining', 'education', 
                            'fairs', 'jobs', 'networking', 'parties', 'sales']
    
    def search(self):
        sqs = super(EventSearchForm, self).search()
        eb_client_query = {}
        
        # First, store the SearchQuerySet received from other processing.
        logging.debug('sqs: ' + str(sqs.all()))

        if self.cleaned_data['longitude'] and self.cleaned_data['latitude'] and self.cleaned_data['distance']:
            map_center = Point(self.cleaned_data['longitude'], self.cleaned_data['latitude'])
            distance = D(mi=self.cleaned_data['distance'])
            sqs = sqs.dwithin('location', map_center, distance)
            eb_client_query['latitude'] = self.cleaned_data['latitude']
            eb_client_query['longitude'] = self.cleaned_data['longitude']
            eb_client_query['within'] = int(self.cleaned_data['distance'])

        # Check to see if a start_date was chosen.
        if self.cleaned_data['start_date']:
            sqs = sqs.filter(end_date__gte=self.cleaned_data['start_date'])

        # Check to see if an end_date was chosen.
        if self.cleaned_data['end_date']:
            sqs = sqs.filter(start_date__lte=self.cleaned_data['end_date'])
        
        # Get a list of Event objects so we can append these results with other sources
        events = [ result.object for result in sqs ]

        if sqs.count() < settings.MAX_EVENTS:
            eb_events = self.searchEventBrite(eb_client_query, settings.MAX_EVENTS - sqs.count())
            events.extend(eb_events)

        return events


    def searchEventBrite(self, eb_client_query, max_events):
        eb_auth_tokens = {'app_key': 'K4FQTKYHI34GPW6HSS'}
        eb_client = eventbrite.EventbriteClient(eb_auth_tokens)
        
        #Only get as many events as we need from EventBrite
        eb_client_query['max'] = max_events
        eb_response = eb_client.event_search(eb_client_query)
        logging.debug('eb response: ' + str(eb_response['events'][1]))
        eb_events = []
        
        for eb_event in eb_response['events'][1:]:
            eb_event = eb_event['event']
            eb_event_venue = eb_event['venue']
            logging.debug('eb event address: ' + eb_event_venue['address'])
            if len(eb_event_venue['address']) == 0 or eb_event_venue['address'] == 'TBA' or eb_event['category'] == 'sales':
                continue
            
            eb_event_address_parts = [eb_event_venue['address'], 
                                    eb_event_venue['address_2'], 
                                    eb_event_venue['city'], 
                                    eb_event_venue['region'], 
                                    eb_event_venue['postal_code']]
            eb_event_address_parts = [value for value in eb_event_address_parts if value != '']
            eb_event_address = ', '.join(eb_event_address_parts)
            eb_event_start = eb_event['start_date'].split()
            eb_event_start_date = eb_event_start[0]
            eb_event_start_time = eb_event_start[1]
            eb_event_end = eb_event['end_date'].split()
            eb_event_end_date = eb_event_start[0]
            eb_event_end_time = eb_event_start[1]
            eb_event_categories = eb_event['category'].split(',')
            
            try:
                eb_event_ticket_price = eb_event['tickets'][0]['ticket']['price'].replace(',','')
            except KeyError:
                eb_event_ticket_price = 0.00
                
            eb_events.append(models.Event(
                            id=eb_event['id'],
                            user_id=eb_event['organizer']['id'],
                            name=eb_event['title'],                
                            address=eb_event_address,
                            street=eb_event_venue['address'],
                            subpremise=eb_event_venue['address_2'],
                            city=eb_event_venue['city'],
                            state=eb_event_venue['region'],
                            zipcode=eb_event_venue['postal_code'],
                            latitude=eb_event_venue['latitude'],
                            longitude=eb_event_venue['longitude'],
                            keywords=eb_event['tags'],
                            category=self.get_category_from_eb(eb_event_categories[0]),
                            description='description',#cgi.escape(eb_event['description'], True),
                            event_url=eb_event['url'],
                            start_date=eb_event_start_date,
                            start_time=eb_event_start_time,
                            end_date=eb_event_end_date,
                            end_time=eb_event_end_time,
                            ticket_price=eb_event_ticket_price,
                            ))
       
        return eb_events
        
    
    def get_category_from_eb(self, category):
        if category in self.gallevent_categories:
            return category
            
        try:
            return self.eb_category_map[category]
        except KeyError:
            return 'networking'
