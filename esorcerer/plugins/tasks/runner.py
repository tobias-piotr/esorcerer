from esorcerer.domain import tasks
from esorcerer.plugins.tasks.worker import celery_app


class CeleryTaskRunner:
    """Celery tasks executor."""

    @classmethod
    def run(cls, name: tasks.TaskName, *args, **kwargs) -> None:
        """Get task by it's name and run it."""
        task = celery_app.signature(name.value)
        task.delay(*args, **kwargs)
