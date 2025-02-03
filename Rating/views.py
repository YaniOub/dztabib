from django.shortcuts import render
from rest_framework import generics
from .models import Rating, RatingRelation
from .serializers import RatingSerializer, RatingRelationSerializer

class RatingListCreate(generics.ListCreateAPIView):
    queryset = Rating.objects.all().order_by('-date')
    serializer_class = RatingSerializer

class RatingRelationListCreate(generics.ListCreateAPIView):
    queryset = RatingRelation.objects.all()
    serializer_class = RatingRelationSerializer

