from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework import viewsets
from .models import Doctor, Patient
from .serializers import DoctorSerializer, PatientSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    # permission_classes = [IsAuthenticated]


    @action(detail=False, methods=['GET', 'POST'])
    def me(self, request):
        (doctor, created) = Doctor.objects.get_or_create(
            user_id=request.user.id)
        if request.method == 'GET':
            serializer = DoctorSerializer(doctor)
            return Response(serializer.data)
        elif request.method == 'POST':
            serializer = DoctorSerializer(doctor, data=request.data)

            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    # permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['GET', 'POST'])
    def me(self, request):
        (patient, created) = Patient.objects.get_or_create(
            user_id=request.user.id)
        if request.method == 'GET':
            serializer = PatientSerializer(patient)
            return Response(serializer.data)
        elif request.method == 'POST':
            serializer = PatientSerializer(patient, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
