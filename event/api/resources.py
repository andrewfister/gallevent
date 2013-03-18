# event/api.py
from tastypie.resources import ModelResource
from event.models import Event


class EventResource(ModelResource):
    class Meta:
        queryset = Event.objects.all()
        resource_name = 'events'
