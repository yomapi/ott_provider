import uuid
import logging

from utils.text.tts_provider import tts_provider
from utils.filesystem_handler import create_folder
from audio.repositories import audio_repo
from django.conf import settings
from audio.services import audio_service


def _create_sentence_mp3(sentence: str, project_id: int) -> str:
    """
    문장과 project id를 받아서 해당 mp3 파일을 만들고 그 경로를 return 합니다
    """
    path = audio_service.get_project_mp3_file_path(project_id)
    create_folder(path)
    file_path = f"{path}/{uuid.uuid4()}.mp3"
    tts_provider.text_to_mp3(sentence=sentence, filename=file_path)
    return file_path


def _save_mp3_and_set_path(audio_data: dict) -> dict:
    """
    audio 데이터를 받아서, 해당 audio의 mp3 파일을 생성하고,
    update할 데이터를 dictionary로 return
    """
    file_path = _create_sentence_mp3(audio_data["text"], audio_data["project"])
    project_id = audio_data["project"]
    del audio_data["project"]
    return {
        **audio_data,
        "path": file_path,
        "is_audio_required": False,
        "project_id": project_id,  # orm 사용시, project에 Project 인스턴스를 넣어주거나 project id 값 지정
    }


def save_mp3_and_bulk_update_audio() -> None:
    """
    DB에서 지정한 batch size 만큼, mp3 생성이 필요한 audio를 가져옵니다.
    mp3 파일 생성 후, audio를 bulk update 해줍니다.
    """
    target_audios = audio_repo.find_order_by_update_at(
        limit=settings.CREATE_MP3_BATCH_SIZE
    )
    mp3_saved_audios = list(map(lambda x: _save_mp3_and_set_path(x), target_audios))
    audio_repo.bulk_update(mp3_saved_audios, ["path", "is_audio_required"])
    return
