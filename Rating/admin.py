from django.contrib import admin
from .models import Rating, RatingRelation

# Enregistrer le modèle Rating
@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('titre', 'note', 'date', 'commentaire')  # Colonnes affichées dans la liste des notations
    search_fields = ('titre', 'commentaire')  # Permet de rechercher des notations par titre ou commentaire
    list_filter = ('note', 'date')  # Filtrer par note ou par date

# Enregistrer le modèle RatingRelation
@admin.register(RatingRelation)
class RatingRelationAdmin(admin.ModelAdmin):
    list_display = ('rating', 'patient', 'doctor')  # Colonnes affichées dans la liste des relations
    search_fields = ('patient__name', 'doctor__name')  # Recherche par nom du patient ou du médecin
    list_filter = ('doctor', 'patient')  # Filtrer par médecin ou patient

