from django.db import models
from user_profile.models import User
from .quiz import Quiz
import uuid

class QuizAssignment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='assignments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_quizzes')
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('quiz', 'user')

    def __str__(self):
        return f"{self.quiz.title} assigned to {self.user.username}"