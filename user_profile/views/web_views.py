from django.shortcuts import render, redirect

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')  # Replace 'dashboard' with the actual name of your dashboard URL pattern
    return render(request, 'register.html')

def account_activation_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')  # Replace 'dashboard' with the actual name of your dashboard URL pattern
    return render(request, 'account_activation.html')

def activated_view(request, token):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'account_activated.html')