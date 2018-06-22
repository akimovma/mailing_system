from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.contrib import messages
from post_office.models import EmailTemplate

from .models import EmailTask


class IndexView(TemplateView):
    template_name = 'index.html'


class TaskListView(ListView):
    model = EmailTask
    context_object_name = 'tasks'
    template_name = 'mailing/email_task_list.html'


class TaskCreateView(CreateView):
    model = EmailTask
    fields = ['name', 'frequency', 'start_date', 'description', 'template']
    template_name = 'mailing/email_task_form.html'

    def get_success_url(self):
        return reverse('tasks_list')


class TaskDetailView(DetailView):
    pass


class TemplateListView(ListView):
    model = EmailTemplate
    template_name = 'mailing/email_template_list.html'
    context_object_name = 'email_templates'


class TemplateDetailView(DetailView):
    pass


class TemplateCreateView(CreateView):
    model = EmailTemplate
    template_name = 'mailing/email_template_form.html'
    fields = ['name', 'description', 'subject', 'content', 'html_content']

    def get_success_url(self):
        return reverse('templates_list')


def change_pause_status(request, task_id):
    task = get_object_or_404(EmailTask, id=task_id)
    task.pause()
    msg = 'Рассылка успешно поставлена на паузу.'
    if not task.paused:
        msg = 'Рассылка успешно снята с паузы.'
    messages.success(request, msg)
    return redirect('tasks_detail', task_id)
