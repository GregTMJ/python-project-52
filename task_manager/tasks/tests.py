from django import test
from django.test import TestCase
from django.urls import reverse

from task_manager.json_data import get_data
from task_manager.tasks.models import Task, TaskLabelRelation
from task_manager.labels.models import Label
from task_manager.status.models import Status
from task_manager.users.models import User


@test.modify_settings(MIDDLEWARE={'remove': [
    'rollbar.contrib.django.middleware.RollbarNotifierMiddleware',
]})
class TaskTest(TestCase):
    fixtures = ['users.json', 'status.json',
                'labels.json', 'tasks.json']

    def setUp(self) -> None:
        self.list_task = reverse('tasks')
        self.create_task = reverse('create_task')

        self.status_data = get_data('status')
        self.users_data = get_data('task_users').get('task_users')

        self.tasks_data: dict = get_data('tasks')

        self.label_data: dict = get_data('labels')

        self.task_labels: dict = get_data('task_labels') \
            .get('task_labels')

        self.status = Status.objects.get(
            name=self.status_data.get('new')['name']
        )
        self.new_status = Status.objects.get(
            name=self.status_data.get('existing')['name']
        )

        self.first_label = Label.objects.get(
            name=self.label_data.get('existing')[0]['name']
        )
        self.second_label = Label.objects.get(
            name=self.label_data.get('existing')[1]['name']
        )

        self.author = User.objects.create_user(
            **self.users_data.get('author')
        )
        self.executor = User.objects.create_user(
            **self.users_data.get('executor')
        )
        self.random_user = User.objects.create(
            **self.users_data.get('random_user')
        )

        self.client.login(
            username=self.users_data.get('author')['username'],
            password=self.users_data.get('author')['password']
        )

        self.existing_task = Task.objects.get(
            name=self.tasks_data.get('existing').get('name'))

        self.task: dict = self.tasks_data.get('new')

        self.task.update(
            {
                'author': self.executor,
                'executor': self.author.id,
                'status': self.new_status.id,
            }
        )

    def test_list_tasks(self):
        """
        Testing to GET our list of tasks
        """
        response = self.client.get(self.list_task)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/main.html')

    def test_create_page(self):
        """
        Testing to GET our creation task page
        """
        get_response = self.client.get(self.create_task)

        self.assertEquals(get_response.status_code, 200)
        self.assertTemplateUsed(get_response, 'tasks/create.html')

    def test_create_task(self):
        """
        Test Create new task
        """
        create_task: dict = self.task
        response = self.client.post(self.create_task,
                                    create_task)

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, self.list_task)

        created_task = Task.objects.get(name=create_task['name'])
        self.assertEquals(created_task.author.username,
                          self.author.username)

    def test_detail_task(self):
        """
        Test GET details on certain existing task
        """
        response = self.client.get(reverse('task',
                                           args=[self.existing_task.pk]))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/detail.html')

    def test_update_page(self):
        """
        Test updating a task
        """
        new_status_task = {
            'name': self.task.get('name'),
            'executor': self.task.get('author').id,
            'status': self.new_status.id,
            'labels': [self.second_label.id]
        }
        post_response = self.client.post(
            reverse('update_task',
                    args=[self.existing_task.pk]),
            new_status_task)

        self.assertRedirects(post_response, self.list_task)
        updated_task = Task.objects.get(name=self.task['name'])
        self.assertEquals(updated_task.status.name, self.new_status.name)

    def test_delete_task(self):
        """
        Testing deleting a task
        """
        response = self.client.get(reverse('delete_task',
                                           args=[self.existing_task.pk]))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/delete.html')

        delete_response = self.client.post(
            reverse('delete_task',
                    args=[self.existing_task.pk]))
        self.assertRedirects(delete_response, self.list_task)

    def test_create_label_task(self):
        """
        Test to create a foreign relations using TaskLabelRelation Model
        """
        created_label = Label.objects.get(
            name=self.task_labels[0].get('name')
        )
        task_label = TaskLabelRelation.objects.create(
            task=self.existing_task,
            label=created_label
        )

        self.assertEquals(task_label.task, self.existing_task)
        self.assertEquals(task_label.label, created_label)
        self.assertEquals(self.existing_task.labels.all()[0], created_label)

    def test_filter_task(self):
        """
        Test our filter on tasks main page
        :return:
        """
        task_filter = {
            'status': self.task.get('status')
        }

        response = self.client.get(self.list_task,
                                   task_filter)
        task = Task.objects.filter(status=self.task.
                                   get('status'))

        self.assertQuerysetEqual(response.context['tasks'], task)

        self.client.logout()
        self.client.login(
            username=self.users_data.get('random_user').get('username'),
            password=self.users_data.get('random_user').get('password')
        )

        task_filter = {
            'users_task': 'on',
            'status': self.task.get('status')
        }

        response = self.client.get(self.list_task,
                                   task_filter)
        self.assertQuerysetEqual(response.context['tasks'], [])
