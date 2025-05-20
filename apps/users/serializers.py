from rest_framework import serializers
from .models import User
from core.mixins.sanitize_mixin import BleachSanitizeMixin 

class UserSerializer(BleachSanitizeMixin, serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
