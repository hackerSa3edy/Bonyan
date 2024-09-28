from rest_framework import viewsets, permissions
from quiz_participation.models import UserAnswer
from quiz_participation.serializers import UserAnswerSerializer

class UserAnswerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for retrieving user answers.

    This ViewSet provides read-only access to user answers. It ensures that only authenticated users
    can access these actions and filters the answers to only include those related to the authenticated user.
    """
    queryset = UserAnswer.objects.all()
    serializer_class = UserAnswerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Returns the queryset of user answers for the authenticated user.

        This method filters the UserAnswer objects to only include those related to quiz attempts
        made by the authenticated user.

        Returns:
            QuerySet: The queryset of user answers for the authenticated user.
        """
        return UserAnswer.objects.filter(quiz_attempt__user=self.request.user)