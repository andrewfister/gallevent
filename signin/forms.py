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
    invite_code = forms.CharField(required=False, max_length=64)
    password = forms.CharField(max_length=32)
    confirm_password = forms.CharField(required=False, max_length=32)
    
    def clean_email(self):
        email = self.cleaned_data['email']

        if len(User.objects.filter(username=email)) > 0:
            raise forms.ValidationError('This email address is already registered!')

        return email
    
    def clean_invite_code(self):
        invite_code = self.cleaned_data['invite_code']
        query_email = self.cleaned_data['email']
        
        try:
            invite_request = models.InvitationManager.objects.get(email=query_email)
        except (models.InvitationManager.DoesNotExist, models.InvitationManager.MultipleObjectsReturned):
            raise forms.ValidationError('This email address did not receive an invitation yet.')
        
        if invite_request.code != invite_code:
            raise forms.ValidationError('This invitation code does not match for this email address.')
        
        return invite_code
    
    def clean_password(self):
        password = self.cleaned_data['password']
        
        if len(password) < 7:
            raise forms.ValidationError('This password is too short')
        elif len(password) > 32:
            raise forms.ValidationError('This password is too long')
        
        return password
        
    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        
        if password != confirm_password:
            raise forms.ValidationError('The passwords do not match')
        
        return confirm_password
    
    def save(self, commit=True):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        
        user = User.objects.create_user(email, email, password)
        user.save()
        
    
class SignInForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=32)
