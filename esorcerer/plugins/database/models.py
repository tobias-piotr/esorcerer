from tortoise import fields, models


class EventModel(models.Model):
    """Event database model."""

    id = fields.UUIDField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    type = fields.CharField(max_length=63)
    entity_id = fields.UUIDField(null=True)
    payload = fields.JSONField()
