from django.db import models
from user_profile.models import User
from ..permissions import QuizPermissionsMixin
import uuid

class Quiz(models.Model, QuizPermissionsMixin):
    """
    Model representing a quiz.

    Attributes:
        id (UUIDField): Primary key for the quiz, generated using UUID.
        title (CharField): The title of the quiz.
        description (TextField): A description of the quiz, can be blank.
        creator (ForeignKey): Foreign key to the User model, representing the creator of the quiz.
        start_time (DateTimeField): The start time of the quiz, can be null or blank.
        end_time (DateTimeField): The end time of the quiz, can be null or blank.
        is_published (BooleanField): Indicates whether the quiz is published.
        view_after_end (BooleanField): Indicates whether the quiz can be viewed after it ends.
        show_score (BooleanField): Indicates whether the score should be shown after the quiz.
        allow_pdf_download (BooleanField): Indicates whether PDF download is allowed.
        created_at (DateTimeField): The date and time when the quiz was created.
        updated_at (DateTimeField): The date and time when the quiz was last updated.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_quizzes')
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    is_published = models.BooleanField(default=False)
    view_after_end = models.BooleanField(default=False)
    show_score = models.BooleanField(default=True)
    allow_pdf_download = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Returns a string representation of the quiz.

        Returns:
            str: The title of the quiz.
        """
        return self.title