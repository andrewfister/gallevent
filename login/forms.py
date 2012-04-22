import re

from django import forms

class InviteForm(forms.Form):
     email = forms.CharField(max_length=64)
     
     def clean_email(self):
        cleaned_data = self.cleaned_data['email']
        
        if re.match('\w+@\w+\.\w+', cleaned_data) == None:
            raise forms.ValidationError('Invalid Email Address')
        
        return cleaned_data
