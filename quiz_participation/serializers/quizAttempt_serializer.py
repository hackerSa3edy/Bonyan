from rest_framework import serializers
from ..models import QuizAttempt

class QuizAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizAttempt
        fields = '__all__'
        read_only_fields = ['id', 'user', 'start_time', 'end_time', 'score', 'is_completed', 'created_at', 'updated_at']

class StartQuizSerializer(serializers.Serializer):
    quiz_id = serializers.UUIDField()

class SubmitAnswerSerializer(serializers.Serializer):
    question_id = serializers.UUIDField()
    user_answer = serializers.JSONField()