import pytest
from audio.services import audio_service
from django.conf import settings
from rest_framework.serializers import ValidationError
from exceptions import InvalidRequestError
from audio.repositories import audio_repo


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


@pytest.mark.django_db()
def test_find_project_page():
    sut = audio_service.find_project_page(40, 10)
    assert len(sut) <= audio_service.page_setence_count


invalid_find_project_page_params = [
    {"project_id": 1000000000, "page": 1},  # not exist project
    # {"project_id": 40, "page": 5000},  # bigger than project's last page
]


@pytest.mark.django_db()
@pytest.mark.parametrize("input", invalid_find_project_page_params)
def test_find_project_page_with_invalid_params(input):
    # with pytest.raises(InvalidRequestError):
    audio_service.find_project_page(**input)


@pytest.mark.django_db()
def test_create_audio_at_end():
    sut = audio_service.create_audio(
        **{"project_id": 40, "index": -1, "text": "text" * 20, "speed": 1}
    )
    assert isinstance(sut, dict)
    last_index = audio_repo.get_last_index(40)
    assert last_index == sut["index"]


@pytest.mark.django_db()
def test_create_audio_with_specific_index():
    last_index = audio_repo.get_last_index(40)
    sut = audio_service.create_audio(
        **{"project_id": 40, "index": 1, "text": "text" * 20, "speed": 1}
    )
    assert isinstance(sut, dict)
    assert sut["index"] == 1
    assert last_index + 1 == audio_repo.get_last_index(40)


@pytest.mark.django_db()
def test_get_mp3_file():
    sut = audio_service.get_mp3_file(171)
    assert sut
