from django.forms import ModelForm
from task_manager.status.models import Status


class StatusForm(ModelForm):

    class Meta:
        model = Status
        fields = ['name']
