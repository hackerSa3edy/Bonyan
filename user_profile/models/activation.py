from django.db import models
from user_profile.models.profile import User
import uuid
from django.utils import timezone
from datetime import timedelta

class ActivationToken(models.Model):
    """
    Model representing an activation token for user account activation.

    This model stores the activation token, its creation time, and expiry time.
    Each token is associated with a single user and is used to verify the user's email address.

    Attributes:
        user (ForeignKey): A one-to-one relationship to the User model.
        token (UUIDField): A unique UUID token for activation.
        created_at (DateTimeField): The date and time when the token was created.
        token_expiry (DateTimeField): The date and time when the token expires.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    token_expiry = models.DateTimeField(null=False)

    def __str__(self):
        """
        Returns a string representation of the activation token.

        Returns:
            str: A string indicating the activation token for the user's email.
        """
        return f"Activation token for {self.user.email}"