from django.db import models

# Create your models here.
class InvitationManager(models.Model):
    email = models.CharField(max_length=64)
    code = models.CharField(max_length=64)
    date = models.DateField(auto_now_add=True)
