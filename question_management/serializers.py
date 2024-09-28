from rest_framework import serializers
from .models import Question

class QuestionSerializer(serializers.ModelSerializer):
    """
    Serializer for the Question model.

    This serializer handles the conversion of Question model instances to and from JSON format.
    It includes all fields of the model but makes 'id', 'quiz', 'created_at', and 'updated_at' read-only.
    Additionally, it removes the 'correct_answer' field from the serialized representation.
    """

    class Meta:
        model = Question
        fields = '__all__'
        read_only_fields = ['id', 'quiz', 'created_at', 'updated_at']

    def to_representation(self, instance):
        """
        Customize the serialized representation of the Question instance.

        This method removes the 'correct_answer' field from the serialized data.

        Args:
            instance (Question): The Question instance being serialized.

        Returns:
            dict: The serialized representation of the Question instance.
        """
        representation = super().to_representation(instance)
        representation.pop('correct_answer', None)
        return representation