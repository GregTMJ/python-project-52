from django import forms
from django.utils.translation import gettext_lazy as _

from task_manager.tasks.models import Task
from task_manager.labels.models import Label


class CreateTaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['name', 'description', 'executor', 'status', 'label']

    label = forms.ModelMultipleChoiceField(
        queryset=Label.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label=_('labels'),
    )
