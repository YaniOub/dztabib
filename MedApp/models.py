from django.db import models
from errno import EMFILE
from os import name
from pickle import TRUE
from random import choices
# Create your models here.

GENDER_MALE = 'M'
GENDER_FEMALE = 'F'
GENDER_UNKNOWN = 'U'

GENDER_CHOICES = [
    (GENDER_MALE, 'Male'),
    (GENDER_FEMALE, 'Female'),
    (GENDER_UNKNOWN , 'Unknown')
]

# Create your models here.
class Patient(models.Model):
    patient_id = models.BigAutoField(auto_created=True, primary_key=True),
    name = models.CharField(max_length=50)
    family_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone = models.CharField(null = TRUE)
    address = models.CharField(max_length=255, null = True)
    password = models.CharField(max_length=128)
    date_of_birth = models.DateField(null = True)
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    gender = models.CharField(max_length = 1, choices=GENDER_CHOICES, default = GENDER_UNKNOWN)

class Doctor(models.Model):
    doctor_id = models.BigAutoField(auto_created=True, primary_key=True)
    speciality_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=50)
    family_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=100)
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=GENDER_UNKNOWN)
    date_joined = models.DateTimeField(auto_now_add=True)
