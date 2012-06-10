from django.db import models

class Event(models.Model):
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    zipcode = models.CharField(max_length=16)
    category = models.CharField(max_length=64)
    keywords = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    name = models.CharField(max_length=64)
    description = models.TextField()
    event_url = models.URLField()
    rsvp_limit = models.IntegerField()
    ticket_price = models.DecimalField(decimal_places=2)
    ticket_url = models.URLField()
