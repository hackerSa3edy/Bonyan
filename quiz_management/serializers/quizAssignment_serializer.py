from rest_framework import serializers
from ..models import QuizAssignment

class QuizAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizAssignment
        fields = '__all__'
        read_only_fields = ['id', 'assigned_at']