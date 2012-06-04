from django.shortcuts import render_to_response
from django.template import RequestContext

def post_event(request):
    return render_to_response('post-event.html', {
    'edit': False
    }, context_instance=RequestContext(request))

def edit_event(request):
    return render_to_response('post-event.html', {
    'edit': True
    }, context_instance=RequestContext(request))

def show_events(request):
    return render_to_response('your-posts.html', {
    'selected_page': 'your-posts'
    }, context_instance=RequestContext(request))

def show_lineup(request):
    return render_to_response('your-posts.html', {
    'selected_page': 'your-events'
    }, context_instance=RequestContext(request))

def manage_events(request):
    return render_to_response('your-posts-manage.html', {
    }, context_instance=RequestContext(request))
