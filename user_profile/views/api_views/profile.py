from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from user_profile.serializers import UserSerializer
from rest_framework import generics
from rest_framework.response import Response

User = get_user_model()

class UserProfileView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        data = request.data.copy()
        data.pop('avatar', None)  # Remove the avatar field from the data
        serializer = self.get_serializer(user, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
