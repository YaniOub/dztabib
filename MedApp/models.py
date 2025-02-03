from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female')
]

class Patient(models.Model):
    patient_id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    password = models.CharField(max_length=128)  # Stocké en hash via Django
    date_of_birth = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to='patients/', null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='U')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Speciality(models.Model):
    speciality_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Doctor(models.Model):
    doctor_id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, unique=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Stocké en hash via Django
    photo = models.ImageField(upload_to='doctors/', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='U')
    speciality = models.ForeignKey(Speciality, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name} - {self.speciality.name if self.speciality else 'Généraliste'}"

class Insurance(models.Model):
    insurance_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Appointment(models.Model):
    appointment_id = models.BigAutoField(primary_key=True)
    date = models.DateTimeField()
    appointment_type = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=50)
    priority = models.CharField(max_length=50)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    def __str__(self):
        return f"Appointment {self.appointment_id} - {self.patient.first_name} with {self.doctor.user.first_name}"

class Rating(models.Model):
    rating_id = models.BigAutoField(primary_key=True)
    note = models.IntegerField()
    title = models.CharField(max_length=100)
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rating {self.rating_id} - {self.note}/5"

class PatientInsurance(models.Model):
    patient_insurance_id = models.BigAutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    insurance = models.ForeignKey(Insurance, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.patient} - {self.insurance}"

class DoctorInsurance(models.Model):
    doctor_insurance_id = models.BigAutoField(primary_key=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    insurance = models.ForeignKey(Insurance, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.doctor} - {self.insurance}"

class RatingRelation(models.Model):
    rating_relation_id = models.BigAutoField(primary_key=True)
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    def __str__(self):
        return f"Rating {self.rating} by {self.patient} for {self.doctor}"

class Language(models.Model):
    language_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class DoctorLanguages(models.Model):
    doctor_language_id = models.BigAutoField(primary_key=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.doctor} speaks {self.language}"
