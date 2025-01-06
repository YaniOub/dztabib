from rest_framework import viewsets
from rest_framework.decorators import action
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

    # Récupérer le profil d'un médecin spécifique
    def retrieve(self, request, pk=None):
        """
        Retrieve a specific doctor's details by ID.
        """
        doctor = get_object_or_404(Doctor, pk=pk)
        serializer = DoctorSerializer(doctor)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Mettre à jour les informations d'un médecin par ID
    def update(self, request, pk=None):
        """
        Update a doctor's details by ID.
        """
        doctor = get_object_or_404(Doctor, pk=pk)  # Récupère le médecin par son ID
        serializer = DoctorSerializer(doctor, data=request.data)  # Valide les nouvelles données
        if serializer.is_valid():
            serializer.save()  # Sauvegarde les modifications
            return Response(serializer.data, status=status.HTTP_200_OK)  # Retourne les données mises à jour
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Erreurs si les données sont invalides

    # Endpoint pour récupérer ou mettre à jour les informations du médecin connecté
    @action(detail=False, methods=['GET', 'POST'])
    def me(self, request):
        (doctor, created) = Doctor.objects.get_or_create(user_id=request.user.id)
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
        (patient, created) = Patient.objects.get_or_create(user_id=request.user.id)
        if request.method == 'GET':
            serializer = PatientSerializer(patient)
            return Response(serializer.data)
        elif request.method == 'POST':
            serializer = PatientSerializer(patient, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

