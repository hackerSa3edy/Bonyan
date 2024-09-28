from django.shortcuts import render, redirect

def login_view(request):
    """
    Handles the login view.

    If the user is authenticated, they are redirected to the dashboard.
    If the user is not authenticated, the login page is rendered.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: A redirect to the dashboard if the user is authenticated.
        HttpResponse: The rendered login page if the user is not authenticated.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')  # Replace 'dashboard' with the actual name of your dashboard URL pattern
    return render(request, 'login.html')