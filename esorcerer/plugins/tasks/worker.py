from datetime import timedelta

from celery import Celery

from esorcerer.settings import settings

celery_app = Celery()
celery_app.conf.update(
    broker_url=settings.REDIS_URL,
    result_backend=settings.REDIS_URL,
)

celery_app.autodiscover_tasks(["esorcerer.plugins.tasks"])

celery_app.conf.update(
    beat_schedule={
        "health_check": {
            "task": "esorcerer.plugins.tasks.tasks.health_check",
            "schedule": timedelta(minutes=1),
        },
        "expensive_projections": {
            "task": "esorcerer.plugins.tasks.tasks.create_expensive_projections",
            "schedule": timedelta(minutes=5),
        },
    }
)
