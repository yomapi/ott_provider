from django.apps import AppConfig


class JobSchedulerAppConfig(AppConfig):
    name = "job_scheduler"

    def ready(self):
        from job_scheduler.scheduler import start

        start()
