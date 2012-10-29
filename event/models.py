from django.db import models

class Event(models.Model):
    address1 = models.CharField(max_length=1000)
    address2 = models.CharField(max_length=64, blank=True, null=True)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=2)
    zipcode = models.CharField(max_length=16)
    category = models.CharField(max_length=64)
    keywords = models.CharField(max_length=255, blank=True, null=False)
    start_date = models.DateField()
    start_time = models.TimeField()
    end_date = models.DateField()
    end_time = models.TimeField()
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=1024)
    event_url = models.URLField(blank=True, null=False)
    rsvp_limit = models.IntegerField(default=0)
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
    
    def get_location(self):
        from django.contrib.gis.geos import Point
        return Point(self.longitude, self.latitude)
