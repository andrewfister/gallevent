from django.shortcuts import render_to_response
from django.contrib.auth.models import User


def show(request):

    return render_to_response('index.html', {
        'username': request.user.username,
    })
