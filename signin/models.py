from django.db import models

# Create your models here.
class InvitationManager(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=64)
    date = models.DateField(auto_now=True)
