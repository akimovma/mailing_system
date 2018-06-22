import calendar
import datetime

from django.db import models
from django.urls import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _

from post_office import mail
from post_office.models import EmailTemplate

import logging

from mailing_system.models import TimeStampedModel

logger = logging.getLogger(__name__)


class EmailTask(TimeStampedModel):
    ONCE = 'once'
    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'

    FREQUENCY_CHOICES = (
        (ONCE, _('Один раз')),
        (DAILY, _('Каждый день')),
        (WEEKLY, _('Каждую неделю')),
        (MONTHLY, _('Каждый месяц')),
    )

    name = models.CharField(
        _('Название рассылки'),
        max_length=255,
        help_text=_("пример: Недельная рассылка о главном"))

    last_send = models.DateField(null=True, blank=True)

    frequency = models.CharField(
        choices=FREQUENCY_CHOICES,
        default=ONCE,
        null=False,
        blank=False,
        max_length=20,
        help_text=_('Как часто будет срабатывать рассылка.'))

    start_date = models.DateField(_('Дата начала рассылки'))

    paused = models.BooleanField(default=False)

    stopped = models.BooleanField(default=False)

    sent = models.IntegerField(default=0)

    description = models.TextField(blank=True, verbose_name=_("Описание"))

    template = models.ForeignKey(EmailTemplate,
                                 on_delete=models.DO_NOTHING,
                                 related_name='tasks',
                                 verbose_name=_('Email шаблон'))

    def perform_task(self):
        logger.info(f'Found email task. ID - {self.id}')
        # get recipients for the task
        recipients = ['temp@temp.ru', 'test@tes.test']
        # just return if we don't have recipients
        if not recipients:
            return
        # we need to check if the template exists, if no just return and
        # log the error
        if not self.template:
            logger.error(f'There is no template for task - {self.id}')
            return
        # make emails list
        mails = [r for r in recipients]
        # send all of them
        mail.send(mails, self.template)
        # override the last count of sent emails
        self.sent = len(mails)
        self.last_send = datetime.date.today()
        # if this task has frequency ONCE we need to stop that.
        if self.frequency == self.ONCE:
            self.stop()
        self.save()

    def next_month(self, date, months=0):
        month_range = calendar.monthrange(date.year, date.month)[1]
        month = datetime.timedelta(days=month_range)
        next_date = date + month
        return self.next_month(next_date, months - 1) if months else next_date

    def pause(self):
        """
        Pause/Resume mailing
        """
        self.paused = not self.paused
        self.save()

    @property
    def ready_for_send(self):
        time_factor = {
            'daily': lambda date: date + datetime.timedelta(days=1),
            'weekly': lambda date: date + datetime.timedelta(days=7),
            'monthly': lambda date: self.next_month(date),
        }
        if not self.last_send:
            return datetime.date.today() == self.start_date
        next_send = time_factor[self.frequency](self.last_send)
        return next_send <= datetime.date.today()

    def __str__(self):
        return self.name

    def stop(self):
        """
        stop the email task
        """
        self.stopped = True
        self.save()

    def get_absolute_url(self):
        return reverse('tasks_detail', args=[str(self.id)])
