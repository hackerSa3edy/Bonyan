from rest_framework import serializers
from django.contrib.auth import get_user_model

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