from audio.models import Audio, Project
from rest_framework import serializers


def _validate_title(project_title: str):
    if len(project_title) > 0:
        return project_title
    else:
        raise serializers.ValidationError(
            "Project title must be lonnger than 1 character"
        )


class ProjectSerializer(serializers.ModelSerializer):
    def validate_project_title(self, project_title: str):
        return _validate_title(project_title)

    class Meta:
        model = Project
        fields = "__all__"


class AudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audio
        fields = "__all__"


class CreateProjectSchema(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    sentences = serializers.CharField(max_length=4096)  # about 4KB

    def validate_title(self, project_title: str):
        return _validate_title(project_title)
