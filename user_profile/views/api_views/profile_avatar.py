from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth import get_user_model
from user_profile.serializers import UserAvatarSerializer
from PIL import Image
from django.core.exceptions import ValidationError
import io

User = get_user_model()

def validate_image(image):
    """
    Validates the uploaded image.

    This function checks if the image size is within the 5MB limit and verifies if the file is a valid image.

    Args:
        image (InMemoryUploadedFile): The uploaded image file.

    Raises:
        ValidationError: If the image size exceeds 5MB or if the file is not a valid image.
    """
    if image.size > 5 * 1024 * 1024:  # 5MB limit
        raise ValidationError("Image file too large ( > 5MB )")
    try:
        img = Image.open(image)
        img.verify()
    except:
        raise ValidationError("Invalid image file")

class ProfilePictureView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, and deleting the authenticated user's profile picture.

    This view allows the authenticated user to retrieve their profile picture, update it with a new image,
    and delete the existing profile picture.

    Attributes:
        queryset (QuerySet): The queryset of all User instances.
        serializer_class (Serializer): The serializer class used for serializing User instances.
        parser_classes (tuple): The tuple of parsers used to handle file uploads.
        permission_classes (list): The list of permission classes required to access this view.
    """
    queryset = User.objects.all()
    serializer_class = UserAvatarSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """
        Retrieves the authenticated user.

        This method overrides the default get_object method to return the currently authenticated user.

        Returns:
            User: The authenticated user.
        """
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieves the authenticated user's profile picture.

        This method returns the serialized data of the authenticated user's profile picture.

        Args:
            request (Request): The HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: The HTTP response containing the serialized user data.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """
        Updates the authenticated user's profile picture.

        This method updates the user's profile picture with a new image, validates the image,
        processes it (resizes to max 300x300), and saves it.

        Args:
            request (Request): The HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: The HTTP response containing the updated user data or an error message.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        avatar = request.data.get('avatar')
        if avatar:
            try:
                validate_image(avatar)
                # Process image
                img = Image.open(avatar)
                img.thumbnail((300, 300))  # Resize to max 300x300
                buffer = io.BytesIO()
                img.save(buffer, format='PNG')
                avatar.file = buffer
                avatar.name = f"{instance.id}_avatar.png"
            except ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if instance.avatar:
            instance.avatar.delete()

        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Deletes the authenticated user's profile picture.

        This method deletes the user's existing profile picture and updates the user instance.

        Args:
            request (Request): The HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: The HTTP response indicating the result of the delete operation.
        """
        instance = self.get_object()
        if instance.avatar:
            instance.avatar.delete()
            instance.avatar = None
            instance.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "No profile picture to delete."}, status=status.HTTP_400_BAD_REQUEST)