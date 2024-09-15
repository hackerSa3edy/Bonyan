from django.urls import path
from .views import UserRegisterView, UserActivationView, UserProfileView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('activate/<uuid:token>/', UserActivationView.as_view(), name='user-activate'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
]