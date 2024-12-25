from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_doctor = models.BooleanField(null=True)
    is_patient = models.BooleanField(null=True)