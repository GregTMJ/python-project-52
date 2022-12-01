from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Label(models.Model):
    name = models.CharField(_('name'), max_length=75, unique=True)
    created_at = models.DateTimeField(_('created_at'), default=timezone.now)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name
