from django.urls import path

from .views import IndexView, TaskDetailView, TaskListView, TemplateListView, \
    TemplateDetailView, TemplateCreateView, change_pause_status, TaskCreateView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),

    path('tasks/', TaskListView.as_view(), name='tasks_list'),
    path('tasks/create/', TaskCreateView.as_view(), name='tasks_create'),
    path('tasks/<int:pk>', TaskDetailView.as_view(), name='tasks_detail'),
    path('tasks/<int:task_id>/pause/', change_pause_status, name='tasks_pause'),

    path('templates/', TemplateListView.as_view(), name='templates_list'),
    path('templates/create/', TemplateCreateView.as_view(), name='templates_create'),

    path('templates/<int:pk>',
         TemplateDetailView.as_view(),
         name='templates_detail')
]