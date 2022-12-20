from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
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


class LabelCreateView(CreateView,
                      LoginRequiredMixin):
    """
    View to create new labels
    """
    model = Label
    fields = ('name', )
    template_name = 'labels/create.html'

    def form_valid(self, form):
        messages.success(request=self.request,
                         message=_('Label successfully created!'))
        return super(LabelCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('labels')


class LabelUpdateView(UpdateView,
                      LoginRequiredMixin):
    """
    View to update a label
    """
    model = Label
    fields = ('name', )
    template_name = 'labels/edit.html'
    success_url = reverse_lazy('labels')

    def form_valid(self, form):
        messages.success(request=self.request,
                         message=_('Label successfully updated!'))
        return super(LabelUpdateView, self).form_valid(form)

    def get_success_url(self):
        return self.success_url


class LabelDeleteView(DeleteView,
                      LoginRequiredMixin):
    """
    View to delete a label
    """
    model = Label
    template_name = 'labels/delete.html'
    success_url = reverse_lazy('labels')

    def form_valid(self, form):
        messages.success(request=self.request,
                         message=_('Label successfully deleted!'))
        return super(LabelDeleteView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        """
        Before deleting we check if the label is used in a task
        """
        if self.get_object().labels.all().exists():
            messages.error(self.request,
                           _('Unable to delete label because it is in use'))
            return redirect('labels')

        return super().post(request, *args, **kwargs)
