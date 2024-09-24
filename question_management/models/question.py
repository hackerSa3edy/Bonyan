from django.db import models
from quiz_management.models import Quiz
import uuid

class Question(models.Model):

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
        return f"Question for {self.quiz.title}"