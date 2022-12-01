from django.urls import path

from task_manager.tasks.views import TaskListView, TaskDetailView, \
    TaskCreateView, TaskUpdateView, TaskDeleteView

urlpatterns = [
    path('', TaskListView.as_view(), name='tasks'),
    path('<int:pk>/', TaskDetailView.as_view(), name='task'),
    path('create/', TaskCreateView.as_view(), name='create_task'),
    path('<int:pk>/update/', TaskUpdateView.as_view(), name='update_task'),
    path('<int:pk>/delete/', TaskDeleteView.as_view(), name='delete_task'),
]
