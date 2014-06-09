import logging

from django import forms

from models import UserProfile

logger = logging.getLogger("gallevent")

class UserProfileBioForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['fname', 'lname', 'city', 'state', 'bio', 'twitter', 'facebook', 'website']


class UserProfileBasicInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['gender', 'interests', 'relationship']


class UserProfileContactForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['email', 'phone']


class UserProfileEducationForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['school', 'study_field']


class UserProfileWorkForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['job_title', 'company']
