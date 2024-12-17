from errno import EMFILE
from os import name
from pickle import TRUE
from random import choices
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    