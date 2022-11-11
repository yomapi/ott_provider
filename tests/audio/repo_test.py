import pytest
from audio.repositories import project_repo, audio_repo
from django.conf import settings


@pytest.fixture(scope="session")
def django_db_setup():
    settings.DATABASES


@pytest.mark.django_db()
def test_create_project():
    sut = project_repo.create("플젝1")
