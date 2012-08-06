from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User

from djangbone.views import BackboneAPIView

def show_profile(request):
    return render_to_response('your-profile.html', {
    }, context_instance=RequestContext(request))


class UserView(BackboneAPIView):
    serialize_fields = ['id', 'username', 'first_name', 'last_name', 'email']
    
    def dispatch(self, request, *args, **kwargs):
        self.base_queryset = User.objects.filter(id=request.user.id)
        return super(UserView, self).dispatch(request, *args, **kwargs)
