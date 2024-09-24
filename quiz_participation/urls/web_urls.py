from django.urls import path
from quiz_participation.views import userDashboard_view

app_name = 'quiz_participation-web'  # Namespace for the app

urlpatterns = [
    # Web: URL for the user dashboard
    path('dashboard/', userDashboard_view, name='dashboard'),
]