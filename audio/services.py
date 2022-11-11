from utils.text.text_handler import string_to_sentence_list
from utils.filesystem_handler import create_folder
from audio.repositories import project_repo, audio_repo
from django.conf import settings


class AudioService:
    def get_project_mp3_file_path(self, project_id: int) -> str:
        return f"{settings.MP3_ROOT_DIR}/p_{project_id}"

    def _create_project_and_project_dir(self, title: str) -> tuple[dict, int]:
        """
        새로운 project를 생성하고, 프로젝트의 mp3파일을 저장하기 위한 디렉토리를 만듭니다.
        return 값은 새로만든 프로젝트 dict, project의 id
        """
        new_project = project_repo.create(title)
        project_id = new_project["id"]
        project_audio_file_path = self.get_project_mp3_file_path(project_id)
        create_folder(project_audio_file_path)
        return new_project, new_project["id"]

    def _bulk_create_audio(
        self,
        project_id: int,
        sentences: list[str],
    ) -> None:
        """
        프로젝트 id와 문장 list를 받아 audio를 bulk create 합니다
        """
        new_audio_data = []
        cnt = 1
        for sentence in sentences:
            new_audio_data.append(
                {
                    "index": cnt,
                    "text": sentence,
                }
            )
            cnt += 1
        audio_repo.bulk_create(project_id, new_audio_data)

    def create_project_with_sentences(self, title: str, sentences: str):
        """
        프로젝트의 제목을 받아 프로젝트를 생성합니다.
        백그라운드에서 mp3를 생성할 수 있도록 flag를 하여 audio를 bulk create합니다.
        """
        sentence_list = string_to_sentence_list(sentences)
        new_project, project_id = self._create_project_and_project_dir(title)
        self._bulk_create_audio(project_id, sentence_list)
        return {"project": new_project}


audio_service = AudioService()
