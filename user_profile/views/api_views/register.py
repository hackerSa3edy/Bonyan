from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from user_profile.tasks import send_activation_email, delete_user_and_token
from django.conf import settings
from user_profile.serializers import UserSerializer
from user_profile.models import ActivationToken
from django.utils import timezone

User = get_user_model()

class UserRegisterView(generics.CreateAPIView):
    """
    API view for user registration.

    This view allows any user to register by creating a new User instance.
    It uses the UserSerializer to validate and save the user data.
    Upon successful registration, an activation email is sent to the user,
    and a task is scheduled to delete the user and token if not activated within 30 minutes.

    Attributes:
        queryset (QuerySet): The queryset of all User instances.
        permission_classes (tuple): The permission classes for the view.
        serializer_class (class): The serializer class used for validating and saving user data.
    """
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        """
        Performs the creation of a new User instance.

        This method saves the user data, creates an activation token, sends an activation email,
        and schedules a task to delete the user and token if not activated within 30 minutes.

        Args:
            serializer (UserSerializer): The serializer instance containing validated user data.

        Returns:
            None
        """
        user = serializer.save()

        # Create an activation token with a 30-minute expiry
        token = ActivationToken.objects.create(user=user, token_expiry=timezone.now() + timezone.timedelta(minutes=30))
        activation_link = f"{settings.FRONTEND_URL}/activate/{token.token}"

        # Call the Celery task to send the activation email
        send_activation_email.delay(user.first_name, user.email, activation_link)

        # Schedule the task to delete the user and token after 30 minutes
        delete_user_and_token.apply_async(args=[token.token], countdown=1800)