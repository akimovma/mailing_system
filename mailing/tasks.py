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
    logger.info("Try to find emails to send.")
    email_tasks = EmailTask.objects.filter(stopped=False, paused=False).all()
    for email_task in email_tasks:
        if email_task.ready_for_send:
            email_task.perform_task()
