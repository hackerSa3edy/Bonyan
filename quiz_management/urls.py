from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import QuizViewSet

# Initialize the router
router = SimpleRouter()
router.register(r'quizzes', QuizViewSet, basename='quizzes')

app_name = 'quiz_management'  # Namespace for the app

# Manually add the URLs from the router, excluding the root view
urlpatterns = [
    # Include the router URLs under the 'quizzes/' path
    path('', include((router.urls, 'quizzes'), namespace='quizzes')),
]