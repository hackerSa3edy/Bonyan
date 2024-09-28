from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from quiz_management.models import Quiz, QuizAssignment
from quiz_management.serializers import QuizSerializer, QuizAssignmentSerializer

class QuizViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing quiz instances.

    This viewset provides `list`, `create`, `retrieve`, `update`, and `destroy` actions.
    Additionally, it provides custom actions to publish, unpublish, and assign quizzes.

    Attributes:
        queryset (QuerySet): The base queryset for the viewset.
        serializer_class (Serializer): The serializer class used for the viewset.
        permission_classes (list): The list of permission classes applied to the viewset.
    """
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Return the queryset of quizzes assigned to the current user.

        This method filters the quizzes to only include those assigned to the current user.

        Returns:
            QuerySet: The filtered queryset of quizzes.
        """
        user = self.request.user
        return Quiz.objects.filter(assignments__user=user)

    def perform_create(self, serializer):
        """
        Save the new quiz instance with the current user as the creator.

        Args:
            serializer (Serializer): The serializer instance containing the validated data.
        """
        serializer.save(creator=self.request.user)

    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        """
        Publish the specified quiz.

        This custom action sets the `is_public` attribute of the quiz to True.

        Args:
            request (Request): The request object.
            pk (str): The primary key of the quiz to publish.

        Returns:
            Response: A response indicating the quiz has been published.
        """
        quiz = self.get_object()
        quiz.is_public = True
        quiz.save()
        return Response({'status': 'quiz published'})

    @action(detail=True, methods=['post'])
    def unpublish(self, request, pk=None):
        """
        Unpublish the specified quiz.

        This custom action sets the `is_public` attribute of the quiz to False.

        Args:
            request (Request): The request object.
            pk (str): The primary key of the quiz to unpublish.

        Returns:
            Response: A response indicating the quiz has been unpublished.
        """
        quiz = self.get_object()
        quiz.is_public = False
        quiz.save()
        return Response({'status': 'quiz unpublished'})

    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        """
        Assign the specified quiz to a user.

        This custom action assigns the quiz to a user specified by `user_id` in the request data.
        It checks if the user has already attempted the quiz before creating the assignment.

        Args:
            request (Request): The request object.
            pk (str): The primary key of the quiz to assign.

        Returns:
            Response: A response containing the serialized assignment data or an error message.
        """
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