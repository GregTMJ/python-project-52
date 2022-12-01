from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, View, UpdateView, DeleteView

from task_manager.users.forms import NewUserForm


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


class CreateUserView(View):
    """
    A view that gives us an option of getting the form to create
    a new user.
    """
    def get(self, request, *args, **kwargs):
        """
        Gets the form in html template
        :return: template with the form
        """
        form = NewUserForm()
        return render(request=request,
                      template_name='users/register.html',
                      context={'register_form': form})

    def post(self, request, *args, **kwargs):
        """
        Validates the form, if valid adds the user in database
        if not returns an error message
        :return: a redirect to users with a successful message
        of stays on the same page with an error message
        """
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request,
                             _("Registration successful."))
            return redirect("/users")
        messages.error(request,
                       _("Unsuccessful registration. Invalid information."))


class UserUpdateView(UpdateView, SuccessMessageMixin):
    """
    View to update information about users
    """
    model = get_user_model()
    template_name = 'users/edit.html'
    fields = ('username', 'first_name', 'last_name',)
    success_message = _("User's information successfully updated")
    success_url = reverse_lazy('users')


class UserDeleteView(DeleteView, SuccessMessageMixin):
    """
    View to delete a certain user
    """
    model = get_user_model()
    template_name = 'users/delete.html'
    success_message = _("User deleted!")
    success_url = reverse_lazy('home')


class LoginUserView(SuccessMessageMixin, LoginView):
    """
    Handles the login view
    """
    template_name = 'users/login.html'
    success_message = _('You are logged in!')


class LogoutUserView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.info(request, _('You logged out!'))
        return super().dispatch(request, *args, **kwargs)
