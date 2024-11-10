from rest_framework.mixins import (
    DestroyModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from apps.users.models import User

from .serializers import UserSerializer


class UserViewSet(
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        if self.kwargs.get(self.lookup_field) == "me" and self.request.user.is_authenticated:
            self.kwargs[self.lookup_field] = self.request.user.pk
        return super().get_object()

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
