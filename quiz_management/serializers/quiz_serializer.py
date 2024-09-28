from rest_framework import serializers
from ..models import Quiz

class QuizSerializer(serializers.ModelSerializer):
    """
    Serializer for the Quiz model.

    This serializer handles the conversion of Quiz model instances to and from JSON format.
    It includes all fields of the model but makes 'id', 'creator', 'created_at', and 'updated_at' read-only.
    Additionally, it customizes the representation of the 'creator' field.
    """

    class Meta:
        """
        Meta options for the QuizSerializer.

        Attributes:
            model (Quiz): Specifies the model to be serialized.
            fields (str): Specifies that all fields of the model should be included in the serialized representation.
            read_only_fields (list): Specifies the fields that are read-only.
        """
        model = Quiz
        fields = '__all__'
        read_only_fields = ['id', 'creator', 'created_at', 'updated_at']

    def to_representation(self, instance):
        """
        Customize the serialized representation of the Quiz instance.

        This method customizes the 'creator' field to include the creator's full name.

        Args:
            instance (Quiz): The Quiz instance being serialized.

        Returns:
            dict: The serialized representation of the Quiz instance.
        """
        representation = super().to_representation(instance)
        representation['creator'] = {
            'name': f"{instance.creator.first_name} {instance.creator.last_name}",
        }
        return representation