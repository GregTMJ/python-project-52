from django import test
from django.test import TestCase
from django.urls import reverse

from task_manager.json_data import get_data
from task_manager.status.models import Status
from task_manager.users.models import User


@test.modify_settings(MIDDLEWARE={'remove': [
    'rollbar.contrib.django.middleware.RollbarNotifierMiddleware',
]})
class TestStatusRequest(TestCase):
    fixtures = ['status.json']

    def setUp(self) -> None:
        """
        initializing our setup for the test cases
        """
        self.list_statuses = reverse('statuses')
        self.create_status = reverse('status_create')
        self.user_info: dict = get_data('users').get('new')
        self.status_info: dict = get_data('status')
        self.create_user = User.objects.create_user(**self.user_info)
        self.create_user.save()
        self.client.login(
            username=self.user_info.get("username"),
            password=self.user_info.get("password")
        )

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.list_statuses)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/login?next=/statuses/')

    def test_logged_in_user(self):
        response = self.client.get(self.list_statuses)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'status/main.html')

    def test_create_status(self):
        response = self.client.get(self.create_status)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'status/create.html')

        new_status = self.status_info.get("new")
        post_response = self.client.post(self.create_status,
                                         new_status)
        self.assertRedirects(post_response, self.list_statuses)

        created_status = Status.objects.get(name=new_status['name'])
        self.assertEqual(created_status.name, new_status['name'])

    def test_update_status(self):
        existing_status = Status.objects.get(
            name=self.status_info.get('existing')['name']
        )
        response = self.client.get(reverse('status_update',
                                           args=[existing_status.pk]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'status/edit.html')

        updated_status = self.status_info.get("new")
        post_response = self.client.post(
            reverse('status_update',
                    args=[existing_status.pk]),
            updated_status)
        self.assertEquals(post_response.status_code, 302)

        status = Status.objects.get(name=updated_status['name'])
        self.assertEquals(updated_status['name'], status.name)

    def test_delete_status(self):
        created_status = Status.objects.get(
            name=self.status_info.get("existing")['name'])
        response = self.client.get(reverse('status_delete',
                                           args=[created_status.pk]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'status/delete.html')

        response = self.client.post(reverse('status_delete',
                                            args=[created_status.pk]))
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, self.list_statuses)
