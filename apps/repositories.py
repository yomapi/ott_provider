from rest_framework.serializers import ModelSerializer
from apps.models import BaseModel
from typing import Union


class BaseRepo:
    def __init__(self, model: BaseModel, serializer: ModelSerializer):
        self.model = model
        self.serializer = serializer

    def _get_instance(self, id: int) -> Union[BaseModel, None]:
        try:
            return self.model.objects.get(id=id)
        except self.model.DoesNotExist:
            return None

    def get(self, id: int) -> Union[dict, None]:
        instance = self._get_instance(id)
        if instance == None:
            return instance
        else:
            return self.serializer(instance).data
