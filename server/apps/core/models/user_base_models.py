import uuid
from django.db import models

from apps.core.models import BaseModel
from apps.user_auth.models import MTEUser


class BaseUserModel(BaseModel):

    class Meta:
        abstract = True

    user_id: uuid.UUID = models.ForeignKey(MTEUser, on_delete=models.PROTECT)
