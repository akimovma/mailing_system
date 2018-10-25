from django.db import models

from mailing.querysets import TasksQueryset


class TaskManager(models.Manager):
    def get_queryset(self):
        return TasksQueryset(self.model, using=self._db)


class ActiveManager(TaskManager):
    def get_queryset(self):
        return super().get_queryset().active()
