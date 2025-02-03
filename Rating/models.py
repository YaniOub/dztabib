from django.db import models
from django.db import models
from django.contrib.auth import get_user_model
from dz_tabib.models import Doctor, Patient  # Import des modèles existants

User = get_user_model()

class Rating(models.Model):
    rating_id = models.BigAutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    note = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # Échelle de 1 à 5
    title = models.CharField(max_length=100)
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rating {self.note}/5 by {self.patient} for {self.doctor}"

class RatingLike(models.Model):
    like_id = models.BigAutoField(primary_key=True)
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Un utilisateur peut aimer une évaluation
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('rating', 'user')  # Empêche un utilisateur de liker plusieurs fois la même évaluation

    def __str__(self):
        return f"Like by {self.user} on {self.rating}"

class RatingReply(models.Model):
    reply_id = models.BigAutoField(primary_key=True)
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE, related_name="replies")
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Peut être un médecin ou un patient
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply by {self.user} on {self.rating}"

class ReportedRating(models.Model):
    report_id = models.BigAutoField(primary_key=True)
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE, related_name="reports")
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[
        ('Pending', 'Pending'),
        ('Reviewed', 'Reviewed'),
        ('Rejected', 'Rejected')
    ], default='Pending')

    def __str__(self):
        return f"Report by {self.reported_by} on {self.rating}"

