#views.py

from django.shortcuts import render_to_response

from gallevent.invite.forms import InviteForm


def invite(response):
    if request.method == 'POST':
        form = InviteForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
    else:
        form = InviteForm()
            
    return render_to_response('contact_form.html', {'form': form})
