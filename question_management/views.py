from rest_framework import viewsets, permissions
from .models import Question
from .serializers import QuestionSerializer

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Question.objects.filter(quiz_id=self.kwargs['quiz_pk'])

    def perform_create(self, serializer):
        serializer.save(quiz_id=self.kwargs['quiz_pk'])