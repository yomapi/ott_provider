from user.repositories import user_repo
import jwt
from django.conf import settings
from exceptions import (
    NotFoundUserError,
    NotAuthorizedError,
    TokenExpiredError,
)
from datetime import datetime
import bcrypt


class AuthProvider:
    def __init__(self):
        self.key = settings.JWT_KEY
        self.expire_sec = settings.JWT_EXPIRE_TIME

    def _get_curr_sec(self):
        return datetime.now().timestamp()

    def hashpw(self, password: str):
        return bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt()).decode("utf8")

    def checkpw(self, password: str, hashed: str):
        return bcrypt.checkpw(password.encode("utf8"), hashed.encode("utf8"))

    def _decode(self, token: str):
        decoded = jwt.decode(token, self.key, algorithms=["HS256"])
        if decoded["exp"] <= self._get_curr_sec():
            raise TokenExpiredError
        else:
            return decoded

    def get_token_from_request(self, request):
        return request.META.get("HTTP_AUTHORIZATION", None)

    def create_token(self, user_id: str, is_expired: bool = False) -> dict:
        exp = 0 if is_expired else self._get_curr_sec() + self.expire_sec
        encoded_jwt = jwt.encode(
            {"id": user_id, "exp": exp},
            self.key,
            algorithm="HS256",
        )
        return {"access": encoded_jwt}

    def login(self, email: str, password: str) -> dict:
        user = user_repo.get_by_email(email=email)
        if user == None:
            raise NotFoundUserError()

        if self.checkpw(password, user["password"]):
            return self.create_token(user["id"])
        else:
            raise NotFoundUserError()

    def check_auth(self, token: str) -> int:
        decoded = self._decode(token)
        user = user_repo.get(decoded["id"])
        if user:
            return user["id"]
        else:
            raise NotAuthorizedError


auth_provider = AuthProvider()
