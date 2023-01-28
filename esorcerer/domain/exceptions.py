from fastapi import HTTPException


class NotFoundException(HTTPException):
    """Exception for missing entries."""
