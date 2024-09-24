from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from user_profile.tasks import send_account_activated_email
from user_profile.models import ActivationToken
from django.utils import timezone

User = get_user_model()

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