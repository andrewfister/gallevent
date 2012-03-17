from django.shortcuts import render_to_response

def invite_code(request):
    return render_to_response('invite-code.html')
    
def invite_request(request):
    return render_to_response('invite-request.html')
    
def sign_in(request):
    return render_to_response('sign-in.html')
