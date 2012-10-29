import datetime
from haystack.indexes import *
from haystack import site
from gallevent.event.models import Event


class EventIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    name = CharField(model_attr='name')
    keywords = CharField(model_attr='keywords')
    description = CharField(model_attr='description')
    start_date = DateField(model_attr='start_date')
    end_date = DateField(model_attr='end_date')
    location = LocationField(model_attr='get_location')

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return Event.objects.all()


site.register(Event, EventIndex)
