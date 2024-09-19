from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from user_profile.tasks import send_activation_email, delete_user_and_token, send_account_activated_email
from django.conf import settings
from user_profile.serializers import UserSerializer
from user_profile.models import ActivationToken
from django.utils import timezone

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
        send_activation_email.delay(user.first_name, user.email, activation_link)

        # Schedule the task to delete the user and token after 30 minutes
        delete_user_and_token.apply_async(args=[token.token], countdown=1800)

class UserActivationView(generics.GenericAPIView):
    permission_classes = (AllowAny,)

    def get(self, request, token):
        try:
            activation_token = ActivationToken.objects.get(token=token)
            user = activation_token.user
            if activation_token.token_expiry < timezone.now():
                activation_token.delete()
                user.delete()
                return Response({"detail": "Activation token has expired. Register again."}, status=status.HTTP_410_GONE)
            if not user.is_active:
                user.is_active = True
                user.save()
                activation_token.delete()  # Remove the token after successful activation

                send_account_activated_email.delay(user.first_name, user.email)  # Send an email to the user to notify them that their account has been activated

                return Response({"detail": "Account activated successfully."}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Account is already activated."}, status=status.HTTP_409_CONFLICT)
        except ActivationToken.DoesNotExist:
            return Response({"detail": "Invalid activation token."}, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user