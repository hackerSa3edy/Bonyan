from rest_framework_simplejwt.views import TokenObtainPairView
from authentication.serializers import CustomTokenObtainPairSerializer
from rest_framework.permissions import AllowAny

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = (AllowAny,)