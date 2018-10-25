from django.db import models


class TasksQueryset(models.QuerySet):
    def active(self):
        return self.filter(stopped=False, paused=False)
