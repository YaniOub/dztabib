from django.urls import path
from .views import RatingListCreate, RatingRelationListCreate

urlpatterns = [
    path('Ratings/', RatingListCreate.as_view(), name='Rating-list'),
    path('Rating-relations/', RatingRelationListCreate.as_view(), name='Rating-relation-list'),
]
