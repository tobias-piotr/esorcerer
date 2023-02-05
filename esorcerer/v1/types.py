import enum


class OrderingField(str, enum.Enum):
    """Ordering field."""

    CREATED_AT_ASC = "created_at"
    CREATED_AT_DESC = "-created_at"
