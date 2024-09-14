from celery import shared_task
from django.core.mail import EmailMessage
from django.conf import settings

@shared_task
def send_activation_email(user_id, activation_link):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    user = User.objects.get(id=user_id)
    
    email = EmailMessage(
        'Activate your account',
        f'Click this link to activate your account: {activation_link}',
        settings.EMAIL_HOST_USER,
        [user.email],
    )
    email.send(fail_silently=False)