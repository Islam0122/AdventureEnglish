from rest_framework import serializers
from .models import Feedback

class FeedbackSerializer(serializers.ModelSerializer):
    user_email = serializers.SerializerMethodField()

    class Meta:
        model = Feedback
        fields = [
            'id',
            'user',
            'user_email',
            'email',
            'subject',
            'message',
            'is_read',
            'created_at',
        ]
        read_only_fields = ['id', 'user', 'user_email', 'created_at']

    def get_user_email(self, obj):
        if obj.user:
            return obj.user.email
        return obj.email
