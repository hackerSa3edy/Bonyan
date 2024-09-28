from rest_framework import serializers
from ..models import QuizAssignment

class QuizAssignmentSerializer(serializers.ModelSerializer):
    """
    Serializer for the QuizAssignment model.

    This serializer handles the conversion of QuizAssignment model instances to and from JSON format.
    It includes all fields of the model but makes 'id' and 'assigned_at' read-only.
    """

    class Meta:
        """
        Meta options for the QuizAssignmentSerializer.

        Attributes:
            model (QuizAssignment): Specifies the model to be serialized.
            fields (str): Specifies that all fields of the model should be included in the serialized representation.
            read_only_fields (list): Specifies the fields that are read-only.
        """
        model = QuizAssignment
        fields = '__all__'
        read_only_fields = ['id', 'assigned_at']