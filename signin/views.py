import json
import logging

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.views.generic.base import View, TemplateView
from django.views.generic.edit import FormView

from signin import forms, models


logger = logging.getLogger('gallevent')

class SignInView(FormView):
    template_name = 'sign-in.html'
    form_class = forms.SignInForm
    success_url = '/profile'

    def form_valid(self, form):
        query_email = form.cleaned_data['email']
        query_password = form.cleaned_data['password']
        logging.debug('email: ' + query_email)
        logging.debug('password: ' + query_password)
        user = authenticate(username=query_email, password=query_password)

        if user is not None:
            logger.info('Found user: {}'.format(user.username))
            if user.is_active:
                logger.info('logging in')
                login(self.request, user)
            else:
                logging.debug('disabled account')
                logger.info('disabled account')
        else:
            logging.debug('invalid login')
            logger.info('invalid login')
        
        return super(SignInView, self).form_valid(form)


class SignOutView(View):
    def get(self, request):
        if request.user.is_authenticated():
            logout(request)

        login_response = {'success': request.user.is_authenticated()}
        return redirect('/signin/sign_in')


class JoinView(FormView):
    template_name = "join.html"
    form_class = forms.JoinForm
    success_url = '/profile'

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
