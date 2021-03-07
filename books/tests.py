# contains three type of tests
# model test -> mock test unit test
# public api test -> not authenticated
# priate api test -> authenticated

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from books.models import Author, Book
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

AUTHOR_LIST_URL = reverse("books:author-list")
BOOK_LIST_URL = reverse("books:books-list")


def CREATE_AUTHOR_DETAIL_URL(id):
    return reverse("books:author-detail", args=[id])


def CREATE_BOOK_DETAIL_URL(id):
    return reverse("books:books-detail", args=[id])


def create_user(**params):
    return get_user_model().objects.create_user(**params)


def create_super_user(email, name, password):
    return get_user_model().objects.create_superuser(email, name, password)


def create_sample_author(**params):
    return Author.objects.create(**params)


def create_sample_book(**params):
    return Book.objects.create(**params)


class ModelTest(TestCase):

    def test_create_author_successfully(self):
        body = {
            "name": "michael jackson",
            "location": "america"
        }
        obj = Author.objects.create(**body)

        self.assertEqual(obj.name, body["name"])
        self.assertEqual(obj.location, body["location"])

    def test_create_book_successfully(self):
        body1 = {
            "name": "michael jackson",
            "location": "america"
        }
        author = create_sample_author(**body1)

        body2 = {
            "name": "ramakanto kamar",
            "description": "Lorem ipsum, or lipsum as it is sometimes known, is dummy text used in laying out print, graphic or web designs. The passage is attributed to an unknown typesetter in the 15th century who is thought to have scrambled parts of Cicero's De Finibus Bonorum et Malorum for use in a type specimen book. It usually begins with",
            "author": author
        }

        book = create_sample_book(**body2)

        self.assertEqual(book.name, body2["name"])
        self.assertEqual(book.description, body2["description"])
        self.assertEqual(book.author.id, author.id)
        self.assertEqual(book.author.name, author.name)
        self.assertEqual(book.author.location, author.location)


class PublicApiTest(TestCase):

    def setup(self):
        self.client = APIClient()

    def test_list_author_no_authentication(self):
        body = {
            "name": "michael jackson",
            "location": "america"
        }
        create_sample_author(**body)
        create_sample_author(**body)

        res = self.client.get(AUTHOR_LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_list_books_no_authentication(self):
        body1 = {
            "name": "michael jackson",
            "location": "america"
        }
        author = create_sample_author(**body1)

        body2 = {
            "name": "ramakanto kamar",
            "description": "Lorem ipsum, or lipsum as it is sometimes known, is dummy text used in laying out print, graphic or web designs. The passage is attributed to an unknown typesetter in the 15th century who is thought to have scrambled parts of Cicero's De Finibus Bonorum et Malorum for use in a type specimen book. It usually begins with",
            "author": author
        }
        create_sample_book(**body2)
        create_sample_book(**body2)

        res = self.client.get(BOOK_LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_create_author_unauthorized(self):
        payload = {
            "name": "michael jackson",
            "location": "america"
        }
        res = self.client.post(AUTHOR_LIST_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_book_unauthorized(self):
        body1 = {
            "name": "michael jackson",
            "location": "america"
        }
        author = create_sample_author(**body1)

        body2 = {
            "name": "ramakanto kamar",
            "description": "Lorem ipsum, or lipsum as it is sometimes known, is dummy text used in laying out print, graphic or web designs. The passage is attributed to an unknown typesetter in the 15th century who is thought to have scrambled parts of Cicero's De Finibus Bonorum et Malorum for use in a type specimen book. It usually begins with",
            "author": author.id
        }

        res = self.client.post(BOOK_LIST_URL, body2)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_author_unauthorized(self):
        payload = {
            "name": "michael jackson",
            "location": "america"
        }

        author = create_sample_author(**payload)

        updated_payload = {
            "name": "michael updated",
            "location": "america updated"
        }

        res = self.client.patch(
            CREATE_AUTHOR_DETAIL_URL(author.id), updated_payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_book_unauthorized(self):
        body1 = {
            "name": "michael jackson",
            "location": "america"
        }
        author = create_sample_author(**body1)

        body2 = {
            "name": "ramakanto kamar",
            "description": "Lorem ipsum, or lipsum as it is sometimes known, is dummy text used in laying out print, graphic or web designs. The passage is attributed to an unknown typesetter in the 15th century who is thought to have scrambled parts of Cicero's De Finibus Bonorum et Malorum for use in a type specimen book. It usually begins with",
            "author": author
        }
        book = create_sample_book(**body2)

        updated_payload = {
            "name": "ramakanto updated",
            "description": "Lorem updated"
        }
        res = self.client.patch(
            CREATE_AUTHOR_DETAIL_URL(book.id), updated_payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_author_unauthorized(self):
        body1 = {
            "name": "michael jackson",
            "location": "america"
        }
        author = create_sample_author(**body1)
        res = self.client.delete(
            CREATE_AUTHOR_DETAIL_URL(author.id))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_book_unauthorized(self):
        body1 = {
            "name": "michael jackson",
            "location": "america"
        }
        author = create_sample_author(**body1)

        body2 = {
            "name": "ramakanto kamar",
            "description": "Lorem ipsum, or lipsum as it is sometimes known, is dummy text used in laying out print, graphic or web designs. The passage is attributed to an unknown typesetter in the 15th century who is thought to have scrambled parts of Cicero's De Finibus Bonorum et Malorum for use in a type specimen book. It usually begins with",
            "author": author
        }
        book = create_sample_book(**body2)

        res = self.client.delete(CREATE_BOOK_DETAIL_URL(book.id))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = create_super_user("riyad@gmail.com", "riyad", "123")
        self.client.force_authenticate(self.user)

    def test_list_author_with_authentication(self):
        body = {
            "name": "michael jackson",
            "location": "america"
        }
        create_sample_author(**body)
        create_sample_author(**body)

        res = self.client.get(AUTHOR_LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_list_books_with_authentication(self):
        body1 = {
            "name": "michael jackson",
            "location": "america"
        }
        author = create_sample_author(**body1)

        body2 = {
            "name": "ramakanto kamar",
            "description": "Lorem ipsum, or lipsum as it is sometimes known, is dummy text used in laying out print, graphic or web designs. The passage is attributed to an unknown typesetter in the 15th century who is thought to have scrambled parts of Cicero's De Finibus Bonorum et Malorum for use in a type specimen book. It usually begins with",
            "author": author
        }
        create_sample_book(**body2)
        create_sample_book(**body2)

        res = self.client.get(BOOK_LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_create_author_successful_authorized_admin(self):
        payload = {
            "name": "michael jackson",
            "location": "america"
        }
        res = self.client.post(AUTHOR_LIST_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["name"], payload["name"])
        self.assertEqual(res.data["location"], payload["location"])

    def test_create_author_forbidden_authorized_member(self):
        user = {
            "email": "onni@gmail.com",
            "name": "onni",
            "password": "123"
        }
        self.user = create_user(**user)
        self.client.force_authenticate(self.user)
        payload = {
            "name": "michael jackson",
            "location": "america"
        }
        res = self.client.post(AUTHOR_LIST_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_book_successful_authorized_admin(self):
        body1 = {
            "name": "michael jackson",
            "location": "america"
        }
        author = create_sample_author(**body1)

        body2 = {
            "name": "ramakanto kamar",
            "description": "Lorem ipsum, or lipsum as it is sometimes known, is dummy text used in laying out print, graphic or web designs. The passage is attributed to an unknown typesetter in the 15th century who is thought to have scrambled parts of Cicero's De Finibus Bonorum et Malorum for use in a type specimen book. It usually begins with",
            "author": author.id
        }

        res = self.client.post(BOOK_LIST_URL, body2)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["name"], body2["name"])
        self.assertEqual(res.data["description"], body2["description"])

    def test_create_book_forbidden_authorized_member(self):

        user = {
            "email": "onni@gmail.com",
            "name": "onni",
            "password": "123"
        }
        self.user = create_user(**user)
        self.client.force_authenticate(self.user)
        body1 = {
            "name": "michael jackson",
            "location": "america"
        }
        author = create_sample_author(**body1)

        body2 = {
            "name": "ramakanto kamar",
            "description": "Lorem ipsum, or lipsum as it is sometimes known, is dummy text used in laying out print, graphic or web designs. The passage is attributed to an unknown typesetter in the 15th century who is thought to have scrambled parts of Cicero's De Finibus Bonorum et Malorum for use in a type specimen book. It usually begins with",
            "author": author.id
        }

        res = self.client.post(BOOK_LIST_URL, body2)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_author_successful_authorized_admin(self):
        payload = {
            "name": "michael jackson",
            "location": "america"
        }

        author = create_sample_author(**payload)

        updated_payload = {
            "name": "michael updated",
            "location": "america updated"
        }

        res = self.client.patch(
            CREATE_AUTHOR_DETAIL_URL(author.id), updated_payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(updated_payload["name"], res.data["name"])
        self.assertEqual(updated_payload["location"], res.data["location"])

    def test_update_book_forbidden_authorized_member(self):
        user = {
            "email": "onni@gmail.com",
            "name": "onni",
            "password": "123"
        }
        self.user = create_user(**user)
        self.client.force_authenticate(self.user)
        body1 = {
            "name": "michael jackson",
            "location": "america"
        }
        author = create_sample_author(**body1)

        body2 = {
            "name": "ramakanto kamar",
            "description": "Lorem ipsum, or lipsum as it is sometimes known, is dummy text used in laying out print, graphic or web designs. The passage is attributed to an unknown typesetter in the 15th century who is thought to have scrambled parts of Cicero's De Finibus Bonorum et Malorum for use in a type specimen book. It usually begins with",
            "author": author
        }
        book = create_sample_book(**body2)

        updated_payload = {
            "name": "ramakanto updated",
            "description": "Lorem updated"
        }
        res = self.client.patch(
            CREATE_AUTHOR_DETAIL_URL(book.id), updated_payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_author_successful_authorized_admin(self):
        body1 = {
            "name": "michael jackson",
            "location": "america"
        }
        author = create_sample_author(**body1)
        res = self.client.delete(
            CREATE_AUTHOR_DETAIL_URL(author.id))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_book_forbidden_authorized_member(self):
        user = {
            "email": "onni@gmail.com",
            "name": "onni",
            "password": "123"
        }
        self.user = create_user(**user)
        self.client.force_authenticate(self.user)
        body1 = {
            "name": "michael jackson",
            "location": "america"
        }
        author = create_sample_author(**body1)

        body2 = {
            "name": "ramakanto kamar",
            "description": "Lorem ipsum, or lipsum as it is sometimes known, is dummy text used in laying out print, graphic or web designs. The passage is attributed to an unknown typesetter in the 15th century who is thought to have scrambled parts of Cicero's De Finibus Bonorum et Malorum for use in a type specimen book. It usually begins with",
            "author": author
        }
        book = create_sample_book(**body2)
        res = self.client.delete(CREATE_BOOK_DETAIL_URL(book.id))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
