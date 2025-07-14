from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from . import managers


class User(AbstractUser):
    objects = managers.UserObjectManager()
    public_id = models.UUIDField(default=uuid4, editable=False)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
