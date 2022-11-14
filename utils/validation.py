from rest_framework.serializers import Serializer
from django.http import HttpRequest


def validate_req_params(request: HttpRequest, schema: Serializer) -> dict:
    params = schema(data=request.data)
    params.is_valid(raise_exception=True)
    return params.data
