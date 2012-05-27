from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User

from gallevent.login import forms
from gallevent.login import models

def invite_code(request):
    if request.method == 'POST':
        form = forms.RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
    
    return render_to_response('invite-code.html')
    
def invite_request(request):
    if request.method == 'POST': # If the form has been submitted...
        form = forms.RequestInviteForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            form.save()
            
            # Process the data in form.cleaned_data
            new_email_address = form.cleaned_data['email']
            
            from django.core.mail import send_mail
            send_mail('Thank you for your interest in Gallevent', 
                        'Your invite is on the way!', 
                        'gallevent.main@gmail.com', 
                        [new_email_address])
            
            return HttpResponseRedirect('/login/invite_request_received/') # Redirect after POST

    return render_to_response('invite-request.html')

def invite_request_received(request):
    return render_to_response('invite-request-received.html')
    
def sign_in(request):
    return render_to_response('sign-in.html')

def manage_invites(request):
    invite_requests = models.InvitationManager.objects.filter(code='').order_by('date')
    email_choices = [invite_request.email for invite_request in invite_requests]
    dates = [invite_request.date for invite_request in invite_requests]
    values = [str(i) for i in range(len(invite_requests))]

    if request.method == 'POST':
        import uuid
        
        from django.core.mail import send_mail
        
        invite_details = []
        email_key, email_indexes = request.POST.lists()[0]
        email_indexes.reverse()
        
        for i in email_indexes:
            invite_details.append((dates[int(i)], email_choices[int(i)]))
            email_choices.remove(email_choices[int(i)])
        
        for invite_date, invite_email in invite_details:
            invite_data = models.InvitationManager.objects.get(email=invite_email, date=invite_date)
            uuid_hash = uuid.uuid4()
            invite_data.code = str(uuid_hash)
            invite_data.save()
            
            send_mail('Thank you for your interest in Gallevent', 
                    'Here is your invite code: '+ invite_data.code, 
                    'gallevent.main@gmail.com', 
                    [invite_email])  
        
    
    return render_to_response('control/manage-invites.html', {
        'invite_requests': zip(email_choices, dates, values),
    })
