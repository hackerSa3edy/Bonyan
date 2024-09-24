from django.db import models
from user_profile.models.profile import User
import uuid
from django.utils import timezone
from datetime import timedelta

class ActivationToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    token_expiry = models.DateTimeField(null=False)

    def __str__(self):
        return f"Activation token for {self.user.email}"