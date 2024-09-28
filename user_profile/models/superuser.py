from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    """
    Custom manager for User model with no username field.

    This manager provides methods to create regular users and superusers.
    It ensures that the email field is set and handles the creation of users
    with specific roles and permissions.

    Methods:
        create_user: Creates and returns a regular user with the given email, first name, last name, and password.
        create_superuser: Creates and returns a superuser with the given email, first name, last name, and password.
    """

    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        """
        Creates and returns a regular user with the given email, first name, last name, and password.

        This method normalizes the email, sets the password, and saves the user instance.
        It also ensures that the email field is set and prevents non-superusers from having the 'admin' role.

        Args:
            email (str): The email address of the user.
            first_name (str): The first name of the user.
            last_name (str): The last name of the user.
            password (str, optional): The password for the user. Defaults to None.
            **extra_fields: Additional fields for the user model.

        Returns:
            User: The created user instance.

        Raises:
            ValueError: If the email field is not set or if a non-superuser tries to have the 'admin' role.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        
        # Prevent non-superuser creation with 'admin' role
        if extra_fields.get('role') == 'admin' and not extra_fields.get('is_superuser'):
            raise ValueError('Only superusers can have the admin role')
        
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        """
        Creates and returns a superuser with the given email, first name, last name, and password.

        This method sets default values for superuser-specific fields and ensures that the
        superuser has the required permissions and role.

        Args:
            email (str): The email address of the superuser.
            first_name (str): The first name of the superuser.
            last_name (str): The last name of the superuser.
            password (str, optional): The password for the superuser. Defaults to None.
            **extra_fields: Additional fields for the user model.

        Returns:
            User: The created superuser instance.

        Raises:
            ValueError: If the superuser does not have the required permissions or role.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 'admin')  # Set default role to admin for superusers

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('role') != 'admin':
            raise ValueError('Superuser must have role=admin.')

        return self.create_user(email, first_name, last_name, password, **extra_fields)