from django.db import models
from apps.models import BaseModel


class Project(BaseModel):
    project_title = models.CharField(max_length=255, null=False, default="")  # 프로젝트 이름

    class Meta:
        db_table = "project"
        abstract = False
        managed = True


class Audio(BaseModel):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        db_column="project_id",
    )
    index = models.IntegerField(null=False, default=1)  # 몇 번째 문장인지 나타내는 인덱스
    text = models.CharField(max_length=255, null=False)  # 오디오의 텍스트 내용
    speed = models.IntegerField(null=False, default=1)  # 재생 속도
    path = models.CharField(max_length=255, default="")  # 파일이 저장된 위치
    is_audio_required = models.BooleanField(default=True)  # mp3 파일을 생성 필요 flag

    class Meta:
        db_table = "audio"
        abstract = False
        managed = True
