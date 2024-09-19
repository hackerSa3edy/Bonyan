from django.urls import path
from user_profile.views import UserRegisterView, UserActivationView, UserProfileView

app_name = 'user_profile-API'  # Namespace for the app

urlpatterns = [
    # URL pattern for user registration
    path('user/register/', UserRegisterView.as_view(), name='register'),
    
    # URL pattern for user activation with a token
    path('user/activate/<uuid:token>/', UserActivationView.as_view(), name='activate'),
    
    # URL pattern for user profile
    path('user/profile/', UserProfileView.as_view(), name='profile'),
]