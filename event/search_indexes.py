import datetime
from haystack import indexes
from event.models import Event


class EventIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    keywords = indexes.CharField(model_attr='keywords')
    description = indexes.CharField(model_attr='description')
    start_date = indexes.DateField(model_attr='start_date')
    end_date = indexes.DateField(model_attr='end_date')
    location = indexes.LocationField(model_attr='get_location')
    user_id = indexes.IntegerField(model_attr='user_id', null=True)

    def get_model(self):
        return Event

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(end_date__gte=datetime.datetime.now())
