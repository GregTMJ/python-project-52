from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, \
    get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
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
                             "Registration successful.")
            return redirect("/users")
        messages.error(request,
                       "Unsuccessful registration. Invalid information.")


class UserUpdateView(UpdateView):
    """
    View to update information about users
    """
    model = get_user_model()
    template_name = 'users/edit.html'
    fields = ('username', 'first_name', 'last_name',)
    success_url = reverse_lazy('users')


class UserDeleteView(DeleteView):
    """
    View to delete a certain user
    """
    model = get_user_model()
    template_name = 'users/delete.html'
    success_url = reverse_lazy('home')


class LoginUserView(View):
    """
    Handles the login view
    """
    def dispatch(self, request, *args, **kwargs):
        """
        If user is logged in, no need to give access to this url anymore
        :return: if user is authenticated, redirects to homepage
        automatically
        """
        if request.user.is_authenticated:
            return redirect('/')
        return super(LoginUserView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
        Getting the url with a form to login
        :return: template with the correspondant form
        """
        form = AuthenticationForm
        return render(request=request,
                      template_name='users/login.html',
                      context={"login_form": form})

    def post(self, request, *args, **kwargs):
        """
        handles the post of the same form given by the url in GET
        request
        :return: if success, you redirect to homepage with a successful
        message, else keeps on the same page with an error message
        """
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username,
                                password=password)
            if user:
                login(request, user)
                messages.info(request,
                              f"You are now logged in as {username}.")
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")


def user_logout(request):
    """
    logout view in form of function to not make an irrelevant class
    based view
    :return: redirects to homepage
    """
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("/")
