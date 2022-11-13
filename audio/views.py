from audio.services import audio_service
from audio.serializers import (
    CreateProjectReqSchema,
    UpdateAudioReqSchema,
    CreateAudioReqSchema,
    GetPageResponseSchema,
    AudioSerializer,
    IsSuccessResSchema,
)
from django.http import JsonResponse, FileResponse
from rest_framework.decorators import api_view, parser_classes
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework import status
from utils.validation import validate_req_params
from utils.auth_decorators import must_be_user
from drf_yasg.utils import swagger_auto_schema
from audio.serializers import ProjectSerializer


@swagger_auto_schema(
    method="post",
    request_body=CreateProjectReqSchema,
    responses={201: ProjectSerializer},
)
@api_view(["POST"])
@method_decorator(csrf_exempt)
@parser_classes([JSONParser])
@must_be_user()
def create_project(request):
    validated_params = validate_req_params(request, CreateProjectReqSchema)
    return JsonResponse(
        audio_service.create_project_with_sentences(
            user_id=request.user, **validated_params
        ),
        status=status.HTTP_201_CREATED,
    )


@swagger_auto_schema(
    method="get",
    responses={200: GetPageResponseSchema},
)
@api_view(["GET"])
@method_decorator(csrf_exempt)
@must_be_user()
@parser_classes([JSONParser])
def get_page(request, project_id: str, page: str):
    page = audio_service.find_project_page(
        int(project_id),
        int(page),
        user_id=request.user,
    )
    return JsonResponse({"cnt": len(page), "data": page}, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt)
@parser_classes([JSONParser])
@must_be_user()
def update_audio(request, audio_id: str):
    audio_id = int(audio_id)
    validated_params = validate_req_params(request, UpdateAudioReqSchema)
    updated = audio_service.update_audio(
        audio_id=audio_id,
        **validated_params,
        user_id=request.user,
    )
    return JsonResponse(updated, status=status.HTTP_201_CREATED)


@swagger_auto_schema(
    method="post",
    request_body=CreateAudioReqSchema,
    responses={201: AudioSerializer},
)
@api_view(["POST"])
@method_decorator(csrf_exempt)
@parser_classes([JSONParser])
@must_be_user()
def create_audio(request):
    validated_params = validate_req_params(request, CreateAudioReqSchema)
    created = audio_service.create_audio(
        **validated_params,
        user_id=request.user,
    )
    return JsonResponse(created, status=status.HTTP_201_CREATED)


@method_decorator(csrf_exempt)
@parser_classes([JSONParser])
@must_be_user()
def delete_audio(request, audio_id: str):
    audio_id = int(audio_id)
    audio_service.delete_audio(
        audio_id,
        user_id=request.user,
    )
    return JsonResponse({"is_success": True}, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@method_decorator(csrf_exempt)
@parser_classes([JSONParser])
@must_be_user()
def get_mp3_file(request, audio_id: str):
    mp3_file = audio_service.get_mp3_file(
        int(audio_id),
        user_id=request.user,
    )
    return FileResponse(mp3_file, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method="delete",
    responses={201: IsSuccessResSchema},
)
@api_view(["DELETE"])
@method_decorator(csrf_exempt)
@parser_classes([JSONParser])
@must_be_user()
def delete_project(request, project_id: str):
    project_id = int(project_id)
    is_deleted = audio_service.delete_project(
        project_id,
        user_id=request.user,
    )
    return JsonResponse({"is_success": is_deleted}, status=status.HTTP_200_OK)


class AudioDetailAPI(APIView):
    @swagger_auto_schema(
        request_body=UpdateAudioReqSchema,
        responses={201: AudioSerializer},
    )
    def post(self, request, audio_id: str):
        return update_audio(request, audio_id)

    @swagger_auto_schema(
        responses={201: IsSuccessResSchema},
    )
    def delete(self, request, audio_id: str):
        return delete_audio(request, audio_id)
