from django import forms
from django_filters import FilterSet
from django_filters.filters import BooleanFilter, ModelChoiceFilter
from django.utils.translation import gettext_lazy as _

from task_manager.tasks.models import Task
from task_manager.labels.models import Label


class TaskFilter(FilterSet):
    """
    Here we create our filter for the tasks
    """
    users_task = BooleanFilter(
        widget=forms.CheckboxInput,
        field_name='author',
        method='filter_users_task',
        label=_('Only your tasks')
    )

    label = ModelChoiceFilter(
        queryset=Label.objects.all(),
        field_name='labels',
        label=_('label')
    )

    def filter_users_task(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user.id)
        return queryset

    class Meta:
        model = Task
        fields = ['status', 'executor', 'label']
