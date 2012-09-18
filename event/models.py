from django.db import models

class Event(models.Model):
    address1 = models.CharField(max_length=1000)
    address2 = models.CharField(max_length=64, blank=True)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=2)
    zipcode = models.CharField(max_length=16)
    category = models.CharField(max_length=64)
    keywords = models.CharField(max_length=255, blank=True)
    start_date = models.DateField()
    start_time = models.TimeField()
    end_date = models.DateField()
    end_time = models.TimeField()
    name = models.CharField(max_length=64)
    description = models.TextField()
    event_url = models.URLField(blank=True)
    rsvp_limit = models.IntegerField()
    organizer_email = models.EmailField(blank=True)
    organizer_phone = models.CharField(max_length=24, blank=True)
    organizer_url = models.URLField(blank=True)
    purchase_tickets = models.BooleanField(blank=True)
    ticket_type = models.CharField(max_length=32, blank=True)
    ticket_price = models.DecimalField(decimal_places=2, max_digits=10, blank=True)
    ticket_url = models.URLField(blank=True)
    user_id = models.IntegerField()
    longitude = models.FloatField()
    latitude = models.FloatField()
    status = models.IntegerField()
