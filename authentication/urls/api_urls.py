from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from authentication.views import CustomTokenObtainPairView, login_view

app_name = 'authentication-API'  # Namespace for the app

urlpatterns = [
    # URL pattern for obtaining a new token
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # URL pattern for refreshing an existing token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # URL pattern for the login view
    path('login/', login_view, name='login'),
]