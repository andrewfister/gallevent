import re
import datetime

from django import forms
from django.forms.util import ErrorList

from gallevent.event import models


class PostEventForm(forms.ModelForm):
    class Meta:
        model = models.Event
        exclude = ('status','user_id',)
    
    address1 = forms.CharField(max_length=255, initial="")
    address2 = forms.CharField(max_length=64, required=False, initial="")
    city = forms.CharField(max_length=64, initial="")
    state = forms.CharField(max_length=2, initial="") 
    zipcode = forms.CharField(max_length=16, initial="")
    category = forms.CharField(max_length=64, initial="")
    keywords = forms.CharField(max_length=255, required=False, initial="")
    start_date = forms.DateField(initial="")
    start_time = forms.TimeField(initial="", input_formats=['%I:%M%p', '%I:%M %p'])
    end_date = forms.DateField(initial="")
    end_time = forms.TimeField(initial="", input_formats=['%I:%M%p', '%I:%M %p', '%I%p', '%I %p'])
    name = forms.CharField(max_length=64, initial="")
    description = forms.CharField(max_length=1000, initial="")
    event_url = forms.URLField(required=False, initial="")
    rsvp_limit = forms.IntegerField(required=False, initial=0)
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
