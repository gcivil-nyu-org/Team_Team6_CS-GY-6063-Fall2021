from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default="Hi, I'm using DayPlanner to discover my city!")
    is_private = models.BooleanField(default=False)
