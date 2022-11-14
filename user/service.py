from user.repositories import user_repo
from utils.auth_provider import auth_provider


class UserService:
    def create(self, email: str, password: str, name: str) -> dict:
        password = auth_provider.hashpw(password)
        created_user = user_repo.create(
            name=name,
            email=email,
            password=password,
        )
        return created_user


user_service = UserService()
