from django.urls import path
from authentication.views import login_view

app_name = 'authentication-web'  # Namespace for the app

urlpatterns = [
    # URL pattern for the login view
    path('login/', login_view, name='login'),
]