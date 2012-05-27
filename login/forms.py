import re

from django import forms
from django.contrib.auth.models import User

from gallevent.login import models


class RequestInviteForm(forms.Form):
    email = forms.CharField(max_length=64)

    def clean_email(self):
        email = self.cleaned_data['email']

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

        if re.match(email_re, email) == None:
            raise forms.ValidationError('Invalid Email Address')
        
        if len(User.objects.filter(username=email)) > 0:
            raise forms.ValidationError('This email address is already registered!')

        return email
    
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
    


class RegistrationForm(forms.Form):
    email = forms.CharField(max_length=64)
    invite_code = forms.CharField(max_length=64)
    password = forms.CharField(max_length=32)
    confirm_password = forms.CharField(max_length=32)
    
    def clean_email(self):
        email = self.cleaned_data['email']

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

        if re.match(email_re, email) == None:
            raise forms.ValidationError('Invalid Email Address')
        
        if len(User.objects.filter(username=email)) > 0:
            raise forms.ValidationError('This email address is already registered!')

        return email
    
    def clean_invite_code(self):
        invite_code = self.cleaned_data['invite_code']
        query_email = self.cleaned_data['email']
        
        try:
            invite_request = models.InvitationManager.objects.get(email=query_email)
        except DoesNotExist:
            raise ValidationError('This email address did not receive an invitation yet.')
        
        if invite_request['invite_code'] != invite_code:
            raise ValidationError('This invitation code does not match for this email address.')
        
        return invite_code
    
    def clean_password(self):
        password = self.cleaned_data['password']
        
        if len(password) < 7:
            raise ValidationError('This password is too short')
        elif len(password) > 32:
            raise ValidationError('This password is too long')
        
        return password
    
    def save(self, commit=True):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        
        User.objects.create_user(email, email, password)
