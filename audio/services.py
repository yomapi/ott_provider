from utils.text.text_handler import string_to_sentence_list
from utils.filesystem_handler import create_folder, open_file, delete_file, delete_dir
from audio.repositories import project_repo, audio_repo
from utils.orm_filter_mapper import QueryMapper
from utils.orm_id_suffix_handler import set_multi_foreign_key_suffix
from django.conf import settings
from exceptions import InvalidRequestError, AudioFileNotReadyError, NoPermssionError
from django.db import transaction


class AudioService:
    def __init__(self) -> None:
        self.page_setence_count = 10  # 한 페이지 당 문장 갯수

    def _validate_user_is_owner(self, data: dict, user_id_to_check: int) -> bool:
        """
        project 또는 audio의 유저가 맞는지 확인합니다.
        유저가 아닐 경우, 권한이 없다는 오류 raise
        맞으면 True return
        """
        if data["user"] == user_id_to_check:
            return True
        else:
            raise NoPermssionError()

    def _validate_user_is_owner_with_project_id(
        self, project_id: int, user_id_to_check: int
    ) -> bool:
        """
        project의 id로 프로젝트를 조회하여, 유저가 주인이 맞는지 확인합니다.
        유저가 아닐 경우, 권한이 없다는 오류 raise
        맞으면 True return
        """
        project = project_repo.get(project_id)
        if project == None:
            raise InvalidRequestError("Project not exist")
        return self._validate_user_is_owner(project, user_id_to_check)

    def _get_project_max_page(self, project_id: int):
        """
        프로젝트의 최대 페이지 갯수를 return 합니다
        """
        total_cnt = audio_repo.count_by_project_id(project_id)
        page_cnt = total_cnt // self.page_setence_count
        page_cnt = (
            page_cnt if total_cnt % self.page_setence_count == 0 else page_cnt + 1
        )
        return page_cnt

    def get_project_mp3_file_path(self, project_id: int) -> str:
        return f"{settings.MP3_ROOT_DIR}/p_{project_id}"

    def _create_project_and_project_dir(
        self, title: str, user_id: int
    ) -> tuple[dict, int]:
        """
        새로운 project를 생성하고, 프로젝트의 mp3파일을 저장하기 위한 디렉토리를 만듭니다.
        return 값은 새로만든 프로젝트 dict, project의 id
        """
        new_project = project_repo.create(title, user_id)
        project_id = new_project["id"]
        project_audio_file_path = self.get_project_mp3_file_path(project_id)
        create_folder(project_audio_file_path)
        return new_project, new_project["id"]

    def _bulk_create_audio(
        self, project_id: int, sentences: list[str], user_id: int
    ) -> None:
        """
        프로젝트 id와 문장 list를 받아 audio를 bulk create 합니다
        """
        new_audio_data = []
        cnt = 1
        for sentence in sentences:
            new_audio_data.append({"index": cnt, "text": sentence, "user_id": user_id})
            cnt += 1
        audio_repo.bulk_create(project_id, new_audio_data)

    def create_project_with_sentences(
        self, title: str, sentences: str, user_id: int
    ) -> dict:
        """
        프로젝트의 제목을 받아 프로젝트를 생성합니다.
        백그라운드에서 mp3를 생성할 수 있도록 flag를 하여 audio를 bulk create합니다.
        """
        with transaction.atomic():
            sentence_list = string_to_sentence_list(sentences)
            new_project, project_id = self._create_project_and_project_dir(
                title, user_id
            )
            self._bulk_create_audio(project_id, sentence_list, user_id)
            new_audios = audio_repo.find_by_project_id(project_id)
            return {"project": new_project, "audio": new_audios}

    def find_project_page(self, project_id: int, page: int, user_id: int) -> list[dict]:
        """
        프로젝트의 페이지를 가져옵니다.
        프로젝트의 최대 페이지를 넘긴 요청이 올 경우 error를 raise 합니다
        page는 1부터 시작합니다
        """
        self._validate_user_is_owner_with_project_id(project_id, user_id)
        last_page = self._get_project_max_page(project_id)
        if page > last_page:
            raise InvalidRequestError(
                msg=f"request page is bigger than project's max page({last_page})"
            )
        else:
            offset = (page - 1) * self.page_setence_count
            return audio_repo.find_by_project_id_with_limit(
                project_id, offset=offset, limit=self.page_setence_count
            )

    def update_audio(self, audio_id: int, text: str, speed: int, user_id: int) -> dict:
        """
        오디오의 텍스트와 스피드를 업데이트 합니다
        존재하지 않는 오디오일 경우 error를 raise 합니다.
        """
        target_audio = audio_repo.get(audio_id)
        if target_audio == None:
            raise InvalidRequestError("audio is not exist")
        self._validate_user_is_owner(target_audio, user_id)

        is_audio_required = target_audio["text"] != text  # mp3 파일을 다시 만들어야 하는지 확인
        updated_audio = audio_repo.update(
            audio_id,
            {
                "text": text,
                "speed": speed,
                "is_audio_required": is_audio_required,
            },
        )
        return updated_audio

    def _update_audios_index(
        self, project_id: int, index: int, is_increase: bool, operand_number: int = 1
    ) -> bool:
        """
        지정한 index 부터 끝까지, index 값을, operand_number 만큼 증가 시키거나 감소시킵니다.
        성공한 경우 True return
        """
        targets = audio_repo.find_by_project_id(
            project_id=project_id,
            filter_params=QueryMapper(field_name="index", operator="<=", value=index),
            order_by="-index",
        )
        update_audio_data = []
        for audio_data in targets:
            update_index = (
                audio_data["index"] + operand_number
                if is_increase
                else audio_data["index"] - operand_number
            )
            audio_data = set_multi_foreign_key_suffix(audio_data, ["user", "project"])

            update_audio_data.append(
                {
                    **audio_data,
                    "index": update_index,
                }
            )

        audio_repo.bulk_update(update_audio_data, ["index"])
        return True

    def _insert_audio_at_last_index(
        self, project_id: int, text: str, speed: int, user_id: int
    ) -> dict:
        """
        오디오를 맨 끝의 index에 생성합니다.
        생성된 오디오 정보를 dict로 return
        """
        with transaction.atomic():
            insert_index = audio_repo.get_last_index(project_id) + 1
            create_params = {
                "project": project_id,
                "index": insert_index,
                "text": text,
                "speed": speed,
                "user": user_id,
            }
            return audio_repo.create(create_params)

    def _insert_audio_and_update_indexs(
        self, project_id: int, index: int, text: str, speed: int, user_id: int
    ) -> dict:
        """
        오디오를 지정한 위치에 생성하고, 뒤로 밀려나게 되는 audio의 index를 업데이트 합니다.
        생성된 오디오 정보를 dict로 return
        """
        with transaction.atomic():
            self._update_audios_index(project_id, index, is_increase=True)
            create_params = {
                "project": project_id,
                "index": index,
                "text": text,
                "speed": speed,
                "user": user_id,
            }
            new_audio = audio_repo.create(create_params)
            return new_audio

    def create_audio(
        self, project_id: int, index: int, text: str, speed: int, user_id: int
    ) -> dict:
        """
        지정한 프로젝트에 오디오를 만듭니다.
        index를 지정한 경우 해당 index에 삽입 합니다.
        -1인 경우 인덱스를 지정하지 않은 것으로 하여, 맨 마지막에 넣습니다.
        생성한 audio를 dict로 return
        """
        self._validate_user_is_owner_with_project_id(project_id, user_id)
        if index == -1:
            return self._insert_audio_at_last_index(project_id, text, speed, user_id)
        else:
            return self._insert_audio_and_update_indexs(
                project_id, index, text, speed, user_id
            )

    def delete_audio(self, audio_id: int, user_id: int):
        """
        오디오를 지우고, index를 맞춥니다.
        """
        target = audio_repo.get(audio_id)
        if target == None:
            raise InvalidRequestError("Can not delete non exist audio")
        self._validate_user_is_owner(target, user_id)
        audio_repo.delete(target["id"])
        self._update_audios_index(target["project"], target["index"], False)
        delete_file(target["path"])
        return

    def get_mp3_file(self, audio_id: int, user_id: int):
        """
        audio의 mp3 파일을 바이너리로 열어서 return 해줍니다.
        파일이 없거나, audio가 없는 경우 error raise
        """
        audio = audio_repo.get(audio_id)
        if audio == None:
            raise InvalidRequestError("Audio not exist")
        elif audio["is_audio_required"]:
            raise AudioFileNotReadyError
        else:
            self._validate_user_is_owner(audio, user_id)
            return open_file(audio["path"])

    def _delete_project_dir(self, project_id: int):
        delete_dir(self.get_project_mp3_file_path(project_id))

    def delete_project(self, project_id: int, user_id) -> bool:
        """
        프로젝트를 삭제합니다.
        오디오는 delete on cascade로 삭제됩니다.
        프로젝트의 mp3 파일이 들어있는 디렉토리 전체를 삭제합니다.
        성공한 경우 True return
        """
        self._validate_user_is_owner_with_project_id(project_id, user_id)
        is_deleted = project_repo.delete(project_id)
        if is_deleted:
            self._delete_project_dir(project_id)
            return True
        else:
            raise InvalidRequestError("Project is not exist")


audio_service = AudioService()
