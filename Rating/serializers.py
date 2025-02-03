from rest_framework import serializers
from Rating.models import Rating , RatingRelation

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'

class RatingRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RatingRelation
        fields = '__all__'
