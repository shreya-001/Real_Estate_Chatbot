# realtors/models.py
from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_realtor = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username
