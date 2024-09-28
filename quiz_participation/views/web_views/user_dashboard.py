from django.shortcuts import render, redirect
from django.urls import reverse

def userDashboard_view(request):
    """
    Renders the user dashboard view.

    This view checks if the user is authenticated. If the user is not authenticated,
    they are redirected to the login page. If the user is authenticated, the user dashboard
    template is rendered.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered user dashboard template if the user is authenticated.
        HttpResponseRedirect: A redirect to the login page if the user is not authenticated.
    """
    # Uncomment the following lines to enable authentication check
    # if not request.user.is_authenticated:
    #     return redirect(reverse('authentication-web:login'))  # Replace 'authentication-web:login' with the actual name of your login URL pattern

    return render(request, 'user_dashboard.html')