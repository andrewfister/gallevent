#models.py

from django.db import models

class Invite(models.Model):
    email = models.CharField(max_length=50)
    invite_code = models.CharField(max_length=30)
