import pytest
from audio.repositories import project_repo, audio_repo
from django.conf import settings
from audio.repositories import QueryMapper


@pytest.fixture(scope="session")
def django_db_setup():
    settings.DATABASES


@pytest.mark.django_db()
def test_create_project():
    sut = project_repo.create("플젝1")


@pytest.mark.django_db()
def test_get_last_index():
    sut = audio_repo.get_last_index(10000)
    assert isinstance(sut, dict)


@pytest.mark.django_db()
def test_find_by_project_id():
    audio_repo.find_by_project_id(40, QueryMapper("index", "<=", 30))
