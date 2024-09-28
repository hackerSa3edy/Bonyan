from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from user_profile.serializers import UserSerializer
from rest_framework import generics
from rest_framework.response import Response

User = get_user_model()

class UserProfileView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, and deleting the authenticated user's profile.

    This view allows the authenticated user to retrieve their profile information,
    update their profile details (excluding the avatar), and delete their profile.

    Attributes:
        queryset (QuerySet): The queryset of all User instances.
        serializer_class (Serializer): The serializer class used for serializing User instances.
        permission_classes (tuple): The tuple of permission classes required to access this view.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        """
        Retrieves the authenticated user.

        This method overrides the default get_object method to return the currently authenticated user.

        Returns:
            User: The authenticated user.
        """
        return self.request.user

    def update(self, request, *args, **kwargs):
        """
        Updates the authenticated user's profile.

        This method updates the user's profile details, excluding the avatar field.
        It validates the provided data and performs the update.

        Args:
            request (Request): The HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: The HTTP response containing the updated user data.
        """
        user = self.get_object()
        data = request.data.copy()
        data.pop('avatar', None)  # Remove the avatar field from the data
        serializer = self.get_serializer(user, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
