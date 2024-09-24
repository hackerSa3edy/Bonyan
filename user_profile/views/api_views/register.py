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
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()

        token = ActivationToken.objects.create(user=user, token_expiry=timezone.now() + timezone.timedelta(minutes=30))
        activation_link = f"{settings.FRONTEND_URL}/activate/{token.token}"

        # Call the Celery task
        send_activation_email.delay(user.first_name, user.email, activation_link)

        # Schedule the task to delete the user and token after 30 minutes
        delete_user_and_token.apply_async(args=[token.token], countdown=1800)