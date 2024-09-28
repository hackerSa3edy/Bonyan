from rest_framework import viewsets, permissions
from question_management.models import Question
from question_management.serializers import QuestionSerializer
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from quiz_management.models import Quiz

class QuestionViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Question instances.

    This viewset provides `list`, `create`, `retrieve`, `update`, and `destroy` actions.
    It restricts access to authenticated users only.

    Attributes:
        queryset (QuerySet): The base queryset for retrieving Question instances.
        serializer_class (Serializer): The serializer class used for validating and deserializing input, and for serializing output.
        permission_classes (list): The list of permission classes that this viewset requires.
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Override the default queryset to filter questions by quiz.

        This method filters the questions to only include those that belong to the quiz specified by the `quiz_pk` URL parameter.

        Returns:
            QuerySet: The filtered queryset of Question instances.
        """
        return Question.objects.filter(quiz_id=self.kwargs['quiz_pk'])

    def perform_create(self, serializer):
        """
        Override the default create behavior to associate the question with a quiz.

        This method saves the new Question instance and associates it with the quiz specified by the `quiz_pk` URL parameter.

        Args:
            serializer (Serializer): The serializer instance containing the validated data.
        """
        serializer.save(quiz_id=self.kwargs['quiz_pk'])

def quizPage_view(request, token):
    """
    Render the quiz page.

    This view renders the `quiz_page.html` template for the quiz specified by the `token` URL parameter.
    If the quiz does not exist, it raises a 404 error.

    Args:
        request (HttpRequest): The HTTP request object.
        token (str): The token identifying the quiz.

    Returns:
        HttpResponse: The rendered `quiz_page.html` template.
    """
    # if not request.user.is_authenticated:
    #     return redirect(reverse('authentication-web:login'))

    get_object_or_404(Quiz, pk=token)
    return render(request, 'quiz_page.html')