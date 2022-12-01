from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, UpdateView, \
    DeleteView, DetailView
from django_filters.views import FilterView

from task_manager.tasks.filters import TaskFilter
from task_manager.tasks.forms import CreateTaskForm
from task_manager.tasks.models import Task


class TaskListView(FilterView):
    """
    View to get all the available tasks
    """
    model = Task
    template_name = 'tasks/main.html'
    context_object_name = 'tasks'
    filterset_class = TaskFilter


class TaskDetailView(DetailView):
    """
    View to get a single task
    """
    model = Task
    template_name = 'tasks/detail.html'
    context_object_name = 'task'


class TaskCreateView(CreateView, SuccessMessageMixin):
    """
    View to create some tasks
    """
    model = Task
    form_class = CreateTaskForm
    template_name = 'tasks/create.html'
    success_message = _('Task successfully created!')
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        current_user = self.request.user
        form.instance.author = current_user
        return super(TaskCreateView, self).form_valid(form)


class TaskUpdateView(UpdateView, SuccessMessageMixin):
    """
    Updating a task
    """
    model = Task
    form_class = CreateTaskForm
    template_name = 'tasks/edit.html'
    success_message = _('Task successfully updated!')
    success_url = reverse_lazy('tasks')


class TaskDeleteView(DeleteView, SuccessMessageMixin):
    """
    Deleting a task
    """
    model = Task
    template_name = 'tasks/delete.html'
    success_message = _('Task successfully deleted!')
    success_url = reverse_lazy('tasks')
