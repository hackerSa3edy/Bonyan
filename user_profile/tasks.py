from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
from user_profile.models import ActivationToken

@shared_task
def send_activation_email(user_fname, user_email, activation_link):
    
    # Render the HTML template with dynamic data
    html_content = render_to_string('activation_email.html', {
        'activation_link': activation_link,
        'user_fname': user_fname,
        'frontend_url': settings.FRONTEND_URL,
    })
    text_content = strip_tags(html_content)

    # Create the email
    email = EmailMultiAlternatives(
        'Activate your account',
        text_content,
        settings.EMAIL_HOST_USER,
        [user_email],
    )

    email.attach_alternative(html_content, "text/html")

    # Send the email
    try:
        email.send(fail_silently=False)
    except Exception as e:
        # Log the error or handle it as needed
        print(f"Failed to send email: {e}")




@shared_task
def delete_user_and_token(token):
    try:
        activation_token = ActivationToken.objects.get(token=token)
        user = activation_token.user
        if activation_token.token_expiry < timezone.now():
            activation_token.delete()
            user.delete()
    except ActivationToken.DoesNotExist:
        pass


@shared_task
def send_account_activated_email(user_fname, user_email):
    # Render the HTML template with dynamic data
    html_content = render_to_string('activated_email.html', {
        'user_fname': user_fname,
        'login_url': f'{settings.FRONTEND_URL}/login',
        'frontend_url': settings.FRONTEND_URL,
    })
    
    # Create the plain text content
    text_content = strip_tags(html_content)
    
    # Create the email
    email = EmailMultiAlternatives(
        'Account Activated Successfully',
        text_content,
        settings.EMAIL_HOST_USER,
        [user_email],
    )
    email.attach_alternative(html_content, "text/html")
    
    # Send the email
    try:
        email.send(fail_silently=False)
    except Exception as e:
        # Log the error or handle it as needed
        pass