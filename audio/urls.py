from django.urls import path
from audio.views import (
    create_project,
    get_page,
    create_audio,
    AudioDetailAPI,
    get_mp3_file,
    delete_project,
)

urlpatterns = [
    path("project/", create_project),
    path("project/<project_id>", delete_project),
    path("audio/", create_audio),
    path("audio/<audio_id>", AudioDetailAPI.as_view()),
    path("audio/<audio_id>/mp3_file", get_mp3_file),
    path("project/<project_id>/page/<page>", get_page),
]
