from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from post_office.models import EmailTemplate

from mailing.filters import EmailTaskFilter, EmailTemplateFilter
from mailing_system.common import views as common_views
from mailing.models import EmailTask
from mailing_system.common.views import FilteredMixin


class IndexView(TemplateView):
    template_name = 'index.html'


class TaskListView(FilteredMixin, common_views.LoginRequiredListView):
    model = EmailTask
    context_object_name = 'tasks'
    template_name = 'mailing/email_task_list.html'
    paginate_by = 5
    filter_class = EmailTaskFilter


class TaskCreateView(common_views.LoginRequiredCreateView):
    model = EmailTask
    fields = ['name', 'frequency', 'start_date', 'description', 'template']
    template_name = 'mailing/email_task_form.html'

    def get_success_url(self):
        return reverse('task_list')


class TaskDetailView(common_views.LoginRequiredDetailView):
    model = EmailTask
    template_name = 'mailing/email_task_detail.html'
    context_object_name = 'email_task'


class TemplateListView(FilteredMixin, common_views.LoginRequiredListView):
    model = EmailTemplate
    template_name = 'mailing/email_template_list.html'
    context_object_name = 'email_templates'
    paginate_by = 5
    filter_class = EmailTemplateFilter


class TemplateDetailView(common_views.LoginRequiredDetailView):
    model = EmailTemplate
    template_name = 'mailing/email_template_detail.html'
    context_object_name = 'email_template'


class TemplateCreateView(common_views.LoginRequiredCreateView):
    model = EmailTemplate
    template_name = 'mailing/email_template_form.html'
    fields = ['name', 'description', 'subject', 'content', 'html_content']

    def get_success_url(self):
        return reverse('template_list')


@login_required(login_url='/accounts/login/')
def change_tasks_pause_status(request, task_id):
    """
    View for change pause status of task

    :raises: Http404 if no such task in DB
    :param task_id: The task which status would be changed
    :return: Redirects to list of tasks
    """
    task = get_object_or_404(EmailTask, id=task_id)
    if task.stopped:
        msg = 'Невозможно. Рассылка остановлена.'
        messages.error(request, msg)
        return redirect('task_list')
    task.pause()
    msg = 'Рассылка успешно поставлена на паузу.'
    if task.active:
        msg = 'Рассылка успешно снята с паузы.'
    messages.success(request, msg)
    return redirect('task_list')


@login_required(login_url='/accounts/login/')
def stop_task_activity(request, task_id):
    task = get_object_or_404(EmailTask, id=task_id)
    if not task.stopped:
        task.stop()
        msg = 'Рассылка успешно отановлена.'
        messages.success(request, msg)
    return redirect('task_list')
