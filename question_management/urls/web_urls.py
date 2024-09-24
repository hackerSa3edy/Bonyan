from django.urls import path
from question_management.views import quizPage_view


app_name = 'question_management-web'  # Namespace for the app

urlpatterns = [
    # Web: Include the URL for the quiz page
    path('quizzes/<uuid:token>/', quizPage_view, name='quiz-page'),
]