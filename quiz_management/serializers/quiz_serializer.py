from rest_framework import serializers
from ..models import Quiz

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'
        read_only_fields = ['id', 'creator', 'created_at', 'updated_at']