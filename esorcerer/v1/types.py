import enum


class EventOrderingField(str, enum.Enum):
    """Event ordering field."""

    CREATED_AT_ASC = "created_at"
    CREATED_AT_DESC = "-created_at"
