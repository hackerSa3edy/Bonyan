from rest_framework import viewsets, permissions
from ..models import UserAnswer
from ..serializers import UserAnswerSerializer

class UserAnswerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserAnswer.objects.all()
    serializer_class = UserAnswerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserAnswer.objects.filter(quiz_attempt__user=self.request.user)