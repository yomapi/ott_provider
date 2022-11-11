import pytest
from audio.services import audio_service
from django.conf import settings
from rest_framework.serializers import ValidationError
from job_scheduler.jobs.save_mp3_and_bulk_update_audio import (
    save_mp3_and_bulk_update_audio,
)


@pytest.fixture(scope="session")
def django_db_setup():
    settings.DATABASES


@pytest.mark.django_db()
def test_create_project():
    sut = audio_service.create_project_with_sentences(
        "플젝1", "나는 운이 좋았지.다른 사람들은 그렇게 어려운 이별을 한다는데."
    )
    return sut


@pytest.mark.django_db()
def test_create_project_with_invalid_name():
    with pytest.raises(ValidationError):
        audio_service.create_project_with_sentences(
            "", "나는 운이 좋았지.다른 사람들은 그렇게 어려운 이별을 한다는데."
        )
