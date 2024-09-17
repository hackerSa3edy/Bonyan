from rest_framework import serializers
from ..models import UserAnswer

class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = '__all__'
        read_only_fields = ['id', 'quiz_attempt', 'is_correct', 'created_at']
