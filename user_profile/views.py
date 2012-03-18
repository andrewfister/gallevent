from django.shortcuts import render_to_response

def show_profile(request):
    return render_to_response('your-profile.html')
