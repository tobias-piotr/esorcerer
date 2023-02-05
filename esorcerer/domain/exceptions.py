from typing import Any

from fastapi import status


class DomainError(Exception):
    """Domain error processable by the exception handlers."""

    status_code: int
    detail: str

    def __init__(self, status_code: int | None = None, detail: Any = None) -> None:
        if status_code is not None:
            self.status_code = status_code
        if detail is not None:
            self.detail = detail


class NotFoundError(DomainError):
    """Error for missing entries."""

    status_code = status.HTTP_404_NOT_FOUND
    detail = "Entry not found"
