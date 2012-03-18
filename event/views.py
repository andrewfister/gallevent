from django.shortcuts import render_to_response

def post_event(request):
    return render_to_response('post-event.html', {'edit': False})

def edit_event(request):
    return render_to_response('post-event.html', {'edit': True})

def show_events(request):
    return render_to_response('your-posts.html', {'selected_page': 'your-posts'})

def show_lineup(request):
    return render_to_response('your-posts.html', {'selected_page': 'your-events'})

def manage_events(request):
    return render_to_response('your-posts-manage.html')
