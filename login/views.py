from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

from gallevent.login import forms
from gallevent.login import models

def invite_code(request):
    return render_to_response('invite-code.html')
    
def invite_request(request):
    if request.method == 'POST': # If the form has been submitted...
        form = forms.RequestInviteForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            new_email_address = form.cleaned_data['email']
            
            if len(models.InvitationManager.objects.filter(email=new_email_address)) == 0:
                invite_data = models.InvitationManager(email=new_email_address)
                invite_data.save()
            
            from django.core.mail import send_mail
            send_mail('Thank you for your interest in Gallevent', 
                        'Your invite is on the way!', 
                        'gallevent.main@gmail.com', 
                        [new_email_address])
            
            return HttpResponseRedirect('/login/invite_request_received/') # Redirect after POST
    else:
        form = forms.RequestInviteForm() # An unbound form

    return render_to_response('invite-request.html', {
        'form': form,
    })

def invite_request_received(request):
    return render_to_response('invite-request-received.html')
    
def sign_in(request):
    return render_to_response('sign-in.html')

def manage_invites(request):
    invite_requests = models.InvitationManager.objects.all()
    email_choices = [invite_request.email for invite_request in invite_requests]
    dates = [invite_request.date for invite_request in invite_requests]
    

    if request.method == 'POST':
        form = forms.InviteEmailsForm(email_choices)
        if form.is_valid():
            emails_chosen = form.cleaned_data['emails']
    else:
        form = forms.InviteEmailsForm(email_choices)
    
    return render_to_response('control/manage-invites.html', {
        'form': form,
        'invite_requests': zip(email_choices, dates),
    })
