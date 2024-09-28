from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from user_profile.tasks import send_account_activated_email
from user_profile.models import ActivationToken
from django.utils import timezone

User = get_user_model()

class UserActivationView(generics.GenericAPIView):
    """
    API view for activating a user's account.

    This view allows a user to activate their account using an activation token.
    It verifies the token, activates the user's account if the token is valid and not expired,
    and sends an account activation email to the user.

    Attributes:
        permission_classes (tuple): The tuple of permission classes required to access this view.
    """
    permission_classes = (AllowAny,)

    def get(self, request, token):
        """
        Handles GET requests for account activation.

        This method retrieves the activation token, checks its validity and expiry,
        activates the user's account if valid, and sends an account activation email.
        If the token is invalid or expired, it returns an appropriate error response.

        Args:
            request (Request): The HTTP request object.
            token (str): The activation token.

        Returns:
            Response: The HTTP response indicating the result of the activation process.
        """
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