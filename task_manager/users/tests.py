from django import test
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.json_data import get_data
from task_manager.users.models import User


@test.modify_settings(MIDDLEWARE={'remove': [
    'rollbar.contrib.django.middleware.RollbarNotifierMiddleware',
]})
class TestAuthRequests(TestCase):
    fixtures = ['users.json']

    def setUp(self) -> None:
        """
        Initialize all our urls + We create a new user for
        tests
        """
        self.homepage_url = reverse('home')
        self.list_users_url = reverse('users')
        self.login_url = reverse('login')
        self.register_url = reverse('register')

        self.user_info: dict = get_data('users').get('new')
        self.users_info = get_data("users")

        self.create_user = User.objects.create_user(**self.users_info.get('new'))
        self.create_user.save()

        self.edit_user_url = reverse('edit',
                                     args=[self.create_user.id])
        self.delete_user_url = reverse('delete',
                                       args=[self.create_user.id])

    def login(self):
        """
        To keep our client logged in, because if we try to
        post to login_url, we will always get an 403 error
        because of the csrf token
        """
        self.client.login(
            username=self.user_info.get('username'),
            password=self.user_info.get('password')
        )

    def assertUser(self, user, user_data):
        """
        New assertion to compare 2 data queries
        :param user: the user updated infos
        :param user_data: the current user stored in db
        """
        self.assertEqual(user.first_name, user_data.get('first_name'))
        self.assertEqual(user.last_name, user_data.get('last_name'))

    def test_homepage_GET(self):
        """
        Checking if you get the homepage correctly
        """
        response = self.client.get(self.homepage_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'basic.html')

    def test_users_GET(self):
        """
        Testing the users page GET request
        """
        response = self.client.get(self.list_users_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/main.html')

    def test_login_GET(self):
        """
        Testing the login page GET request
        """
        response = self.client.get(self.login_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

        exist_user = {
            'id': self.user_info.get('id'),
            'username': self.user_info.get('username'),
            'password': self.user_info.get('password')
        }

        tester_login = self.client.login(**exist_user)

        self.assertTrue(tester_login)
        self.client.logout()

        response = self.client.post(self.login_url,
                                    exist_user,
                                    follow=True)

        self.assertTrue(response.context['user'].is_active)
        self.assertEquals(int(self.client.session['_auth_user_id']),
                          exist_user.get('id'))

    def test_register_GET(self):
        """
        Testing the register page GET request
        """
        response = self.client.get(self.register_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_register_user(self):
        """
        Testing register new user
        """
        response = self.client.post(self.register_url,
                                    self.users_info.get("tester"))

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, self.list_users_url)

        response = self.client.post(self.register_url,
                                    self.users_info.get("new"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_edit_user_GET(self):
        """
        Testing the edit user page GET request
        """
        response = self.client.get(self.edit_user_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/edit.html')

    def test_delete_user_GET(self):
        """
        Testing the delete user page GET request
        """
        response = self.client.get(self.delete_user_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/delete.html')

    def test_update_user(self):
        """
        Testing update
        """
        self.login()
        update_user_info = self.users_info.get('updated_user')
        response = self.client.post(self.edit_user_url,
                                    update_user_info)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, self.list_users_url)
        updated_user = get_user_model().objects.get(
            username=update_user_info.get("username"))
        self.assertUser(updated_user, update_user_info)

    def test_delete_user(self):
        """
        Testing delete
        """
        self.login()
        response = self.client.post(self.delete_user_url)
        self.assertRedirects(response, self.homepage_url)
        self.assertEqual(response.status_code, 302)

    def test_logout(self):
        """
        Testing the logout
        """
        self.login()
        response = self.client.post(reverse('logout'))

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))
