import pytest
from audio.services import audio_service
from django.conf import settings
from rest_framework.serializers import ValidationError
from audio.repositories import audio_repo
from user.service import user_service
from tests.utils.test_text import test_text
from exceptions import InvalidRequestError


@pytest.fixture(scope="session")
def django_db_setup():
    settings.DATABASES


def _create_new_user():
    return user_service.create("test1@test.com", "test1234!", "test")


def _setup_database():
    create_user = _create_new_user()
    project = audio_service.create_project_with_sentences(
        "플젝1", test_text, create_user["id"]
    )["project"]
    return create_user, project


@pytest.mark.django_db()
def test_create_project():
    new_user = _create_new_user()

    sut = audio_service.create_project_with_sentences(
        "플젝1", "나는 운이 좋았지.다른 사람들은 그렇게 어려운 이별을 한다는데.", new_user["id"]
    )
    return sut


@pytest.mark.django_db()
def test_create_project_with_invalid_name():
    new_user = _create_new_user()
    with pytest.raises(ValidationError):
        audio_service.create_project_with_sentences(
            "", "나는 운이 좋았지.다른 사람들은 그렇게 어려운 이별을 한다는데.", new_user[id]
        )


@pytest.mark.django_db()
def test_find_project_page():
    new_user, new_project = _setup_database()
    sut = audio_service.find_project_page(new_project["id"], 2, new_user["id"])
    assert len(sut) <= audio_service.page_setence_count


def _get_invalid_find_project_params():
    new_user, new_project = _setup_database()
    return [
        {
            "project_id": 1000000000,
            "page": 1,
            "user_id": new_user["id"],
        },  # not exist project
        {
            "project_id": new_project["id"],
            "page": 5000,
            "user_id": new_user["id"],
        },  # bigger than project's last page
        {
            "project_id": 40,
            "page": 5000,
            "user_id": new_user["id"] + 1,
        },  # user is not owner of project
    ]


@pytest.mark.django_db()
@pytest.mark.parametrize("input", _get_invalid_find_project_params())
def test_find_project_page_with_invalid_params(input):
    with pytest.raises(InvalidRequestError):
        audio_service.find_project_page(**input)


@pytest.mark.django_db()
def test_create_audio_at_end():
    sut = audio_service.create_audio(
        **{"project_id": 40, "index": -1, "text": "text" * 20, "speed": 1, "user_id": 1}
    )
    assert isinstance(sut, dict)
    last_index = audio_repo.get_last_index(40)
    assert last_index == sut["index"]


@pytest.mark.django_db()
def test_create_audio_with_specific_index():
    project_id = 1
    last_index = audio_repo.get_last_index(project_id)
    sut = audio_service.create_audio(
        **{
            "project_id": project_id,
            "index": 1,
            "text": "text" * 20,
            "speed": 1,
            "user_id": 1,
        }
    )
    assert isinstance(sut, dict)
    assert sut["index"] == 1
    assert last_index + 1 == audio_repo.get_last_index(project_id)


@pytest.mark.django_db()
def test_get_mp3_file():
    sut = audio_service.get_mp3_file(171)
    assert sut
