from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework import viewsets
from .models import Doctor, Patient, Appointment
from .serializers import DoctorSerializer, PatientSerializer, AppointmentSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.pagination  import PageNumberPagination
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta
from . import permissions
from django.db import connection


def is_time_overlapping(date, time):
    time_start = (datetime.combine(date, time)).time()
    time_end = (datetime.combine(date, time) + timedelta(minutes=29)).time()
    return Appointment.objects.filter(date=date, time__range=(time_start, time_end)).exists()


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination 


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
    
    @action(detail=False, methods=['GET'], url_path='search')
    def search(self, request):
        speciality = request.query_params.get('speciality', None)
        location = request.query_params.get('location', None)
        availability = request.query_params.get('availability', None)
        insurance = request.query_params.get('insurance', None)

        doctors = Doctor.objects.all()

        if speciality:
            doctors = doctors.filter(speciality__icontains=speciality)
        if location:
            doctors = doctors.filter(location__icontains=location)
        if availability is not None:
            doctors = doctors.filter(availability=availability.lower() == 'true')
        if insurance:
            doctors = doctors.filter(insurance_accepted__icontains=insurance)

        page = self.paginate_queryset(doctors)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(doctors, many=True)
        return Response(serializer.data)

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

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

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    pagination_class = PageNumberPagination
    
    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated, permissions.IsPatient]
        elif self.action in ['destroy']:
            self.permission_classes = [IsAuthenticated, permissions.IsDoctor]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def create(self, request, doctor_pk=None):
        serializer = AppointmentSerializer(data=request.data, context={'request': request, 'view': self})
        serializer.is_valid(raise_exception=True)
        date = serializer.validated_data['date']
        time = serializer.validated_data['time'] 
        if date < datetime.today().date():
            return Response({'error': 'You cannot create an appointment in the past'}, status=status.HTTP_400_BAD_REQUEST)

        if is_time_overlapping(date, time):
            return Response({'error': 'An appointment already exists for this date and time'}, status=status.HTTP_400_BAD_REQUEST)       

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        appointment = get_object_or_404(Appointment, pk=pk)
        serializer = AppointmentSerializer(appointment, data=request.data, context = {'request': request, 'view': self})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        appointment = get_object_or_404(Appointment, pk=pk)
        appointment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

    def list(self, request):
        user = request.user
        if user.is_patient:
            queryset = Appointment.objects.filter(patient__user=user)
        elif user.is_doctor:
            queryset = Appointment.objects.filter(doctor__user=user)
        else:
            queryset = Appointment.objects.none()
        
        serializer = AppointmentSerializer(queryset, many=True)
        return Response(serializer.data)


# class AppointmentViewSet(viewsets.ViewSet):

#     permission_classes = [IsAuthenticated]

#     @action(detail=False, methods=['POST'], permission_classes=[permissions.IsPatient])
#     def create(self, request):
#         date = request.data.get('date')
#         time = request.data.get('time')

#         if datetime.strptime(date, '%Y-%m-%d').date() < datetime.today().date():
#             return Response({'error': 'You cannot create an appointment in the past'}, status=status.HTTP_400_BAD_REQUEST)

#         with connection.cursor() as cursor:
#             cursor.execute("SELECT COUNT(*) FROM MedApp_appointment WHERE date = %s AND time = %s", [date, time])
#             if cursor.fetchone()[0] > 0:
#                 return Response({'error': 'An appointment already exists for this date and time'}, status=status.HTTP_400_BAD_REQUEST)

#             cursor.execute("INSERT INTO MedApp_appointment (date, time, patient_id, doctor_id) VALUES (%s, %s, %s, %s) RETURNING id",
#                            [date, time, request.data.get('patient_id'), request.data.get('doctor_id')])
#             appointment_id = cursor.fetchone()[0]

#         return Response({'id': appointment_id, 'date': date, 'time': time}, status=status.HTTP_201_CREATED)

#     @action(detail=False, methods=['PUT'], permission_classes=[permissions.IsDoctor])
#     def update(self, request, pk=None):
#         date = request.data.get('date')
#         time = request.data.get('time')

#         with connection.cursor() as cursor:
#             cursor.execute("UPDATE MedApp_appointment SET date = %s, time = %s WHERE id = %s",
#                            [date, time, pk])

#         return Response({'id': pk, 'date': date, 'time': time})

#     @action(detail=False, methods=['DELETE'], permission_classes=[permissions.IsDoctor])
#     def destroy(self, request, pk=None):
#         with connection.cursor() as cursor:
#             cursor.execute("DELETE FROM MedApp_appointment WHERE id = %s", [pk])

#         return Response(status=status.HTTP_204_NO_CONTENT)
