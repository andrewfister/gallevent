import json
import logging

from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.generic.base import View
from django.views.generic.edit import FormView
from django.forms.models import model_to_dict

from signin import forms


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


class JSONSignInView(View):
    def post(self, request):
        query_email = request.POST['email']
        query_password = request.POST['password']
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

            user_dict = model_to_dict(user, fields=['id', 'username', 'first_name', 'last_name', 'email'])
            user_dict['userName'] = user_dict['username']
            user_dict['firstName'] = user_dict['first_name']
            user_dict['lastName'] = user_dict['last_name']
            del user_dict['username']
            del user_dict['first_name']
            del user_dict['last_name']
        else:
            user_dict = {}
            logging.debug('invalid login')
            logger.info('invalid login')

        login_response = {'success': request.user.is_authenticated(),
                          'user': user_dict}
        return HttpResponse(json.dumps(login_response), content_type="application/json")


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
