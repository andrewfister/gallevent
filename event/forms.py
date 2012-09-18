import re
import datetime

from django import forms
from django.forms.util import ErrorList

from gallevent.event import models


class PostEventForm(forms.ModelForm):
    class Meta:
        model = models.Event
        exclude = ('status',)

    start_time = forms.TimeField(initial="", input_formats=['%I:%M%p', '%I:%M %p'])
    end_time = forms.TimeField(initial="", input_formats=['%I:%M%p', '%I:%M %p', '%I%p', '%I %p'])
    rsvp_limit = forms.IntegerField(initial=0, required=False)
    
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
