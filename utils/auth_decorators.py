from functools import wraps
from utils.auth_provider import auth_provider
from exceptions import NotAuthorizedError
from rest_framework.views import APIView


def must_be_user():
    def decorator(api_func):
        @wraps(api_func)
        def _wrapped_view(request, *args, **kwargs):
            request = request.request if isinstance(request, APIView) else request
            auth_token = auth_provider.get_token_from_request(request)
            if auth_token == None:
                raise NotAuthorizedError
            user_id = auth_provider.check_auth(auth_token)
            request.user = user_id
            return api_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator
