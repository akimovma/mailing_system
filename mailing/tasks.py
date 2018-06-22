from __future__ import absolute_import, unicode_literals

import logging

from celery import task
from .models import EmailTask

logger = logging.getLogger(__name__)


@task()
def fetch_emails():
    """
    This task searching every minute for all email templates,that can be
    performed.
    """
    logger.info('Try to find emails to send.')
    email_tasks = EmailTask.objects.all()
    for email_task in email_tasks:
        paused = email_task.paused
        stopped = email_task.stopped
        ready = email_task.ready_for_send
        if not (paused or stopped) and ready:
            email_task.perform_task()
