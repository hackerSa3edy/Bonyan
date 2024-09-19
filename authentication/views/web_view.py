from django.shortcuts import render, redirect

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')  # Replace 'dashboard' with the actual name of your dashboard URL pattern
    return render(request, 'login.html')