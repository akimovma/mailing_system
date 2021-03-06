import logging
import datetime

from django.db import models
from django.urls import reverse
from post_office import mail
from post_office.models import EmailTemplate

from mailing.utils import next_month
from mailing.managers import TaskManager, ActiveManager
from mailing_system.common.models import TimeStampedModel

from django.utils.translation import ugettext_lazy as _

logger = logging.getLogger(__name__)


class EmailTask(TimeStampedModel):
    ONCE = "once"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"

    FREQUENCY_CHOICES = (
        (ONCE, _("Один раз")),
        (DAILY, _("Каждый день")),
        (WEEKLY, _("Каждую неделю")),
        (MONTHLY, _("Каждый месяц")),
    )

    name = models.CharField(
        _("Название рассылки"),
        max_length=255,
        help_text=_("пример: Недельная рассылка о главном"),
    )

    last_send = models.DateField(null=True, blank=True)

    frequency = models.CharField(
        choices=FREQUENCY_CHOICES,
        default=ONCE,
        null=False,
        blank=False,
        max_length=20,
        help_text=_("Как часто будет срабатывать рассылка."),
    )

    start_date = models.DateField(_("Дата начала рассылки"))

    paused = models.BooleanField(default=False)

    stopped = models.BooleanField(default=False)

    sent = models.IntegerField(default=0, verbose_name=_("Всего отправлено"))

    description = models.TextField(blank=True, verbose_name=_("Описание"))

    template = models.ForeignKey(
        EmailTemplate,
        on_delete=models.DO_NOTHING,
        related_name="tasks",
        verbose_name=_("Email шаблон"),
    )

    objects = TaskManager()
    active_objects = ActiveManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("task_detail", args=[str(self.id)])

    def perform_task(self):
        logger.info(f"Found email task. ID - {self.id}")
        # get recipients for the task
        recipients = ["temp@temp.ru", "test@tes.test"]
        # just return if we don't have recipients
        if not recipients:
            return
        # we need to check if the template exists, if no just return and
        # log the error
        if not self.template:
            logger.error(f"There is no template for task - {self.id}")
            return
        # make emails list
        # mails = [r for r in recipients]
        # send all of them
        mail.send(recipients, self.template)
        # override the last count of sent emails
        self.sent = self.sent + len(recipients)
        self.last_send = datetime.date.today()
        # if this task has frequency ONCE we need to stop that.
        self.check_once_frequency()
        self.save()

    def pause(self):
        """
        Pause/Resume mailing
        """
        self.paused = not self.paused
        self.save()

    @property
    def ready_for_send(self):
        if not self.active:
            return False
        if not self.last_send:
            return datetime.date.today() == self.start_date
        return self.next_send() <= datetime.date.today()

    def stop(self):
        """
        stop the email task
        """
        self.stopped = True
        self.save()

    @property
    def human_read_status(self):
        if self.stopped:
            return "Остановлен"
        return "На паузе" if self.paused else "Активен"

    def check_once_frequency(self):
        if self.frequency == self.ONCE:
            self.stop()

    @property
    def active(self):
        return not self.stopped and not self.paused

    @property
    def next_send(self):
        time_factor = {
            "daily": lambda date: date + datetime.timedelta(days=1),
            "weekly": lambda date: date + datetime.timedelta(days=7),
            "monthly": lambda date: next_month(date),
        }
        return time_factor[self.frequency](self.last_send)
