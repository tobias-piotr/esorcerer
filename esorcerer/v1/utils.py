from typing import Any


def dict_factory(d: list[tuple[str, Any]]) -> dict:
    """Create a dict by removing empty values."""
    return {k: v for k, v in d if v is not None}
