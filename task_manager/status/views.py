from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, UpdateView, \
    DeleteView, CreateView

from task_manager.status.models import Status
from task_manager.status.forms import StatusForm


class StatusListView(LoginRequiredMixin, ListView):
    """
    View to get all the available status
    """
    model = Status
    template_name = 'status/main.html'
    context_object_name = 'statuses'


class StatusCreateView(LoginRequiredMixin, CreateView,
                       SuccessMessageMixin):
    """
    View to create new status
    """
    model = Status
    form_class = StatusForm
    template_name = 'status/create.html'
    success_message = _('Status successfully created!')
    success_url = reverse_lazy('statuses')


class StatusUpdateView(LoginRequiredMixin, UpdateView,
                       SuccessMessageMixin):
    """
    View to update a status
    """
    model = Status
    template_name = 'status/edit.html'
    fields = ['name']
    success_message = _('Status successfully updated!')
    success_url = reverse_lazy('statuses')


class StatusDeleteView(LoginRequiredMixin, DeleteView,
                       SuccessMessageMixin):
    """
    View to delete a status
    """
    model = Status
    template_name = 'status/delete.html'
    success_url = reverse_lazy('statuses')
    success_message = _('Status successfully deleted!')
