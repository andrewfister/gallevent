from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext

from gallevent.login import forms
from gallevent.login import models

def invite_code(request):
    email = ''
    invite_code = ''
    import logging
    logging.debug('calling register')

    if request.method == 'POST':
        logging.debug('submitting register')
        form = forms.RegistrationForm(request.POST)
        if form.is_valid():
            logging.debug('register form is valid')
            form.save()
            query_email = form.cleaned_data['email']
            query_password = form.cleaned_data['password']
            user = authenticate(username=query_email, password=query_password)
            logging.debug('email: ' + query_email)
            logging.debug('password: ' + query_password)
        
            if user is not None:
                if user.is_active:
                    logging.debug('logging in')
                    login(request, user)
                    
                    return HttpResponseRedirect('/') # Redirect after POST
                else:
                    logging.debug('disabled account')
                    print 'disabled account'
            else:
                logging.debug('invalid login')
                print 'invalid login'
            
            return HttpResponseRedirect('/event/show/')
        
        email = request.POST['email']
        invite_code = request.POST['invite_code']
    elif request.method == 'GET':
        invite_code = request.GET['invite_code']
        email = request.GET['email']
    
    return render_to_response('invite-code.html', {
        'email': email,
        'invite_code': invite_code,
    }, context_instance=RequestContext(request))
    
        
def invite_request(request):
    import logging
    logging.debug('request invite?');
    if request.method == 'POST': # If the form has been submitted...
        form = forms.RequestInviteForm(request.POST) # A form bound to the POST data
        
        logging.debug('validating email');
        if form.is_valid(): # All validation rules pass
            form.save()
            
            # Process the data in form.cleaned_data
            new_email_address = form.cleaned_data['email']
            
            
            logging.debug('sending email')
            
            from django.core.mail import send_mail
            send_mail('Thank you for your interest in Gallevent', 
                        'Your invite is on the way!', 
                        'gallevent.main@gmail.com', 
                        [new_email_address])
            
            return HttpResponseRedirect('/login/invite_request_received/') # Redirect after POST

    return render_to_response('invite-request.html', {
    }, context_instance=RequestContext(request))

def invite_request_received(request):
    return render_to_response('invite-request-received.html', {
    }, context_instance=RequestContext(request))
    
def sign_in(request):
    import logging
    logging.debug('loading sign-in page')
    
    if request.method == 'POST':
        form = forms.SignInForm(request.POST)
        if form.is_valid():
            query_email = form.cleaned_data['email']
            query_password = form.cleaned_data['password']
            logging.debug('email: ' + query_email)
            logging.debug('password: ' + query_password)
            user = authenticate(username=query_email, password=query_password)
        
            if user is not None:
                if user.is_active:
                    logging.debug('logging in')
                    login(request, user)
                    
                    return HttpResponseRedirect(request.POST['next']) # Redirect after POST
                else:
                    logging.debug('disabled account')
                    print 'disabled account'
            else:
                logging.debug('invalid login')
                print 'invalid login'
    
    return render_to_response('sign-in.html', {
        'next': request.GET['next'] if request.GET.has_key('next') else '/'
    }, context_instance=RequestContext(request))
    
def sign_out(request):
    if request.user.is_authenticated():
        logout(request)
        
    return HttpResponseRedirect('/login/sign_in') # Redirect after logout

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
                    invite_email + ' is using Gallevent&trade;, a place to find events and discover awesome things to do, and is inviting you to join.\nhttp://froggi.andrewfister.com/login/invite_code?invite_code='+ invite_data.code + '&email=' + invite_email, 
                    'gallevent.main@gmail.com',
					Membership to Gallevent&trade; is by invitation only. Each user receives a limited number of invitations, which they may share with their friends.
                    [invite_email])  
        
    
    return render_to_response('control/manage-invites.html', {
        'invite_requests': zip(email_choices, dates, values),
    }, context_instance=RequestContext(request))
