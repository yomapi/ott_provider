from django.http import JsonResponse
from utils.auth_provider import auth_provider
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from user.service import user_service
from user.serializers import UserSignUpSchema


@api_view(["POST"])
@parser_classes([JSONParser])
def login(request):
    email = request.data["email"]
    password = request.data["password"]
    auth_token = auth_provider.login(email, password)
    return JsonResponse(auth_token, status=status.HTTP_201_CREATED)


@api_view(["POST"])
@parser_classes([JSONParser])
def signup(request):
    params = request.data
    params = UserSignUpSchema(data=params)
    params.is_valid(raise_exception=True)
    created_user = user_service.create(**params.data)
    return JsonResponse(created_user, status=status.HTTP_201_CREATED)
