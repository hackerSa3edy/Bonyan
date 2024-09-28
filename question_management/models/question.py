from django.db import models
from quiz_management.models import Quiz
import uuid

class Question(models.Model):
    """
    Model representing a question in a quiz.

    Attributes:
        QUESTION_TYPE_CHOICES (list): Choices for the type of question.
        id (UUIDField): Primary key for the question, generated using UUID.
        quiz (ForeignKey): Foreign key to the Quiz model, with a CASCADE delete behavior.
        text (TextField): The text of the question.
        type (CharField): The type of question, with choices defined in QUESTION_TYPE_CHOICES.
        weight (DecimalField): The weight of the question, used for scoring.
        options (JSONField): The options for the question, stored as JSON.
        correct_answers (JSONField): The correct answers for the question, stored as JSON.
        created_at (DateTimeField): The date and time when the question was created.
        updated_at (DateTimeField): The date and time when the question was last updated.
    """

    QUESTION_TYPE_CHOICES = [
        ('multiple choice', 'Multiple Choice'),
        ('one choice', 'One Choice'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    type = models.CharField(
        max_length=50,
        choices=QUESTION_TYPE_CHOICES,
        default='one choice',
    )
    weight = models.DecimalField(max_digits=5, decimal_places=2, default=1)
    options = models.JSONField()
    correct_answers = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Returns a string representation of the question.

        Returns:
            str: A string representing the question and its associated quiz.
        """
        return f"Question for {self.quiz.title}"