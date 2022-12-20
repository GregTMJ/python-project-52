from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
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


class StatusCreateView(LoginRequiredMixin, CreateView):
    """
    View to create new status
    """
    model = Status
    form_class = StatusForm
    template_name = 'status/create.html'
    success_message = _('Status successfully created!')
    success_url = reverse_lazy('statuses')

    def form_valid(self, form):
        messages.success(request=self.request,
                         message=self.success_message)
        return super(StatusCreateView, self).form_valid(form)


class StatusUpdateView(LoginRequiredMixin, UpdateView):
    """
    View to update a status
    """
    model = Status
    template_name = 'status/edit.html'
    fields = ['name']
    success_message = _('Status successfully updated!')
    success_url = reverse_lazy('statuses')

    def form_valid(self, form):
        messages.success(request=self.request,
                         message=self.success_message)
        return super(StatusUpdateView, self).form_valid(form)


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    """
    View to delete a status
    """
    model = Status
    template_name = 'status/delete.html'
    success_url = reverse_lazy('statuses')
    success_message = _('Status successfully deleted!')

    def form_valid(self, form):
        messages.success(request=self.request,
                         message=self.success_message)
        return super(StatusDeleteView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        """
        Before deleting we verify if the status is not used in a task
        """
        if self.get_object().status.all().exists():
            messages.error(self.request,
                           _('Unable to delete status because it is in use'))
            return redirect('statuses')
        return super().post(request, *args, **kwargs)
