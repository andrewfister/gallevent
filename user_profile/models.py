from django.db import models

# Create your models here.
class UserProfile(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    fname = models.CharField(max_length=256L, blank=True)
    lname = models.CharField(max_length=256L, blank=True)
    bio = models.TextField(blank=True)
    short_bio = models.CharField(max_length=64L, blank=True)
    gender = models.IntegerField(null=True, blank=True)
    relationship = models.IntegerField(null=True, blank=True)
    interests = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=1000L, blank=True)
    street_number = models.CharField(max_length=64L, blank=True)
    street = models.CharField(max_length=255L, blank=True)
    subpremise = models.CharField(max_length=64L, blank=True)
    city = models.CharField(max_length=64L, blank=True)
    state = models.CharField(max_length=2L, blank=True)
    zipcode = models.CharField(max_length=16L, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    email = models.CharField(max_length=75L, blank=True)
    phone = models.CharField(max_length=24L, blank=True)
    website = models.CharField(max_length=200L, blank=True)
    facebook = models.CharField(max_length=200L, blank=True)
    twitter = models.CharField(max_length=64L, blank=True)
    school = models.CharField(max_length=255L, blank=True)
    study_field = models.CharField(max_length=255L, blank=True)
    job_title = models.CharField(max_length=255L, blank=True)
    company = models.CharField(max_length=255L, blank=True)
    privacy = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    status = models.IntegerField()
    class Meta:
        db_table = 'user_profile_profile'
    
    def create_profile_for_user(self, user):
        self.user_id = user.id
        self.email = user.email
        self.privacy = 0
        self.status = 0
        self.save()
