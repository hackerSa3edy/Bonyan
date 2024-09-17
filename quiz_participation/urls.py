from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import QuizAttemptViewSet, UserAnswerViewSet

# Initialize the router
router = SimpleRouter()
router.register(r'attempts', QuizAttemptViewSet, basename='quiz-attempts')
router.register(r'answers', UserAnswerViewSet, basename='user-answers')

app_name = 'quiz_participation'  # Namespace for the app

urlpatterns = [
    # Include the router URLs under the 'participation/' path
    path('participation/', include((router.urls, 'participation'), namespace='participation')),
]