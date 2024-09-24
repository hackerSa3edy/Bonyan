from django.shortcuts import render, redirect
from django.urls import reverse

def userDashboard_view(request):
    # if not request.user.is_authenticated:
    #     return redirect(reverse('authentication-web:login'))  # Replace 'dashboard' with the actual name of your dashboard URL pattern
    return render(request, 'user_dashboard.html')