import re

from django import forms
from django.forms.widgets import CheckboxSelectMultiple

from gallevent.login import models

class RequestInviteForm(forms.Form):
    email = forms.CharField(max_length=64)

    def clean_email(self):
        cleaned_data = self.cleaned_data['email']

        ADDR_SPEC = (
            "((?:"
                r"[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(?:\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*" # dot-atom
            ")|(?:"
                r'"(?:[\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-011\013\014\016-\177])*"' # quoted-string
            "))@("
            r'(?:[A-Z0-9-]+\.)+[A-Z]{2,6}'   #domain
            ")"
        )

        email_re = re.compile(
            "^(?:" + ADDR_SPEC + ")|(?:\w[\w ]*)<" + ADDR_SPEC + ">$", re.IGNORECASE)

        if re.match(email_re, cleaned_data) == None:
            raise forms.ValidationError('Invalid Email Address')

        return cleaned_data
    
    def save(self, commit=True):
        new_email_address = self.cleaned_data['email']
        new_email_address_search = models.InvitationManager.objects.filter(email=new_email_address)
        
        if len(new_email_address_search) == 0:
            invite_data = models.InvitationManager(email=new_email_address)
            invite_data.save()
        else:
            invite_data = new_email_address_search[0]
            invite_data.code = ''
            invite_data.save()
            
