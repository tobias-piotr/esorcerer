import enum
from typing import Protocol


class TaskName(str, enum.Enum):
    """Task name."""

    RUN_ACTIVE_HOOKS = "run_active_hooks"


class TaskRunner(Protocol):
    """Tasks executor interface."""

    @classmethod
    def run(cls, name: TaskName, *args, **kwargs) -> None:
        """Run task by it's name."""
