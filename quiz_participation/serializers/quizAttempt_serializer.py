from rest_framework import serializers
from ..models import QuizAttempt

class QuizAttemptSerializer(serializers.ModelSerializer):
    """
    Serializer for the QuizAttempt model.

    This serializer handles the conversion of QuizAttempt model instances to and from JSON format.
    It includes all fields of the model but makes certain fields read-only.
    """

    class Meta:
        """
        Meta options for the QuizAttemptSerializer.

        Attributes:
            model (QuizAttempt): Specifies the model to be serialized.
            fields (str): Specifies that all fields of the model should be included in the serialized representation.
            read_only_fields (list): Specifies the fields that are read-only.
        """
        model = QuizAttempt
        fields = '__all__'
        read_only_fields = ['id', 'user', 'start_time', 'end_time', 'score', 'is_completed', 'created_at', 'updated_at']

    def to_representation(self, instance):
        """
        Customize the serialized representation of the QuizAttempt instance.

        This method customizes the 'quiz' field to include the quiz title.

        Args:
            instance (QuizAttempt): The QuizAttempt instance being serialized.

        Returns:
            dict: The serialized representation of the QuizAttempt instance.
        """
        representation = super().to_representation(instance)
        representation['quiz'] = instance.quiz.title if instance.quiz else None
        return representation

class StartQuizSerializer(serializers.Serializer):
    """
    Serializer for starting a quiz.

    This serializer handles the input data required to start a quiz, which includes the quiz ID.
    """

    quiz_id = serializers.UUIDField()

class SubmitAnswerSerializer(serializers.Serializer):
    """
    Serializer for submitting an answer to a quiz question.

    This serializer handles the input data required to submit an answer, which includes the question ID and the user's answer.
    """

    question_id = serializers.UUIDField()
    user_answer = serializers.JSONField()