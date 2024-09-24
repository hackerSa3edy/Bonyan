from rest_framework import viewsets, permissions
from quiz_participation.models import UserAnswer
from quiz_participation.serializers import UserAnswerSerializer

class UserAnswerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserAnswer.objects.all()
    serializer_class = UserAnswerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserAnswer.objects.filter(quiz_attempt__user=self.request.user)