import re

from django import forms
from django.contrib.auth.models import User
from django.core.validators import validate_email

from signin import models


class SignInForm(forms.Form):
    email = forms.EmailField()
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
    
    def create_user(self, commit=True):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        
        user = User.objects.create_user(email, email, password)
        user.save()

