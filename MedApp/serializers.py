from rest_framework import serializers
from .models import Doctor, Patient, Appointment


class DoctorSerializer(serializers.ModelSerializer):
    is_doctor = serializers.SerializerMethodField()

    class Meta:
        model = Doctor
        fields = ['user_id','doctor_id', 'first_name', 'last_name', 'date_of_birth', 'speciality','location', 'diploma_code', 'is_doctor']
        extra_kwargs = {'user_id': {'read_only': True},
                        'is_doctor': {'read_only': True},
                        'doctor_id': {'read_only': True},
                        'location': {'required': False},}

    def get_is_doctor(self, obj):
        return obj.user.is_doctor

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data['user'].is_doctor = True  
        validated_data['user'].is_patient = False
        validated_data['user'].save()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().update(instance, validated_data)

class PatientSerializer(serializers.ModelSerializer):
    is_patient = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = ['user_id', 'first_name', 'last_name', 'date_of_birth', 'is_patient']
        extra_kwargs = {'user_id': {'read_only': True},
                        'is_patient': {'read_only': True}}

    def get_is_patient(self, obj):
        return obj.user.is_patient

    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data['user'].is_patient = True  # Set is_patient to True
        validated_data['user'].is_doctor = False  # Set is_doctor to False
        validated_data['user'].save()
        return super().create(validated_data)


    def update(self, instance, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().update(instance, validated_data)
    

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['appointment_id','patient_name','patient_email','type', 'date','time', 'status']
        extra_kwargs = {'appointment_id': {'read_only': True}}
    patient_name = serializers.SerializerMethodField('get_patient_name')
    patient_email = serializers.SerializerMethodField('get_patient_email')

    def get_patient_name(self, obj : Appointment):
        return "".join([obj.patient.first_name, " ", obj.patient.last_name])
    
    def get_patient_email(self, obj : Appointment):
        return f"{obj.patient.user.email}"  
    
    def create(self, validated_data):
        user = self.context['request'].user
        patient = Patient.objects.get(user=user)
        doctor = Doctor.objects.get(pk=self.context['view'].kwargs['doctor_pk'])
        
        appointment = Appointment(**validated_data)
        appointment.doctor = doctor
        appointment.patient = patient 
        appointment.save()
        return appointment