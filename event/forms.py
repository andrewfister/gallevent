import re
import datetime

from django import forms
from django.forms.util import ErrorList

from gallevent.event import models


class PostEventForm(forms.Form):
    address1 = forms.CharField(max_length=255, initial="")
    address2 = forms.CharField(max_length=64, initial="", required=False)
    city = forms.CharField(max_length=64, initial="")
    zipcode = forms.CharField(max_length=16, initial="")
    event_category = forms.CharField(max_length=64, initial="")
    event_keywords = forms.CharField(max_length=255, initial="", required=False)
    start_date = forms.DateField(initial="")
    start_time = forms.TimeField(initial="")
    end_date = forms.DateField(initial="")
    end_time = forms.TimeField(initial="")
    event_name = forms.CharField(max_length=64, initial="")
    event_description = forms.CharField(max_length=1000, initial="")
    event_url = forms.URLField(required=False, initial="")
    rsvp_limit = forms.IntegerField(required=False, initial="")
    purchase_tickets = forms.BooleanField(initial=False, required=False)
    ticket_price = forms.DecimalField(required=False, decimal_places=2, initial="")
    ticket_url = forms.URLField(required=False, initial="")
    latitude = forms.FloatField()
    longitude = forms.FloatField()
    
    def clean_purchase_tickets(self):
        return self.cleaned_data['purchase_tickets'] == "yes"
    
    def clean_ticket_price(self):
        return self.cleaned_data['ticket_price'] or 0
    
    def clean_rsvp_limit(self):
        return self.cleaned_data['rsvp_limit'] or 0
    
    def save(self, commit=True):
        address1 = self.cleaned_data['address1']
        address2 = self.cleaned_data['address2']
        city = self.cleaned_data['city']
        zipcode = self.cleaned_data['zipcode']
        event_category = self.cleaned_data['event_category']
        event_keywords = self.cleaned_data['event_keywords']
        start_date = self.cleaned_data['start_date']
        start_time = self.cleaned_data['start_time']
        end_date = self.cleaned_data['end_date']
        end_time = self.cleaned_data['end_time']
        event_name = self.cleaned_data['event_name']
        event_description = self.cleaned_data['event_description']
        event_url = self.cleaned_data['event_url']
        rsvp_limit = self.cleaned_data['rsvp_limit']
        purchase_tickets = self.cleaned_data['purchase_tickets']
        ticket_price = self.cleaned_data['ticket_price']
        ticket_url = self.cleaned_data['ticket_url']
        latitude = self.cleaned_data['latitude']
        longitude = self.cleaned_data['longitude']
        
        #Need to combine these fields for realsies
        start_datetime = datetime.datetime.combine(start_date, start_time)
        end_datetime = datetime.datetime.combine(end_date, end_time)
        
        
        event = models.Event(address1=address1, address2=address2, city=city, 
                            zipcode=zipcode, category=event_category, 
                            keywords=event_keywords, start_date=start_datetime, 
                            end_date=end_datetime, name=event_name, 
                            description=event_description, event_url=event_url, 
                            rsvp_limit=rsvp_limit, 
                            purchase_tickets=purchase_tickets,
                            ticket_price=ticket_price, ticket_url=ticket_url,
                            latitude=latitude, longitude=longitude,
                            user_id=self.request.user.id)
        event.save()
        
        return event
        
    def set_request(self, request):
        self.request = request
