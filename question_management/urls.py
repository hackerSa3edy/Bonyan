from django.urls import path, include
from rest_framework_nested import routers
from quiz_management.views import QuizViewSet
from .views import QuestionViewSet

# Initialize the main router
router = routers.SimpleRouter()
router.register(r'quizzes', QuizViewSet)

# Initialize the nested router for questions
questions_router = routers.NestedSimpleRouter(router, r'quizzes', lookup='quiz')
questions_router.register(r'questions', QuestionViewSet, basename='quiz-questions')

app_name = 'question_management'  # Namespace for the app

urlpatterns = [
    # Include the nested router URLs for questions
    path('', include((questions_router.urls, 'quiz_management'), namespace='quiz-questions')),
]