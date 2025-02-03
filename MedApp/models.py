from django.db import models
from django.contrib.auth import get_user_model
# from Rating.models import Rating , RatingRelation
User = get_user_model()

GENDER_MALE = 'M'
GENDER_FEMALE = 'F'
GENDER_UNKNOWN = 'U'

GENDER_CHOICES = [
    (GENDER_MALE, 'Male'),
    (GENDER_FEMALE, 'Female'),
    (GENDER_UNKNOWN , 'Unknown')
]

APPOINTMENT_TYPE_ONLINE = 'ONLINE'
APPOINTMENT_TYPE_OFFLINE = 'OFFLINE'

APPOINTMENT_TYPE_CHOICES = [
    (APPOINTMENT_TYPE_ONLINE, 'Online'),
    (APPOINTMENT_TYPE_OFFLINE, 'Offline')
]


APPOINTMENT_STATUS_PENDING = 'PENDING'
APPOINTMENT_STATUS_CONFIRMED = 'CONFIRMED'
APPOINTMENT_STATUS_COMPLETED = 'COMPLETED'
APPOINTMENT_STATUS_CANCELLED = 'CANCELLED'
APPOINTMENT_STATUS_DELAYED = 'DELAYED'

APPOINTMENT_STATUS_CHOICES = [
    (APPOINTMENT_STATUS_PENDING, 'Pending'),
    (APPOINTMENT_STATUS_CONFIRMED, 'Confirmed'),
    (APPOINTMENT_STATUS_COMPLETED, 'Completed'),
    (APPOINTMENT_STATUS_CANCELLED, 'Cancelled'),
    (APPOINTMENT_STATUS_DELAYED, 'Delayed')
]

### 1️⃣ Patient
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Gère l'authentification
    patient_id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    date_of_birth = models.DateField(null=True)
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='O')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

### 2️⃣ Speciality
class Speciality(models.Model):
    speciality_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

### 3️⃣ Doctor
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  
    doctor_id = models.BigAutoField(primary_key=True)
    speciality = models.ForeignKey('Speciality', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='O')
    diploma_code = models.CharField(max_length=50, null=True, blank=True)
    date_of_birth = models.DateField()  # Ensure this field exists!


    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name} - {self.speciality.name}"

### 4️⃣ Insurance
class Insurance(models.Model):
    insurance_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

### 5️⃣ Appointment
class Appointment(models.Model):
    appointment_id = models.BigAutoField(primary_key=True)
    date = models.DateField()
    time = models.TimeField()
    type = models.CharField(max_length=10, choices=APPOINTMENT_TYPE_CHOICES, default='offline')
    status = models.CharField(max_length=10, choices=APPOINTMENT_STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=255)
    priority = models.IntegerField(null=True, blank=True)
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE)

    def __str__(self):
        return f"Appointment {self.appointment_id} - {self.patient} with {self.doctor}"



### 7️⃣ Patient Insurance (relation many-to-many)
class PatientInsurance(models.Model):
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    insurance = models.ForeignKey('Insurance', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.patient} - {self.insurance}"

### 8️⃣ Doctor Insurance (relation many-to-many)
class DoctorInsurance(models.Model):
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE)
    insurance = models.ForeignKey('Insurance', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.doctor} - {self.insurance}"


### 🔟 Language
class Language(models.Model):
    language_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

### 1️⃣1️⃣ Doctor Languages (relation many-to-many)
class DoctorLanguage(models.Model):
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE)
    language = models.ForeignKey('Language', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.doctor} speaks {self.language}"
