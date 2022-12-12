from django import forms

from task_manager.tasks.models import Task


class CreateTaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['name', 'description', 'executor', 'status', 'labels']
