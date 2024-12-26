from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers

class UserCreateSerializer(BaseUserCreateSerializer):
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def create(self, validated_data):
        user = super().create(validated_data)
        refresh = RefreshToken.for_user(user)
        user.access = str(refresh.access_token)
        user.refresh = str(refresh)
        return user

    class Meta(BaseUserCreateSerializer.Meta):
        fields = BaseUserCreateSerializer.Meta.fields + ('access', 'refresh',)