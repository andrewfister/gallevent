import json
import logging

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.views.generic.base import View, TemplateView

from signin import forms, models


class SignInView(View):
    

    def post(self, request):
        form = forms.SignInForm(request.POST)
        login_response = {}

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

                    login_response['success'] = True
                    login_response['user'] = {
                        'id': user.id,
                        'userName': user.username,
                        'firstName': user.first_name,
                        'lastName': user.last_name,
                        'email': user.email
                    }
                    return HttpResponse(json.dumps(login_response), content_type="application/json")
                else:
                    logging.debug('disabled account')
                    print 'disabled account'
            else:
                logging.debug('invalid login')
                print 'invalid login'

        login_response['success'] = False
        return HttpResponse(json.dumps(login_response), content_type="application/json")


class SignOutView(View):
    def post(self, request):
        if request.user.is_authenticated():
            logout(request)

        login_response = {'success': request.user.is_authenticated()}
        return HttpResponse(json.dumps(login_response), content_type="application/json")


class JoinView(TemplateView):
    template_name = "join.html"

    def post(self, request):
        register_response = {}
        form = forms.RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            query_email = form.cleaned_data['email']
            query_password = form.cleaned_data['password']
            user = authenticate(username=query_email, password=query_password)

            if user is not None:
                if user.is_active:
                    logging.debug('logging in')
                    login(request, user)

                    register_response['success'] = True
                else:
                    register_response['success'] = False
                    logging.debug('disabled account')
                    print 'disabled account'
            else:
                register_response['success'] = False
                logging.debug('invalid login')
                print 'invalid login'

        return self.render_to_response(register_response)
        

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
                    invite_email + ' is using Gallevent&trade;, a place to find events and discover awesome things to do, and is inviting you to join.\nhttp://froggi.andrewfister.com/login/invite_code?invite_code='+ invite_data.code + '&email=' + invite_email + '\nMembership to Gallevent&trade; is by invitation only. Each user receives a limited number of invitations, which they may share with their friends.',
                    'gallevent.main@gmail.com',
                    [invite_email])


    return render_to_response('control/manage-invites.html', {
        'invite_requests': zip(email_choices, dates, values),
    }, context_instance=RequestContext(request))
