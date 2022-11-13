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
