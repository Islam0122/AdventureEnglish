from rest_framework import serializers
from ..models import StudentProfile
from .user_serializers import UserSerializer, UserMinimalSerializer


class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserMinimalSerializer(read_only=True)

    class Meta:
        model = StudentProfile
        fields = [
            'id',
            'user',
            'avatar',
            'bio',
            'phone_number',
            'birth_date',
            'created_at'
        ]
        read_only_fields = ['id', 'user', 'created_at']

    def validate_phone_number(self, value):
        if value and not value.startswith('+'):
            raise serializers.ValidationError(
                "Номер телефона должен начинаться с '+'"
            )
        return value


class StudentProfileDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    has_complete_profile = serializers.BooleanField(read_only=True)

    class Meta:
        model = StudentProfile
        fields = [
            'id',
            'user',
            'avatar',
            'bio',
            'phone_number',
            'birth_date',
            'has_complete_profile',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'id',
            'user',
            'has_complete_profile',
            'created_at',
            'updated_at'
        ]