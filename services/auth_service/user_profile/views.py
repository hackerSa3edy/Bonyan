from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from .tasks import send_activation_email
from django.conf import settings
from .serializers import UserSerializer
from .models import ActivationToken

User = get_user_model()

class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()

        token = ActivationToken.objects.create(user=user)
        activation_link = f"{settings.FRONTEND_URL}/activate/{token.token}"
        
        # Call the Celery task
        send_activation_email.delay(user.id, activation_link)

class UserActivationView(generics.GenericAPIView):
    permission_classes = (AllowAny,)

    def get(self, request, token):
        try:
            activation_token = ActivationToken.objects.get(token=token)
            user = activation_token.user
            if not user.is_active:
                user.is_active = True
                user.save()
                activation_token.delete()  # Remove the token after successful activation
                return Response({"detail": "Account activated successfully."}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Account is already activated."}, status=status.HTTP_400_BAD_REQUEST)
        except ActivationToken.DoesNotExist:
            return Response({"detail": "Invalid activation token."}, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user