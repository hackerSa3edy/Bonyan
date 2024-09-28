from django.db import models
from user_profile.models import User
from quiz_management.permissions import QuizAttemptPermissionsMixin
from quiz_management.models import Quiz
import uuid

class QuizAttempt(models.Model, QuizAttemptPermissionsMixin):
    """
    Model representing an attempt by a user to complete a quiz.

    Attributes:
        id (UUIDField): Primary key for the attempt, generated using UUID.
        quiz (ForeignKey): Foreign key to the Quiz model, with a CASCADE delete behavior.
        user (ForeignKey): Foreign key to the User model, with a CASCADE delete behavior.
        start_time (DateTimeField): The date and time when the quiz attempt was started.
        completed_at (DateTimeField): The date and time when the quiz attempt was completed, can be null or blank.
        created_at (DateTimeField): The date and time when the quiz attempt was created.
        updated_at (DateTimeField): The date and time when the quiz attempt was last updated.
        score (DecimalField): The score achieved in the quiz attempt, can be null or blank.
        is_completed (BooleanField): Indicates whether the quiz attempt is completed.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_attempts')
    start_time = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        """
        Returns a string representation of the quiz attempt.

        Returns:
            str: A string representing the user's email and the quiz title.
        """
        return f"{self.user.email}'s attempt on {self.quiz.title}"
