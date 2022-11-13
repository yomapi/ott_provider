from typing import Union
from user.models import User as CustomUser
from user.serializers import UserSerializer
from apps.repositories import BaseRepo


class UserRepo(BaseRepo):
    def get_by_email(self, email: str) -> Union[dict, None]:
        try:
            return self.serializer(self.model.objects.get(email=email)).data
        except self.model.DoesNotExist:
            return None

    def create(self, name: str, email: str, password: str) -> dict:
        serializer = self.serializer(
            data={
                "name": name,
                "email": email,
                "password": password,
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data


user_repo = UserRepo(CustomUser, UserSerializer)
