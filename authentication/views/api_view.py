from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from authentication.serializers import CustomTokenObtainPairSerializer
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom view for obtaining JWT tokens.
    Uses a custom serializer to include additional user information in the token response.
    """
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = (AllowAny,)

class LogoutView(APIView):
    """
    View for logging out users by blacklisting their refresh tokens.
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        """
        Handles POST requests to blacklist the provided refresh token.
        
        Args:
            request (Request): The request object containing the refresh token in the body.
        
        Returns:
            Response: A response with status 205 if successful, or 400 if an error occurs.
        """
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)