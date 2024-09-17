from django.db import models
from .quiz_attempt import QuizAttempt
import uuid
from question_management.models import Question

class UserAnswer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quiz_attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_answer = models.JSONField()
    is_correct = models.BooleanField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer for {self.question} in {self.quiz_attempt}"

    class Meta:
        unique_together = ('quiz_attempt', 'question')