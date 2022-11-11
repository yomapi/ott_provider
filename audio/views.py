from audio.services import audio_service
from audio.serializers import CreateProjectSchema
from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework import status


@api_view(["POST"])
@method_decorator(csrf_exempt)
@parser_classes([JSONParser])
def create_project(request):
    params = CreateProjectSchema(data=request.data)
    params.is_valid(raise_exception=True)
    return JsonResponse(audio_service.create_project_with_sentences(**params.data))
