from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet


class BaseModelViewSet(ModelViewSet):
    list_serializer_class: ModelSerializer = None

    def get_serializer_class(self):
        if self.action == "list" and self.list_serializer_class:
            return self.list_serializer_class
        return super().get_serializer_class()
