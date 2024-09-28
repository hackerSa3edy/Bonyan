from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom serializer for obtaining JWT tokens.
    Adds custom claims to the token.
    """

    @classmethod
    def get_token(cls, user):
        """
        Customizes the token by adding custom claims.

        Args:
            user (User): The user for whom the token is being created.

        Returns:
            token (RefreshToken): The customized token with additional claims.
        """
        token = super().get_token(user)

        # Add custom claims
        token['role'] = user.role
        # Add other custom claims as needed
        # token['custom_claim'] = 'value'

        return token