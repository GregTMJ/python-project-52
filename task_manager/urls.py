from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name="home.html"), name='home'),
    path('', include('task_manager.users.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
]
