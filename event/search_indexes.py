import datetime
from haystack import indexes
from gallevent.event.models import Event


class EventIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    keywords = indexes.CharField(model_attr='keywords')
    description = indexes.CharField(model_attr='description')
    start_date = indexes.DateField(model_attr='start_date')
    end_date = indexes.DateField(model_attr='end_date')
    location = indexes.LocationField(model_attr='get_location')

    def get_model(self):
        return Event

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
        
