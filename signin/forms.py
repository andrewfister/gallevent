import re

from django import forms
from django.contrib.auth.models import User
from django.core.validators import validate_email

from signin import models


class RequestInviteForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data['email']
        
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
    password = forms.CharField(max_length=32)
    
    def clean_email(self):
        email = self.cleaned_data['email']

        if len(User.objects.filter(username=email)) > 0:
            raise forms.ValidationError('This email address is already registered!')

        return email
    
    def clean_password(self):
        password = self.cleaned_data['password']
        
        if len(password) < 7:
            raise forms.ValidationError('This password is too short')
        elif len(password) > 32:
            raise forms.ValidationError('This password is too long')
        
        return password
    
    def save(self, commit=True):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        
        user = User.objects.create_user(email, email, password)
        user.save()
        
    
class SignInForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=32)
