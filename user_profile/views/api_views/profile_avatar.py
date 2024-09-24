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
    if image.size > 5 * 1024 * 1024:  # 5MB limit
        raise ValidationError("Image file too large ( > 5MB )")
    try:
        img = Image.open(image)
        img.verify()
    except:
        raise ValidationError("Invalid image file")

class ProfilePictureView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserAvatarSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
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
        instance = self.get_object()
        if instance.avatar:
            instance.avatar.delete()
            instance.avatar = None
            instance.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "No profile picture to delete."}, status=status.HTTP_400_BAD_REQUEST)