from django.db import models
from django.utils import timezone
from .quiz_attempts import QuizAttempt
import uuid

class Result(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quiz_attempt = models.OneToOneField(QuizAttempt, on_delete=models.CASCADE, related_name='result')
    score = models.DecimalField(max_digits=5, decimal_places=2)
    total_questions = models.IntegerField()
    correct_answers = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Result for {self.quiz_attempt.user.username} on {self.quiz_attempt.quiz.title}"