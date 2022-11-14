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


class CreateProjectReqSchema(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    sentences = serializers.CharField(max_length=4096)  # about 4KB

    def validate_title(self, project_title: str):
        return _validate_title(project_title)


class UpdateAudioReqSchema(serializers.Serializer):
    text = serializers.CharField(max_length=255)
    speed = serializers.IntegerField()

    def validate_speed(self, speed: int):
        if speed > 0:
            return speed
        else:
            raise serializers.ValidationError("speed must be bigger than 0")


class CreateAudioReqSchema(serializers.Serializer):
    project_id = serializers.IntegerField(allow_null=False)
    index = serializers.IntegerField(allow_null=False)  # 몇 번째 문장인지 나타내는 인덱스
    text = serializers.CharField(max_length=255, allow_null=False)  # 오디오의 텍스트 내용
    speed = serializers.IntegerField(allow_null=False)  # 재생 속도


class GetPageResponseSchema(serializers.Serializer):
    cnt = serializers.IntegerField(allow_null=False)
    page = AudioSerializer(many=True)


class IsSuccessResSchema(serializers.Serializer):
    is_success = serializers.BooleanField()
