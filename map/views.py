from django.shortcuts import render_to_response

def show(request):
    return render_to_response('index.html')
