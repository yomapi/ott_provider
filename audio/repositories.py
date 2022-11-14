from audio.models import Audio, Project
from audio.serializers import ProjectSerializer, AudioSerializer
from typing import Union
from utils.orm_filter_mapper import QueryMapper, QueryMapprList
from apps.repositories import BaseRepo


class ProjectRepo(BaseRepo):
    def create(self, title: str, user_id: int) -> dict:
        serializer = ProjectSerializer(data={"project_title": title, "user": user_id})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    def delete(self, project_id: int) -> bool:
        instance = self._get_instance(project_id)
        if instance == None:
            return False
        else:
            instance.delete()
            return True


class AudioRepo(BaseRepo):
    def get_last_audio(self, project_id: int) -> Union[None, dict]:
        """
        프로젝트의 마지막 오디오를 가져옵니다.
        존재하지 않으면 None return
        """
        instance = Audio.objects.filter(project=project_id).order_by("-index").first()
        return AudioSerializer(instance).data if instance != None else None

    def get_last_index(self, project_id: int) -> Union[None, int]:
        last_audio = self.get_last_audio(project_id)
        return last_audio["index"] if last_audio != None else None

    def get_by_filter_params(self, filter_params: QueryMapprList) -> Union[dict, None]:
        """
        파라매터로 받은 조건을 만족하는 aduio 1개를 return 합니다.
        존재하지 않는 경우 None을 return
        """
        try:
            return AudioSerializer(Audio.objects.get(filter_params.query())).data
        except Audio.DoesNotExist:
            return None

    def get(self, audio_id: int) -> Union[None, dict]:
        instance = self._get_instance(audio_id)
        if instance == None:
            return instance
        else:
            return AudioSerializer(instance).data

    def delete(self, audio_id: int) -> None:
        self._get_instance(audio_id).delete()
        return

    def update(self, audio_id: int, data: dict) -> dict:
        serializer = AudioSerializer(
            self._get_instance(audio_id),
            data={
                **data,
                "id": audio_id,
            },
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    def create(self, data: dict) -> dict:
        serializer = AudioSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    def count_by_project_id(self, project_id: int) -> int:
        return Audio.objects.filter(project=project_id).count()

    def bulk_create(self, project_id: int, data_list: list[dict]) -> bool:
        model_instances = []
        for data in data_list:
            model_instances.append(Audio(project_id=project_id, **data))

        Audio.objects.bulk_create(model_instances)
        return True

    def bulk_update(self, data_list: list[dict], fields: list[str]) -> None:
        model_instnaces = list(map(lambda x: Audio(**x), data_list))
        Audio.objects.bulk_update(model_instnaces, fields)
        return

    def find_by_project_id(
        self,
        project_id: int,
        filter_params: Union[QueryMapper, None] = None,
        order_by: str = "index",
    ) -> list[dict]:
        instance = None
        if filter_params == None:
            instance = Audio.objects.filter(project=project_id).order_by(order_by)
        else:
            instance = Audio.objects.filter(
                project=project_id, **filter_params.query()
            ).order_by(order_by)
        return AudioSerializer(instance, many=True).data

    def find_by_project_id_with_limit(
        self, project_id: int, offset: int, limit: int, order_by: str = "index"
    ) -> list[dict]:
        return AudioSerializer(
            Audio.objects.filter(project=project_id).order_by(order_by)[
                offset : offset + limit
            ],
            many=True,
        ).data

    def find_order_by_update_at(self, limit: int) -> list[dict]:
        return AudioSerializer(
            Audio.objects.filter(is_audio_required=True).order_by("updated_at")[:limit],
            many=True,
        ).data


project_repo = ProjectRepo(Project, ProjectSerializer)
audio_repo = AudioRepo(Audio, AudioSerializer)
