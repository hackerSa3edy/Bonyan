from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()

class ChangePasswordView(generics.UpdateAPIView):
    """
    API view for changing the authenticated user's password.

    This view allows the authenticated user to change their password by providing the current password
    and the new password. It verifies the current password and updates the user's password if the
    verification is successful.

    Attributes:
        queryset (QuerySet): The queryset of all User instances.
        permission_classes (tuple): The tuple of permission classes required to access this view.
    """
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        """
        Updates the authenticated user's password.

        This method checks if the provided current password is correct. If it is, the user's password
        is updated to the new password. If the current password is incorrect, an error response is returned.

        Args:
            request (Request): The HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: The HTTP response indicating the result of the password change operation.
        """
        user = self.request.user
        current_password = request.data.get("current_password")
        new_password = request.data.get("new_password")

        if not user.check_password(current_password):
            return Response({"detail": "Current password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)

        user.password = make_password(new_password)
        user.save()

        return Response({"detail": "Password changed successfully."}, status=status.HTTP_200_OK)