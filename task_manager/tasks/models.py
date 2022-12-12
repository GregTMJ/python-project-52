from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from task_manager.status.models import Status
from task_manager.labels.models import Label


class Task(models.Model):
    name = models.CharField(_('name'), max_length=255, unique=True)
    description = models.TextField(_('description'), blank=True)
    executor = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
        related_name='executor',
        verbose_name=_('executor'),
        blank=True,
        null=True
    )
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
        related_name='author',
        verbose_name=_('author')
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name='status',
        verbose_name=_('status'),
        blank=True,
        null=True
    )
    labels = models.ManyToManyField(
        Label,
        through='TaskLabelRelation',
        related_name='labels',
        verbose_name=_('labels'),
        blank=True,
    )

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.name} - {self.executor} by {self.author} ' \
               f'- status {self.status}'


class TaskLabelRelation(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.CASCADE)
