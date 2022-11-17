from django.urls import path

from task_manager.users.views import UserListView, CreateUserView, LoginUserView, \
    user_logout, UserUpdateView, UserDeleteView


urlpatterns = [
    path('users', UserListView.as_view(), name='users'),
    path('users/create', CreateUserView.as_view(), name='register'),
    path('users/<int:pk>/edit', UserUpdateView.as_view(), name='edit'),
    path('users/<int:pk>/delete', UserDeleteView.as_view(), name='delete'),
    path('login', LoginUserView.as_view(), name='login'),
    path('logout', user_logout, name='logout'),
]