from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from task_manager.json_data import get_data
from task_manager.labels.models import Label


class TestLabelCase(TestCase):

    def setUp(self) -> None:
        """
        Initializing testcases
        """
        self.label_list = reverse('labels')
        self.create_label = reverse('create_label')
        self.labels = get_data('labels')
        self.user = get_data('users').get("new")
        self.create_user = User.objects.create_user(**self.user)
        self.create_user.save()
        self.client.login(
            username=self.create_user.username,
            password=self.user.get('password')
        )

    def test_get_listview(self):
        """
        Testing the main view
        """
        response = self.client.get(self.label_list)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/main.html')

    def test_get_createView(self):
        """
        Testing the GET method for create view:
        """
        response = self.client.get(self.create_label)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/create.html')

    def test_post_createView(self):
        """
        Testing the POST method for create view
        """
        new_label = self.labels.get('new')
        response = self.client.post(self.create_label,
                                    new_label)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, self.label_list)

    def test_updateView(self):
        """
        Testing the GET/POST method for update view
        """
        new_label = self.labels.get("new")
        self.client.post(self.create_label,
                         new_label)

        label = Label.objects.get(name=new_label['name'])
        response = self.client.get(reverse('update_label',
                                           args=[label.id]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/edit.html')

        edit_label = self.labels.get("updated_label")
        post_response = self.client.post(reverse('update_label',
                                                 args=[label.id]),
                                         edit_label)
        self.assertEquals(post_response.status_code, 302)
        self.assertRedirects(post_response, self.label_list)

        updated_label = Label.objects.get(name=edit_label['name'])
        self.assertEquals(updated_label.name, edit_label['name'])

    def test_deleteView(self):
        """
        Testing the GET/POST method for delete view
        """
        new_label = self.labels.get("new")
        self.client.post(self.create_label,
                         new_label)

        label = Label.objects.get(name=new_label['name'])
        response = self.client.get(reverse('delete_label',
                                           args=[label.id]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/delete.html')

        delete_response = self.client.post(reverse('delete_label',
                                                   args=[label.id]))
        self.assertEquals(delete_response.status_code, 302)
        self.assertRedirects(delete_response, self.label_list)
