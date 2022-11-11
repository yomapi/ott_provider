from django.urls import path
from audio.views import create_project

urlpatterns = [
    path("project/", create_project),
]
