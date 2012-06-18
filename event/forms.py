import re
import datetime

from django import forms

from gallevent.event import models


class PostEventForm(forms.Form):
    address1 = forms.CharField(max_length=255)
    address2 = forms.CharField(max_length=64)
    city = forms.CharField(max_length=64)
    zipcode = forms.CharField(max_length=16)
    event_category = forms.CharField(max_length=64)
    event_keywords = forms.CharField(max_length=255)
    start_date = forms.DateField()
    start_time = forms.TimeField()
    end_date = forms.DateField()
    end_time = forms.TimeField()
    event_name = forms.CharField(max_length=64)
    event_description = forms.CharField(max_length=255)
    event_url = forms.URLField()
    rsvp_limit = forms.IntegerField()
    purchase_tickets = forms.BooleanField()
    ticket_price = forms.DecimalField(decimal_places=2)
    ticket_url = forms.URLField()
    
    def save(self, user, commit=True):
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
                            user_id=user.id)
        event.save()
        