from tortoise import fields, models


class BaseModel(models.Model):
    """Base database model."""

    id = fields.UUIDField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        abstract = True


class EventModel(BaseModel):
    """Event database model."""

    type = fields.CharField(max_length=63)
    entity_id = fields.UUIDField(null=True)
    payload = fields.JSONField()


class HookModel(BaseModel):
    """Hook database model."""

    id = fields.UUIDField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    # TODO: Move those to an abstract model
    name = fields.CharField(max_length=63)
    is_active = fields.BooleanField()
    condition = fields.TextField()
    code = fields.TextField()
