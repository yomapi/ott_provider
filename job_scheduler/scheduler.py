from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from job_scheduler.jobs.save_mp3_and_bulk_update_audio import (
    save_mp3_and_bulk_update_audio,
)
from django.conf import settings


def start() -> None:
    """
    프로세스 1개, 프로세스 내의 최대 쓰레드 1개를 갖는 스케쥴러를 만듭니다.
    NOTE: job_scheduler/apps.py 에서 호출하여 사용합니다.
    """
    scheduler = BackgroundScheduler(
        {
            "apscheduler.jobstores.default": {
                "type": "sqlalchemy",
                "url": "sqlite:///jobs.sqlite",
            },
            "apscheduler.executors.default": {
                "class": "apscheduler.executors.pool:ThreadPoolExecutor",
                "max_workers": "1",
            },
            "apscheduler.executors.processpool": {
                "type": "processpool",
                "max_workers": "1",
            },
            "apscheduler.job_defaults.coalesce": "false",
            "apscheduler.job_defaults.max_instances": "1",
            "apscheduler.timezone": "Asia/Seoul",
        }
    )
    # save_mp3_and_bulk_update_audio 함수를 지정한 주기로 실행하도록 스케쥴러에 추가
    scheduler.add_job(
        save_mp3_and_bulk_update_audio,
        "interval",
        id="mp3_creator",
        replace_existing=True,
        seconds=settings.CREATE_MP3_WORKER_INTERVAL_SEC,
    )
    scheduler.start()
