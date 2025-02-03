from django.db import models
from MedApp.models import Doctor , Patient
# Create your models here.
### 6️⃣ Rating
class Rating(models.Model):
    rating_id = models.BigAutoField(primary_key=True)
    note = models.IntegerField()  # Note de 1 à 5
    titre = models.CharField(max_length=255)
    commentaire = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titre} - {self.note}/5"
### 9️⃣ Rating Relation (relation entre patient, docteur et rating)
class RatingRelation(models.Model):
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    def __str__(self):
        return f"Rating {self.rating.id} by {self.patient} for {self.doctor}"
