from django.shortcuts import render
from rest_framework import generics
from Rating.models import Rating, RatingRelation
from .serializers import RatingSerializer, RatingRelationSerializer
from rest_framework.permissions import IsAuthenticated


class RatingListCreate(generics.ListCreateAPIView):
    queryset = Rating.objects.all().order_by('-date')
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]


class RatingRelationListCreate(generics.ListCreateAPIView):
    queryset = RatingRelation.objects.all()
    serializer_class = RatingRelationSerializer


