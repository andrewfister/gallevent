import datetime, decimal, json

from django.utils.timezone import is_aware
from django.db import models
from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers.json import Serializer as JSONSerializer

class Event(models.Model):
    class Meta:
        unique_together = ('source_event_id', 'source_id')

    date_input_formats = [
        '%m/%d/%Y',       # '10/25/2006'
        '%b %d, %Y',      # 'Oct 25, 2006'
        '%Y-%m-%d',       # '2006-10-25'
        '%m/%d/%y',       # '10/25/06'
        '%b %m %d',       # 'Oct 25 2006'
        '%d %b %Y',       # '25 Oct 2006'
        '%d %b, %Y',      # '25 Oct, 2006'
        '%B %d %Y',       # 'October 25 2006'
        '%B %d, %Y',      # 'October 25, 2006'
        '%d %B %Y',       # '25 October 2006'
        '%d %B, %Y',      # '25 October, 2006'
    ]

    address = models.CharField(max_length=1000)
    street_number = models.CharField(max_length=64)
    street = models.CharField(max_length=255)
    subpremise = models.CharField(max_length=64, blank=True, null=True)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=2)
    zipcode = models.CharField(max_length=16)
    category = models.CharField(max_length=64)
    keywords = models.CharField(max_length=255, blank=True, null=False)
    start_date = models.DateField()
    start_time = models.TimeField()
    end_date = models.DateField()
    end_time = models.TimeField()
    name = models.CharField(max_length=256)
    short_description = models.CharField(max_length=64)
    description = models.TextField()
    event_url = models.URLField(blank=True, null=False)
    rsvp_limit = models.IntegerField(default=0)
    rsvp_end_date = models.DateField(blank=True, null=False)
    rsvp_end_time = models.TimeField(blank=True, null=False)
    organizer_email = models.EmailField(blank=True, null=False)
    organizer_phone = models.CharField(max_length=24, blank=True, null=False)
    organizer_url = models.URLField(blank=True, null=False)
    purchase_tickets = models.BooleanField(blank=True, null=False)
    ticket_type = models.CharField(max_length=32, blank=True, null=False)
    ticket_price = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=False)
    ticket_url = models.URLField(blank=True, null=False)
    user_id = models.IntegerField()
    longitude = models.FloatField()
    latitude = models.FloatField()
    status = models.IntegerField(default=1)
    source_event_id = models.CharField(max_length=64, default='1')
    source_id = models.IntegerField(default=1)
    
    def get_location(self):
        from django.contrib.gis.geos import Point
        return Point(self.longitude, self.latitude)


class GuestType(models.Model):
    guest_type_name = models.CharField(max_length=64)
    price = models.FloatField()
    event_id = models.IntegerField()

class Guest(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    user_id = models.IntegerField(blank=True, null=False)
    event_id = models.IntegerField()
    guest_type_id = models.IntegerField()


class EventJSONEncoder(DjangoJSONEncoder):
    """
    JSONEncoder subclass that knows how to encode date/time and decimal types.
    """
    def default(self, o):
        # See "Date Time String Format" in the ECMA-262 specification.
        if isinstance(o, datetime.datetime):
            r = o.strftime('%m/%d/%Y %I:%M%p')
            if o.microsecond:
                r = r[:23] + r[26:]
            if r.endswith('+00:00'):
                r = r[:-6] + 'Z'
            return r
        elif isinstance(o, datetime.date):
            return o.strftime('%m/%d/%Y')
        elif isinstance(o, datetime.time):
            if is_aware(o):
                raise ValueError("JSON can't represent timezone-aware times.")
            r = o.strftime('%I:%M%p')
            if o.microsecond:
                r = r[:12]
            return r
        elif isinstance(o, decimal.Decimal):
            return str(o)
        else:
            return super(DjangoJSONEncoder, self).default(o)


class EventJSONSerializer(JSONSerializer):
    def end_object(self, obj):
        # self._current has the field data
        indent = self.options.get("indent")
        if not self.first:
            self.stream.write(",")
            if not indent:
                self.stream.write(" ")
        if indent:
            self.stream.write("\n")
        json.dump(self.get_dump_object(obj), self.stream,
                  cls=EventJSONEncoder, **self.json_kwargs)
        self._current = None

    def get_dump_object(self, obj):
        return self._current
