from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from user_profile.models.superuser import CustomUserManager
from django.utils import timezone
import uuid

# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that extends AbstractBaseUser and PermissionsMixin.

    This model represents a user in the system with fields for personal information,
    authentication, and role-based permissions. It uses a custom user manager for
    creating and managing user instances.

    Attributes:
        id (UUIDField): Primary key for the user, generated as a UUID.
        email (EmailField): Unique email address for the user.
        first_name (CharField): First name of the user.
        last_name (CharField): Last name of the user.
        bio (TextField): Short biography of the user.
        avatar (ImageField): Profile picture of the user, stored in the 'avatars/' directory.
        role (CharField): Role of the user, can be 'creator', 'resolver', or 'admin'.
        is_active (BooleanField): Indicates whether the user account is active.
        is_staff (BooleanField): Indicates whether the user has staff privileges.
        created_at (DateTimeField): Timestamp when the user account was created.
        updated_at (DateTimeField): Timestamp when the user account was last updated.
        objects (CustomUserManager): Custom manager for creating and managing user instances.
        USERNAME_FIELD (str): Field used for authentication, set to 'email'.
        EMAIL_FIELD (str): Field used for email, set to 'email'.
        REQUIRED_FIELDS (list): List of fields required for creating a user.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, max_length=100)
    first_name = models.CharField(max_length=50, null=True, blank=False)
    last_name = models.CharField(max_length=50, null=True, blank=False)
    bio = models.TextField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    role = models.CharField(max_length=10, choices=[('creator', 'Creator'), ('resolver', 'Resolver'), ('admin', 'Admin')], null=False, blank=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'role']

    def __str__(self):
        """
        Returns the string representation of the user.

        Returns:
            str: The email of the user.
        """
        return self.email

    class Meta:
        """
        Meta options for the User model.

        Attributes:
            swappable (str): Allows swapping the custom user model with another model.
            verbose_name (str): Human-readable name for the model.
            verbose_name_plural (str): Human-readable plural name for the model.
        """
        swappable = 'AUTH_USER_MODEL'
        verbose_name = 'user'
        verbose_name_plural = 'users'