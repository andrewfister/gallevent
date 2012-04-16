from django import forms

class InviteForm(forms.Form):
     email = forms.CharField(max_length=64)
