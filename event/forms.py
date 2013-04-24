import logging
import calendar
from datetime import datetime

import eventbrite
from meetup_api_client import meetup_api_client
from lxml import html
from lxml.html.soupparser import fromstring

from django import forms

from haystack.utils.geo import Point, D
from haystack.forms import SearchForm

from event import models
from gallevent import settings


class PostEventForm(forms.ModelForm):
    class Meta:
        model = models.Event
        exclude = ('status', 'user_id')
    
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
    
    time_input_formats = [
        '%I:%M%p', 
        '%I:%M %p', 
        '%I%p', 
        '%I %p'
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
    start_time = forms.TimeField(initial="", input_formats=time_input_formats)
    end_date = forms.DateField(initial="", input_formats=date_input_formats)
    end_time = forms.TimeField(initial="", input_formats=time_input_formats)
    name = forms.CharField(max_length=64, initial="")
    description = forms.CharField(max_length=1000, initial="")
    event_url = forms.URLField(required=False, initial="")
    rsvp_limit = forms.IntegerField(required=False, initial="")
    rsvp_end_date = forms.DateField(required=False, initial="", input_formats=date_input_formats)
    rsvp_end_time = forms.TimeField(required=False, initial="", input_formats=time_input_formats)
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

    start_date = forms.DateTimeField(required=False, initial="", input_formats=date_input_formats)
    end_date = forms.DateTimeField(required=False, initial="", input_formats=date_input_formats)
    latitude = forms.FloatField(initial=0)
    longitude = forms.FloatField(initial=0)
    distance = forms.FloatField(initial=5.08)
    
    #TODO: Next time I add another source, modularize each event source
    #Current search sources:
    #Gallevent
    #EventBrite
    def search(self):
        sqs = super(EventSearchForm, self).search()
        eb_client_query = {'keywords': self.cleaned_data['q']}
        
        # First, store the SearchQuerySet received from other processing.
        logging.debug('sqs: ' + str(sqs.all()))

        if self.cleaned_data['longitude'] and self.cleaned_data['latitude'] and self.cleaned_data['distance']:
            map_center = Point(self.cleaned_data['longitude'], self.cleaned_data['latitude'])
            distance = D(mi=self.cleaned_data['distance'])
            sqs = sqs.dwithin('location', map_center, distance)
            eb_client_query['latitude'] = self.cleaned_data['latitude']
            eb_client_query['longitude'] = self.cleaned_data['longitude']
            eb_client_query['within'] = int(self.cleaned_data['distance'])
            logging.debug('within: ' + str(eb_client_query['within']))

        # Check to see if a start_date was chosen.
        if self.cleaned_data['start_date']:
            sqs = sqs.filter(end_date__gte=self.cleaned_data['start_date'])
            logging.debug('raw start date: ' + str(self.cleaned_data['start_date']))
            eb_client_query['date'] = str(self.cleaned_data['start_date'])
            logging.debug('parsed start date: ' + eb_client_query['date'])

        # Check to see if an end_date was chosen.
        if self.cleaned_data['end_date']:
            sqs = sqs.filter(start_date__lte=self.cleaned_data['end_date'])
            eb_client_query['date'] += ' ' + str(self.cleaned_data['end_date'])
        
        # Get a list of Event objects so we can append these results with other sources
        events = [result.object for result in sqs]

        if sqs.count() < settings.MAX_EVENTS:
            try:
                eb_events = self.searchEventBrite(eb_client_query, settings.MAX_EVENTS - sqs.count())
                events.extend(eb_events)
            except EnvironmentError:
                pass

        return events


#Search EventBrite with their API
class EventBriteSearchForm(EventSearchForm):
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
        logging.debug('searching eventbrite')
        eb_client_query = {'keywords': self.cleaned_data['q']}

        if self.cleaned_data['longitude'] and \
            self.cleaned_data['latitude'] and \
            self.cleaned_data['distance']:
            eb_client_query['latitude'] = self.cleaned_data['latitude']
            eb_client_query['longitude'] = self.cleaned_data['longitude']
            eb_client_query['within'] = int(self.cleaned_data['distance'])
            logging.debug('within: ' + str(eb_client_query['within']))

        # Check to see if a start_date was chosen.
        if self.cleaned_data['start_date']:
            logging.debug('raw start date: ' + str(self.cleaned_data['start_date']))
            eb_client_query['date'] = str(self.cleaned_data['start_date'])
            logging.debug('parsed start date: ' + eb_client_query['date'])

        # Check to see if an end_date was chosen.
        if self.cleaned_data['end_date']:
            eb_client_query['date'] += ' ' + str(self.cleaned_data['end_date'])
        
        try:
            events = self.searchEventBrite(eb_client_query, settings.MAX_EVENTS)
        except EnvironmentError:
            events = []

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
            
            try:
                eb_event_venue = eb_event['venue']
            except KeyError:
                continue
            
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
            eb_event_end_date = eb_event_end[0]
            eb_event_end_time = eb_event_end[1]
            eb_event_categories = eb_event['category'].split(',')
            logging.debug('trying to get description')
            eb_event_description = fromstring(eb_event['description']).text_content()
            eb_event_short_description = eb_event_description[:50] + '...'
            try:
                eb_event_title = html.fragment_fromstring(eb_event['title']).text_content()
            except:
                eb_event_title = eb_event['title']
            
            try:
                eb_event_ticket_price = eb_event['tickets'][0]['ticket']['price'].replace(',','')
            except KeyError:
                eb_event_ticket_price = 0.00
                
            eb_events.append({
                            "id": eb_event['id'],
                            "user_id": eb_event['organizer']['id'],
                            "name": eb_event_title,
                            "address": eb_event_address,
                            "street": eb_event_venue['address'],
                            "subpremise": eb_event_venue['address_2'],
                            "city": eb_event_venue['city'],
                            "state": eb_event_venue['region'],
                            "zipcode": eb_event_venue['postal_code'],
                            "latitude": eb_event_venue['latitude'],
                            "longitude": eb_event_venue['longitude'],
                            "keywords": eb_event['tags'],
                            "category": self.get_category_from_eb(eb_event_categories[0]),
                            "short_description": eb_event_short_description,
                            "description": eb_event_description,
                            "event_url": eb_event['url'],
                            "start_date": eb_event_start_date,
                            "start_time": eb_event_start_time,
                            "end_date": eb_event_end_date,
                            "end_time": eb_event_end_time,
                            "ticket_price": eb_event_ticket_price,
                            })
       
        return eb_events
        
    def get_category_from_eb(self, category):
        if category in self.gallevent_categories:
            return category
            
        try:
            return self.eb_category_map[category]
        except KeyError:
            return 'networking'


#Search Meetup with their non-existant python integration
class MeetupSearchForm(EventSearchForm):
    def search(self):
        meetup_client_query = {'text': self.cleaned_data['q']}
        logging.debug('searching meetup' + str(self.cleaned_data))
        
        meetup_client_query['lat'] = self.cleaned_data['latitude']
        meetup_client_query['lon'] = self.cleaned_data['longitude']
        meetup_client_query['radius'] = int(self.cleaned_data['distance'])
        logging.debug('within: ' + str(meetup_client_query['radius']))

        logging.debug('searching meetup')
        logging.debug('meetup search query: ' + str(meetup_client_query))

        # Check to see if a start_date was chosen.
        if self.cleaned_data.has_key('start_date'):
            logging.debug('raw start date: ' + str(self.cleaned_data['start_date']))
            meetup_client_query['time'] = str(calendar.timegm(self.cleaned_data['start_date'].utctimetuple()) * 1000)
            logging.debug('parsed start date: ' + meetup_client_query['time'])

        if self.cleaned_data.has_key('start_date') or self.cleaned_data.has_key('end_date'):
            meetup_client_query['time'] += ','

        # Check to see if an end_date was chosen.
        if self.cleaned_data.has_key('end_date'):
            meetup_client_query['time'] += str(calendar.timegm(self.cleaned_data['end_date'].utctimetuple()) * 1000)
        
        meetup_client_query['text_format'] = 'plain'
        
        try:
            logging.debug('try to call meetup')
            events = self.searchMeetup(meetup_client_query, settings.MAX_EVENTS)
        except EnvironmentError:
            events = []

        return events
    
    def searchMeetup(self, meetup_client_query, max_events):
        logging.debug('inside search meetup: ' + str(meetup_client_query))
        meetup_client = meetup_api_client.Meetup(api_key='237e2a627822653b453365385e652f67')
        
        logging.debug('right before meetup call: ' + str(meetup_client))
        meetup_response = meetup_client.get_open_events(**meetup_client_query)
        logging.debug('meetup search response: ' + str(meetup_response))
        meetup_events = []
        
        for meetup_event in meetup_response.results:
            logging.debug('an event response: ' + str(meetup_event))
            meetup_event_description = meetup_event.description
            meetup_event_short_description = meetup_event_description[:50] + '...'
            try:
                meetup_event_group = meetup_event.group
                meetup_event_venue = meetup_event.venue
            except AttributeError:
                continue
            
            logging.debug('venue: ' + str(meetup_event_venue))
            if not meetup_event_venue.has_key('address_2'):
                meetup_event_venue['address_2'] = ''
            if not meetup_event_venue.has_key('zip'):
                meetup_event_venue['zip'] = ''
            
            meetup_event_address_parts = [meetup_event_venue['address_1'], 
                                    meetup_event_venue['address_2'], 
                                    meetup_event_venue['city'], 
                                    meetup_event_venue['state'], 
                                    meetup_event_venue['zip']]
            meetup_event_address_parts = [value for value in meetup_event_address_parts if value != '']
            meetup_event_address = ', '.join(meetup_event_address_parts)
            meetup_event_start = datetime.fromtimestamp(int(meetup_event.time)/1000)
            
            try:
                duration = meetup_event.duration
            except AttributeError:
                duration = 86400000
            
            meetup_event_end = datetime.fromtimestamp(int(meetup_event.time + duration)/1000)
            
            try:
                meetup_event_fee = meetup_event.fee['amount']
            except AttributeError:
                meetup_event_fee = 0
            
            meetup_event_start_date = meetup_event_start.strftime("%m/%d/%Y")
            meetup_event_start_time = meetup_event_start.strftime("%I:%M%p")
            meetup_event_end_date = meetup_event_end.strftime("%m/%d/%Y")
            meetup_event_end_time = meetup_event_end.strftime("%I:%M%p")
            
            
            
            meetup_events.append({
                            "id": meetup_event.id,
                            #"user_id": meetup_event.event_hosts[0]['id'],
                            "name": meetup_event.name,
                            "address": meetup_event_address,
                            "street": meetup_event_venue['address_1'],
                            "subpremise": meetup_event_venue['address_2'],
                            "city": meetup_event_venue['city'],
                            "state": meetup_event_venue['state'],
                            "zipcode": meetup_event_venue['zip'],
                            "latitude": meetup_event_venue['lat'],
                            "longitude": meetup_event_venue['lon'],
                            #"keywords": meetup_event_group['topics'],
                            #"category": meetup_event_group['category'],
                            "short_description": meetup_event_short_description,
                            "description": meetup_event_description,
                            "event_url": meetup_event.event_url,
                            "start_date": meetup_event_start_date,
                            "start_time": meetup_event_start_time,
                            "end_date": meetup_event_end_date,
                            "end_time": meetup_event_end_time,
                            "ticket_price": meetup_event_fee,
                            })
        
        return meetup_events
