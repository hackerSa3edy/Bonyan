from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from quiz_management.models import Quiz
from quiz_participation.models import QuizAttempt

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'first_name', 'second_name', 'bio', 'avatar_url', 'role', 'created_at', 'updated_at']
        extra_kwargs = {
            'password': {'write_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True}
        }

    def validate_role(self, value):
        if value not in ['creator', 'resolver']:
            raise serializers.ValidationError("Role must be either 'creator' or 'resolver'.")
        return value

    def create(self, validated_data):
        role = validated_data['role']
        if role == 'admin' and not validated_data.get('is_superuser', False):
            raise serializers.ValidationError({"role": "Only superusers can have the admin role."})

        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            second_name=validated_data.get('second_name', ''),
            bio=validated_data.get('bio', ''),
            avatar_url=validated_data.get('avatar_url', ''),
            role=validated_data['role']
        )

        # Assign permissions based on role
        if role == 'admin':
            admin_group = Group.objects.get(name='Admin')
            user.groups.add(admin_group)
        elif role == 'creator':
            creator_group = Group.objects.get(name='Quiz Creator')
            user.groups.add(creator_group)
        elif role == 'resolver':
            participant_group = Group.objects.get(name='Quiz Resolver')
            user.groups.add(participant_group)

        return user
    
    def update(self, instance, validated_data):
        validated_data.pop('role', None)
        return super().update(instance, validated_data)

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get("request")
        if request and request.method == "PUT":
            NOT_REQUIRED_FILEDS = (
                "role",
            )
            for field_name in NOT_REQUIRED_FILEDS:
                fields[field_name].required = False
        return fields