import os, stat
import shutil
from django.conf import settings


def _get_full_path(path: str):
    return f"{settings.BASE_DIR}/{path}"


def create_folder(directory: str):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Creating directory. " + directory)


def open_file(path: str, mode: str = "rb"):
    return open(_get_full_path(path), mode)


def delete_file(path: str):
    full_path = _get_full_path(path)
    if os.path.exists(full_path):
        os.remove(full_path)


def _remove_readonly(func, path, _):
    "Clear the readonly bit and reattempt the removal"
    os.chmod(path, stat.S_IWRITE)
    func(path)


def delete_dir(path: str):
    """
    지정한 디렉토리가 존재하면 삭제합니다.
    NOTE: 디렉토리 내부에 파일이 있어도 삭제됩니다. read only 파일 또한 삭제됩니다.
    REFER: https://docs.python.org/3/library/shutil.html#rmtree-example
    """
    full_path = _get_full_path(path)
    if os.path.exists(full_path):
        shutil.rmtree(full_path, onerror=_remove_readonly)
    return
