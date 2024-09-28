from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.

    This serializer handles the creation, update, and validation of User instances.
    It includes fields for user details and manages permissions based on user roles.

    Attributes:
        Meta (class): Meta class to specify the model and fields to be serialized.
        validate_role (method): Validates the role field to ensure it is either 'creator' or 'resolver'.
        create (method): Creates a new User instance and assigns permissions based on the role.
        update (method): Updates an existing User instance, excluding the role and password fields.
        get_fields (method): Customizes the fields based on the request method.
        to_representation (method): Customizes the representation of the User instance.
    """
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'bio', 'role', 'created_at', 'updated_at', 'avatar']
        extra_kwargs = {
            'password': {'write_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True}
        }

    def validate_role(self, value):
        """
        Validates the role field.

        Ensures that the role is either 'creator' or 'resolver'.

        Args:
            value (str): The role value to be validated.

        Returns:
            str: The validated role value.

        Raises:
            serializers.ValidationError: If the role is not 'creator' or 'resolver'.
        """
        if value not in ['creator', 'resolver']:
            raise serializers.ValidationError("Role must be either 'creator' or 'resolver'.")
        return value

    def create(self, validated_data):
        """
        Creates a new User instance.

        This method creates a new User instance and assigns permissions based on the role.
        Only superusers can have the 'admin' role.

        Args:
            validated_data (dict): The validated data for creating the User instance.

        Returns:
            User: The created User instance.

        Raises:
            serializers.ValidationError: If a non-superuser tries to have the 'admin' role.
        """
        role = validated_data['role']
        if role == 'admin' and not validated_data.get('is_superuser', False):
            raise serializers.ValidationError({"role": "Only superusers can have the admin role."})

        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            bio=validated_data.get('bio', ''),
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
        """
        Updates an existing User instance.

        This method updates the User instance, excluding the role and password fields.

        Args:
            instance (User): The User instance to be updated.
            validated_data (dict): The validated data for updating the User instance.

        Returns:
            User: The updated User instance.
        """
        validated_data.pop('role', None)
        validated_data.pop('password', None)
        return super().update(instance, validated_data)

    def get_fields(self):
        """
        Customizes the fields based on the request method.

        This method makes certain fields not required for PUT requests.

        Returns:
            dict: The fields for the serializer.
        """
        fields = super().get_fields()
        request = self.context.get("request")
        if request and request.method == "PUT":
            NOT_REQUIRED_FIELDS = (
                "role",
            )
            for field_name in NOT_REQUIRED_FIELDS:
                fields[field_name].required = False
        return fields

    def to_representation(self, instance):
        """
        Customizes the representation of the User instance.

        This method includes the avatar URL in the representation for GET and POST requests.

        Args:
            instance (User): The User instance to be represented.

        Returns:
            dict: The representation of the User instance.
        """
        representation = super().to_representation(instance)
        request = self.context.get("request")
        if request and request.method in ["GET", "POST"]:
            representation['avatar'] = instance.avatar.url if instance.avatar else None
        return representation

class UserAvatarSerializer(serializers.ModelSerializer):
    """
    Serializer for updating the user's avatar.

    This serializer handles the update of the avatar field for the User model.

    Attributes:
        Meta (class): Meta class to specify the model and fields to be serialized.
    """
    class Meta:
        model = User
        fields = ['avatar']