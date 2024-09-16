from django.urls import path, include
from rest_framework_nested import routers
from quiz_management.views import QuizViewSet
from .views import QuestionViewSet

router = routers.SimpleRouter()
router.register(r'quizzes', QuizViewSet)

questions_router = routers.NestedSimpleRouter(router, r'quizzes', lookup='quiz')
questions_router.register(r'questions', QuestionViewSet, basename='quiz-questions')

urlpatterns = [
    path('', include(questions_router.urls)),
]