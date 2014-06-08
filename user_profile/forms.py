from django import forms

from models import UserProfile

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


class UserProfileEducationForm(forms.ModelForm):
    class Meta:
        model = UserProfile


class UserProfileWorkForm(forms.ModelForm):
    class Meta:
        model = UserProfile
