from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from quiz_management.models import Quiz, QuizAssignment
from quiz_management.serializers import QuizSerializer, QuizAssignmentSerializer

class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Quiz.objects.filter(assignments__user=user)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        quiz = self.get_object()
        quiz.is_public = True
        quiz.save()
        return Response({'status': 'quiz published'})

    @action(detail=True, methods=['post'])
    def unpublish(self, request, pk=None):
        quiz = self.get_object()
        quiz.is_public = False
        quiz.save()
        return Response({'status': 'quiz unpublished'})

    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        quiz = self.get_object()
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        from quiz_participation.models import QuizAttempt
        # Check if the user has already attempted the quiz
        if QuizAttempt.objects.filter(quiz=quiz, user_id=user_id).exists():
            return Response({'error': 'User has already attempted this quiz'}, status=status.HTTP_400_BAD_REQUEST)
        
        assignment, created = QuizAssignment.objects.get_or_create(quiz=quiz, user_id=user_id)
        serializer = QuizAssignmentSerializer(assignment)
        return Response(serializer.data)