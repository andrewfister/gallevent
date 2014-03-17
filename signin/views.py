import json
import logging

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.views.generic.base import View, TemplateView
from django.views.generic.edit import FormView

from signin import forms, models


class SignInView(TemplateView):
    

    def post(self, request):
        form = forms.RegistrationForm(request.POST)
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


class SignOutView(FormView):
    def post(self, request):
        if request.user.is_authenticated():
            logout(request)

        login_response = {'success': request.user.is_authenticated()}
        return HttpResponse(json.dumps(login_response), content_type="application/json")


class JoinView(FormView):
    template_name = "join.html"
    form_class = forms.SignInForm
    success_url = '/profile/show'

    def form_valid(self, form):
        form.create_user()
        query_email = form.cleaned_data['email']
        query_password = form.cleaned_data['password']
        user = authenticate(username=query_email, password=query_password)

        if user is not None:
            if user.is_active:
                logging.debug('form: {}'.format(form))
                logging.debug('logging in')
                login(self.request, user)
            else:
                logging.debug('disabled account')
                print 'disabled account'
        else:
            logging.debug('invalid login')
            print 'invalid login'
        
        return super(JoinView, self).form_valid(form)

    def form_invalid(self, form):
        print 'blah blah'

        return super(JoinView, self).form_valid(form)
