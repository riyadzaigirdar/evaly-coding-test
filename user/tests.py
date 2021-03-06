from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

CREATE_USER_URL = reverse('user:signup')
LOGIN_URL = reverse('user:login')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class ModelTest(TestCase):

    def test_create_user_with_email_successful(self):
        email = 'riyad@gmail.com'
        name = 'riyad'
        password = '1234'

        user = get_user_model().objects.create_user(
            email=email,
            name=name,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_member)

    def test_check_password_matches(self):
        email = "onni@gmail.com"
        name = "onni"
        user = get_user_model().objects.create_user(email, name, "1234")
        self.assertTrue(user.check_password("1234"))

    def test_create_new_user_email_normalization(self):
        email = 'riyad@kalke.co'
        name = "riyad"
        user = get_user_model().objects.create_user(email, name, '1234')
        self.assertEqual(user.email, email.lower())

    def test_check_create_superuser(self):
        user = get_user_model().objects.create_superuser(
            'riyad@gmail.com',
            'riyad',
            '1234'
        )
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)


class PublicUserApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        payload = {
            'email': 'riyad1234@gmail.com',
            'name': 'riyad1234',
            'password': '123456'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(id=res.data["id"])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exist(self):
        payload = {
            'email': 'new_user@gmail.com',
            'name': 'new_user',
            'password': '1234'
        }
        # create_user(**payload)
        get_user_model().objects.create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_invalid_credintials(self):
        payload = {
            'email': 'newuser1234@gmail.com',
            'name': 'newuser1234',
            'password': '1234'
        }
        create_user(**payload)
        res = self.client.post(
            LOGIN_URL, {'email': 'newuser1234@gmail.com', 'password': '4321'})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        payload = {
            'email': 'newuser1234@gmail.com',
            'name': 'newuser1234',
            'password': '1234'
        }
        res = self.client.post(LOGIN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
