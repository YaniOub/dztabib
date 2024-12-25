from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

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
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    patient_id = models.BigAutoField(auto_created=True, primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(null=True, max_length=15)
    address = models.CharField(max_length=255, null=True)
    password = models.CharField(max_length=128)
    date_of_birth = models.DateField(null=True)
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=GENDER_UNKNOWN)

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    doctor_id = models.BigAutoField(auto_created=True, primary_key=True)
    speciality_id = models.IntegerField(null=True, blank=True)
    speciality = models.CharField(max_length=100, null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    date_of_birth = models.DateField(null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=GENDER_UNKNOWN)
    date_joined = models.DateTimeField(auto_now_add=True)
    diploma_code = models.CharField(max_length=50, null=True, blank=True)