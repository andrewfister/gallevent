from django import forms

from models import UserProfile

class UserProfileBioForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['fname', 'lname', 'city', 'state', 'bio', 'twitter', 'facebook', 'website']
