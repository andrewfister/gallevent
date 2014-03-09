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


class SignOutView(View):
    def post(self, request):
        if request.user.is_authenticated():
            logout(request)

        login_response = {'success': request.user.is_authenticated()}
        return HttpResponse(json.dumps(login_response), content_type="application/json")


class JoinView(FormView):
    template_name = "join.html"
    form_class = forms.RegistrationForm
    success_url = '/user_profile/show'

    def get(self, request):
        return self.render_to_response({})

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
