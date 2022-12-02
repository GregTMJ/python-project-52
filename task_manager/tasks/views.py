from django.contrib import messages
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


class TaskCreateView(CreateView):
    """
    View to create some tasks
    """
    model = Task
    form_class = CreateTaskForm
    template_name = 'tasks/create.html'

    def form_valid(self, form):
        current_user = self.request.user
        form.instance.author = current_user
        messages.success(request=self.request,
                         message=_('Task successfully created!'))
        return super(TaskCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('tasks')


class TaskUpdateView(UpdateView):
    """
    Updating a task
    """
    model = Task
    form_class = CreateTaskForm
    template_name = 'tasks/edit.html'

    def form_valid(self, form):
        messages.success(request=self.request,
                         message=_('Task successfully updated!'))
        return super(TaskUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('tasks')


class TaskDeleteView(DeleteView):
    """
    Deleting a task
    """
    model = Task
    template_name = 'tasks/delete.html'

    def form_valid(self, form):
        obj = self.get_object()
        current_user = self.request.user
        if obj.author != current_user:
            messages.error(request=self.request,
                           message=_("You don't have the permission to delete!"))
            return super(TaskDeleteView, self).form_invalid(form)
        messages.success(request=self.request,
                         message=_('Task successfully deleted!'))
        return super(TaskDeleteView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('tasks')
