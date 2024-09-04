
# Create your models here.
from django.db import models
from datetime import date
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    image = models.FileField(upload_to="users_media/", blank=True, null=True)
