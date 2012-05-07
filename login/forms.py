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
            
        if len(models.InvitationManager.objects.filter(email=new_email_address)) == 0:
            invite_data = models.InvitationManager(email=new_email_address)
            invite_data.save()
    
#This kind of form is a bitch to get working :-(
#And no, this is not working code   
class InviteEmailsForm(forms.Form):
    emails = forms.MultipleChoiceField()
    
    def __init__(self, email_choices, *args, **kwargs):
        super(InviteEmailsForm, self).__init__(*args, **kwargs)
        
        self.fields['emails'].choices = [(str(i), email) for i, email in enumerate(email_choices)]
        
    
    def clean_emails(self):
        cleaned_emails = self.cleaned_data['emails']
        
        if (len(cleaned_emails) == 0):
            raise forms.ValidationError('Must Select At Least One Email Address')
        
    def save(self, commit=True):
        pass
