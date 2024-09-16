from django.db import models
from django.utils import timezone
from user_profile.models import User
from .quiz import Quiz
from ..permissions import QuizAttemptPermissionsMixin
import uuid


class QuizAttempt(models.Model, QuizAttemptPermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_attempts')
    started_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Attempt by {self.user.username} on {self.quiz.title}"