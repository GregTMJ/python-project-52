from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class TestGetRequests(TestCase):

    def setUp(self) -> None:
        """
        Initialize all our urls + We create a new user for
        tests
        """
        self.homepage_url = reverse('home')
        self.list_users_url = reverse('users')
        self.login_url = reverse('login')
        self.register_url = reverse('register')
        self.create_user = get_user_model().objects.create(
            first_name='Gregory',
            last_name='Saliba',
            username='Greg',
            password='Something_1'
        )
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
            username=self.create_user.username,
            password=self.create_user.password
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

    def test_register_GET(self):
        """
        Testing the register page GET request
        """
        response = self.client.get(self.register_url)

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
        new_user_data = {
            "first_name": "Gregz",
            "last_name": "Saliba",
            "username": "Gregtmj"
        }
        response = self.client.post(self.edit_user_url,
                                    new_user_data, )
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, self.list_users_url)
        updated_user = get_user_model().objects.get(username=new_user_data.get("username"))
        self.assertUser(updated_user, new_user_data)

    def test_delete_user(self):
        """
        Testing delete
        """
        self.login()
        response = self.client.post(self.delete_user_url)
        self.assertRedirects(response, self.homepage_url)
        self.assertEqual(response.status_code, 302)
