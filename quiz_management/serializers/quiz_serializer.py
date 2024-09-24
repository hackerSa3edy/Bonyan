from rest_framework import serializers
from ..models import Quiz

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'
        read_only_fields = ['id', 'creator', 'created_at', 'updated_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['creator'] = {'name': f"{instance.creator.first_name} {instance.creator.last_name}",}
        return representation