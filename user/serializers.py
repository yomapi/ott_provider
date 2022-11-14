from user.models import User as CustomUser
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"


class UserSignUpReqSchema(serializers.Serializer):
    """
    user 회원가입 기능 요청 정의 입니다.
    """

    name = serializers.CharField(max_length=20, allow_null=False)
    email = serializers.CharField(max_length=100, allow_null=False)
    password = serializers.CharField(max_length=255, allow_null=False)


class UserLoginReqSchema(serializers.Serializer):
    """
    user 로그인 기능 요청 정의 입니다.
    """

    email = serializers.CharField(max_length=100, allow_null=False)
    password = serializers.CharField(max_length=255, allow_null=False)


class UserLoginResSchema(serializers.Serializer):
    """
    user 로그인 응답 정의 입니다.
    """

    access = serializers.CharField(max_length=124)
