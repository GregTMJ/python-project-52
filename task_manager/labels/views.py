from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, CreateView, \
    UpdateView, DeleteView

from task_manager.labels.models import Label


class LabelListView(ListView, LoginRequiredMixin):
    """
    View to get all available labels
    """
    model = Label
    template_name = 'labels/main.html'
    context_object_name = 'labels'


class LabelCreateView(CreateView, SuccessMessageMixin,
                      LoginRequiredMixin):
    """
    View to create new labels
    """
    model = Label
    fields = ('name', )
    template_name = 'labels/create.html'
    success_message = _('Label successfully created!')
    success_url = reverse_lazy('labels')


class LabelUpdateView(UpdateView, SuccessMessageMixin,
                      LoginRequiredMixin):
    """
    View to update a label
    """
    model = Label
    fields = ('name', )
    template_name = 'labels/edit.html'
    success_message = _('Label successfully updated!')
    success_url = reverse_lazy('labels')


class LabelDeleteView(DeleteView, SuccessMessageMixin,
                      LoginRequiredMixin):
    """
    View to delete a label
    """
    model = Label
    template_name = 'labels/delete.html'
    success_message = _('Label successfully deleted!')
    success_url = reverse_lazy('labels')
