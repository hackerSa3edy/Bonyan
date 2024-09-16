from django.db import models
from django.utils import timezone
from .quiz_attempts import QuizAttempt
from .questions import Question
import uuid

class UserAnswer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quiz_attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name='user_answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_answer = models.JSONField()
    is_correct = models.BooleanField(null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Answer by {self.quiz_attempt.user.username} for {self.question.text[:30]}"