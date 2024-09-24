from rest_framework import viewsets, permissions
from question_management.models import Question
from question_management.serializers import QuestionSerializer
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from quiz_management.models import Quiz


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Question.objects.filter(quiz_id=self.kwargs['quiz_pk'])

    def perform_create(self, serializer):
        serializer.save(quiz_id=self.kwargs['quiz_pk'])


def quizPage_view(request, token):
    # if not request.user.is_authenticated:
    #     return redirect(reverse('authentication-web:login'))

    get_object_or_404(Quiz, pk=token)
    return render(request, 'quiz_page.html')