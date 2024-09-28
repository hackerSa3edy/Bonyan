from django.db import models
from .quiz_attempt import QuizAttempt
import uuid
from question_management.models import Question

class UserAnswer(models.Model):
    """
    Model representing a user's answer to a quiz question.

    Attributes:
        id (UUIDField): Primary key for the user answer, generated using UUID.
        quiz_attempt (ForeignKey): Foreign key to the QuizAttempt model, with a CASCADE delete behavior.
        question (ForeignKey): Foreign key to the Question model, with a CASCADE delete behavior.
        user_answer (JSONField): The user's answer stored in JSON format.
        is_correct (BooleanField): Indicates whether the user's answer is correct, can be null.
        created_at (DateTimeField): The date and time when the user answer was created.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quiz_attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_answer = models.JSONField()
    is_correct = models.BooleanField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Returns a string representation of the user answer.

        Returns:
            str: A string representing the question and the quiz attempt.
        """
        return f"Answer for {self.question} in {self.quiz_attempt}"

    class Meta:
        """
        Meta options for the UserAnswer model.

        Attributes:
            unique_together (tuple): Ensures that each question in a quiz attempt can have only one user answer.
        """
        unique_together = ('quiz_attempt', 'question')