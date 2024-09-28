from django.shortcuts import render, redirect
from django.urls import reverse

def register_view(request):
    """
    Renders the registration view.

    This view checks if the user is authenticated. If the user is authenticated,
    they are redirected to the dashboard. If the user is not authenticated, the
    registration template is rendered.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered registration template if the user is not authenticated.
        HttpResponseRedirect: A redirect to the dashboard if the user is authenticated.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')  # Replace 'dashboard' with the actual name of your dashboard URL pattern
    return render(request, 'register.html')

def account_activation_view(request):
    """
    Renders the account activation view.

    This view checks if the user is authenticated. If the user is authenticated,
    they are redirected to the dashboard. If the user is not authenticated, the
    account activation template is rendered.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered account activation template if the user is not authenticated.
        HttpResponseRedirect: A redirect to the dashboard if the user is authenticated.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')  # Replace 'dashboard' with the actual name of your dashboard URL pattern
    return render(request, 'account_activation.html')

def activated_view(request, token):
    """
    Renders the account activated view.

    This view checks if the user is authenticated. If the user is authenticated,
    they are redirected to the dashboard. If the user is not authenticated, the
    account activated template is rendered.

    Args:
        request (HttpRequest): The HTTP request object.
        token (str): The activation token.

    Returns:
        HttpResponse: The rendered account activated template if the user is not authenticated.
        HttpResponseRedirect: A redirect to the dashboard if the user is authenticated.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')  # Replace 'dashboard' with the actual name of your dashboard URL pattern
    return render(request, 'account_activated.html')

def profile_view(request):
    """
    Renders the profile view.

    This view checks if the user is authenticated. If the user is not authenticated,
    they are redirected to the login page. If the user is authenticated, the profile
    template is rendered.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered profile template if the user is authenticated.
        HttpResponseRedirect: A redirect to the login page if the user is not authenticated.
    """
    # Uncomment the following lines to enable authentication check
    # if not request.user.is_authenticated:
    #     return redirect(reverse('authentication-web:login'))  # Replace 'login' with the actual name of your login URL pattern
    return render(request, 'profile.html')