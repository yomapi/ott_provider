from audio.models import Audio, Project
from audio.serializers import ProjectSerializer, AudioSerializer


class ProjectRepo:
    def __init__(self) -> None:
        pass

    def create(self, title: str) -> dict:
        serializer = ProjectSerializer(data={"project_title": title})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data


class AudioRepo:
    def __init__(self) -> None:
        pass

    def bulk_create(self, project_id: int, data_list: list[dict]):
        model_instances = []
        for data in data_list:
            model_instances.append(Audio(project_id=project_id, **data))

        Audio.objects.bulk_create(model_instances)
        return True

    def bulk_update(self, data_list: list[dict], fields: list[str]):
        model_instnaces = list(map(lambda x: Audio(**x), data_list))
        Audio.objects.bulk_update(model_instnaces, fields)
        return

    def find_by_project_id(self, project_id: int):
        return AudioSerializer(Audio.objects.filter(project=project_id), many=True).data

    def find_order_by_update_at(self, limit: int):
        return AudioSerializer(
            Audio.objects.filter(is_audio_required=True).order_by("updated_at")[:limit],
            many=True,
        ).data


project_repo = ProjectRepo()
audio_repo = AudioRepo()
