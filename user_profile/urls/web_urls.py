from django.urls import path
from user_profile.views import register_view, account_activation_view, activated_view

app_name = 'user_profile-web'  # Namespace for the app

urlpatterns = [
    # URL pattern for the login view
    path('register/', register_view, name='register'),
    path('activation/', account_activation_view, name='activation-message'),
    path('activate/<uuid:token>/', activated_view, name='activated'),
]