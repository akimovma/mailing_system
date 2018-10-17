from django.urls import path

from .views import IndexView, TaskDetailView, TaskListView, TemplateListView, \
    TemplateDetailView, TemplateCreateView, change_tasks_pause_status, \
    TaskCreateView, stop_task_activity

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    # task urls
    path('tasks/', TaskListView.as_view(), name='task_list'),
    path('tasks/create/', TaskCreateView.as_view(), name='task_create'),
    path('tasks/<int:pk>', TaskDetailView.as_view(), name='task_detail'),
    path('tasks/<int:task_id>/pause/', change_tasks_pause_status, name='task_pause'),
    path('tasks/<int:task_id>/stop/', stop_task_activity, name='task_stop'),
    # template urls
    path('templates/', TemplateListView.as_view(), name='template_list'),
    path('templates/create/', TemplateCreateView.as_view(), name='template_create'),
    path('templates/<int:pk>', TemplateDetailView.as_view(), name='template_detail')
]
