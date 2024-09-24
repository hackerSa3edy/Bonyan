from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from user_profile.models.superuser import CustomUserManager
from django.utils import timezone
import uuid

# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, max_length=100)
    first_name = models.CharField(max_length=50, null=True, blank=False)
    last_name = models.CharField(max_length=50, null=True, blank=False)
    bio = models.TextField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    role = models.CharField(max_length=10, choices=[('creator', 'Creator'), ('resolver', 'Resolver'), ('admin', 'Admin')], null=False, blank=False)
    # is_anonymous = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'role', 'email', 'password']

    def __str__(self):
        return self.email

    class Meta:
        swappable = 'AUTH_USER_MODEL'