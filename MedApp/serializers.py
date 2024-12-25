from rest_framework import serializers
from .models import Doctor, Patient

class DoctorSerializer(serializers.ModelSerializer):
    is_doctor = serializers.SerializerMethodField()

    class Meta:
        model = Doctor
        fields = ['user_id', 'first_name', 'last_name', 'date_of_birth', 'speciality', 'diploma_code', 'is_doctor']
        extra_kwargs = {'user_id': {'read_only': True}}

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
        extra_kwargs = {'user_id': {'read_only': True}}

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