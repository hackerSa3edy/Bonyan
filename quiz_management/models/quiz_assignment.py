from django.db import models
from user_profile.models import User
from .quiz import Quiz
import uuid

class QuizAssignment(models.Model):
    """
    Model representing the assignment of a quiz to a user.

    Attributes:
        id (UUIDField): Primary key for the assignment, generated using UUID.
        quiz (ForeignKey): Foreign key to the Quiz model, with a CASCADE delete behavior.
        user (ForeignKey): Foreign key to the User model, with a CASCADE delete behavior.
        assigned_at (DateTimeField): The date and time when the quiz was assigned to the user.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='assignments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_quizzes')
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """
        Meta options for the QuizAssignment model.

        Attributes:
            unique_together (tuple): Ensures that each quiz can be assigned to a user only once.
        """
        unique_together = ('quiz', 'user')

    def __str__(self):
        """
        Returns a string representation of the quiz assignment.

        Returns:
            str: A string representing the quiz title and the user's email.
        """
        return f"{self.quiz.title} assigned to {self.user.email}"