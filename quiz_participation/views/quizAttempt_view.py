from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Sum
from ..models import QuizAttempt, UserAnswer
from ..serializers import QuizAttemptSerializer, UserAnswerSerializer, StartQuizSerializer, SubmitAnswerSerializer
from quiz_management.models import Quiz
from question_management.models import Question

class QuizAttemptViewSet(viewsets.ModelViewSet):
    queryset = QuizAttempt.objects.all()
    serializer_class = QuizAttemptSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return QuizAttempt.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def start_quiz(self, request):
        serializer = StartQuizSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        quiz_id = serializer.validated_data['quiz_id']

        try:
            quiz = Quiz.objects.get(id=quiz_id)
        except Quiz.DoesNotExist:
            return Response({"error": "Quiz not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if the quiz is available
        now = timezone.now()
        if quiz.start_time and now < quiz.start_time:
            return Response({"error": "Quiz has not started yet"}, status=status.HTTP_400_BAD_REQUEST)
        if quiz.end_time and now > quiz.end_time:
            return Response({"error": "Quiz has ended"}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new quiz attempt
        quiz_attempt = QuizAttempt.objects.create(user=request.user, quiz=quiz)
        return Response(QuizAttemptSerializer(quiz_attempt).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def submit_answer(self, request, pk=None):
        quiz_attempt = self.get_object()
        if quiz_attempt.is_completed:
            return Response({"error": "This quiz attempt has already been completed"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = SubmitAnswerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        question_id = serializer.validated_data['question_id']
        user_answer = serializer.validated_data['user_answer']

        try:
            question = Question.objects.get(id=question_id, quiz=quiz_attempt.quiz)
        except Question.DoesNotExist:
            return Response({"error": "Question not found in this quiz"}, status=status.HTTP_404_NOT_FOUND)

        # Create or update the user's answer
        user_answer_obj, created = UserAnswer.objects.update_or_create(
            quiz_attempt=quiz_attempt,
            question=question,
            defaults={'user_answer': user_answer, 'is_correct': None}  # We'll evaluate correctness when finishing the quiz
        )

        return Response(UserAnswerSerializer(user_answer_obj).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def finish_quiz(self, request, pk=None):
        quiz_attempt = self.get_object()
        if quiz_attempt.is_completed:
            return Response({"error": "This quiz attempt has already been completed"}, status=status.HTTP_400_BAD_REQUEST)

        # Mark the attempt as completed
        quiz_attempt.is_completed = True
        quiz_attempt.end_time = timezone.now()

        # Calculate the score
        total_weight = quiz_attempt.quiz.questions.aggregate(total_weight=Sum('weight'))['total_weight'] or 1
        correct_weight = 0

        for answer in quiz_attempt.answers.all():
            question = answer.question
            is_correct = answer.user_answer == question.correct_answers
            answer.is_correct = is_correct
            answer.save()
            if is_correct:
                correct_weight += question.weight

        quiz_attempt.score = (correct_weight / total_weight) * 100
        quiz_attempt.save()

        return Response(QuizAttemptSerializer(quiz_attempt).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def results(self, request, pk=None):
        quiz_attempt = self.get_object()
        if not quiz_attempt.is_completed:
            return Response({"error": "This quiz attempt has not been completed yet"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(QuizAttemptSerializer(quiz_attempt).data, status=status.HTTP_200_OK)
