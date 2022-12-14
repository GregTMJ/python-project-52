from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, UpdateView, DeleteView, CreateView

from task_manager.mixins import AuthRequiredMixin, NoPermissionMixin,\
    SuccessMessageDeleteMixin
from task_manager.users.forms import NewUserForm
from task_manager.users.models import User
from task_manager.users.mixins import CheckUserMixin


class UserListView(ListView):
    """
    Getting the list of users in database
    """
    model = get_user_model()
    template_name = 'users/main.html'
    context_object_name = 'people'

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        to use the context in html template
        :return: the given context
        """
        context = super().get_context_data(**kwargs)
        return context


class CreateUserView(CreateView, SuccessMessageMixin):
    """
    A view that gives us an option of getting the form to create
    a new user.
    """
    model = User
    form_class = NewUserForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')
    success_message = _("Registration successful")

    def form_valid(self, form):
        messages.success(request=self.request,
                         message=self.success_message)
        return super(CreateUserView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(request=self.request,
                       message=_("Unsuccessful registration. Invalid information."))
        return super(CreateUserView, self).form_invalid(form)


class UserUpdateView(NoPermissionMixin, AuthRequiredMixin,
                     CheckUserMixin, SuccessMessageMixin,
                     UpdateView):
    """
    View to update information about users
    """
    model = get_user_model()
    template_name = 'users/edit.html'
    form_class = NewUserForm
    success_message = _("User's information successfully updated")
    success_url = reverse_lazy('users')


class UserDeleteView(NoPermissionMixin, AuthRequiredMixin,
                     CheckUserMixin, SuccessMessageDeleteMixin,
                     DeleteView):
    """
    View to delete a certain user
    """
    model = get_user_model()
    template_name = 'users/delete.html'
    success_message = _("User deleted!")
    success_url = reverse_lazy('users')

    def post(self, request, *args, **kwargs):
        """
        We verify if the use is not taking a task, or didn't create one
        """
        if self.get_object().author.all().exists() or \
                self.get_object().executor.all().exists():
            messages.error(self.request,
                           _('Unable to delete user because it is in use'))
            return redirect('statuses')
        return super().post(request, *args, **kwargs)


class LoginUserView(SuccessMessageMixin, LoginView):
    """
    Handles the login view
    """
    template_name = 'users/login.html'
    success_message = _('You are logged in!')


class LogoutUserView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.info(request, _('You logged out'))
        return super().dispatch(request, *args, **kwargs)
