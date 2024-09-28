from rest_framework import serializers
from ..models import UserAnswer

class UserAnswerSerializer(serializers.ModelSerializer):
    """
    Serializer for the UserAnswer model.

    This serializer handles the conversion of UserAnswer model instances to and from JSON format.
    It includes all fields of the model but makes certain fields read-only.
    """

    class Meta:
        """
        Meta options for the UserAnswerSerializer.

        Attributes:
            model (UserAnswer): Specifies the model to be serialized.
            fields (str): Specifies that all fields of the model should be included in the serialized representation.
            read_only_fields (list): Specifies the fields that are read-only.
        """
        model = UserAnswer
        fields = '__all__'
        read_only_fields = ['id', 'quiz_attempt', 'is_correct', 'created_at']
