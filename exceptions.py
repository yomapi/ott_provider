from rest_framework import status


class InvalidRequestError(Exception):
    def __init__(self, msg="invalid reuest params", *args, **kwargs) -> None:
        self.status = status.HTTP_400_BAD_REQUEST
        super().__init__(msg, *args, **kwargs)


class AudioFileNotReadyError(Exception):
    def __init__(
        self, msg="audio file is not ready. please try agian later.", *args, **kwargs
    ) -> None:
        self.status = status.HTTP_202_ACCEPTED
        super().__init__(msg, *args, **kwargs)


class NotFoundUserError(Exception):
    def __init__(
        self, msg="User Not Found. Please Check ID or Password", *args, **kwargs
    ) -> None:
        self.status = status.HTTP_400_BAD_REQUEST
        super().__init__(msg, *args, **kwargs)


class NotAuthorizedError(Exception):
    def __init__(self, msg="Login Required", *args, **kwargs):
        self.status = status.HTTP_403_FORBIDDEN
        super().__init__(msg, *args, **kwargs)


class NoPermssionError(Exception):
    def __init__(
        self, msg="Not allowed request. Please check your permission", *args, **kwargs
    ):
        self.status = status.HTTP_403_FORBIDDEN
        super().__init__(msg, *args, **kwargs)


class TokenExpiredError(Exception):
    def __init__(self, msg="Login time expired. Please login again", *args, **kwargs):
        self.status = status.HTTP_403_FORBIDDEN
        super().__init__(msg, *args, **kwargs)
