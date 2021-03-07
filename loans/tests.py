from os import stat
from rest_framework import status
from loans.models import Loan
from django.urls import reverse
from django.test import TestCase
from books.models import Book, Author
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

LOAN_LIST_URL = reverse("loans:loan-list")
EXCEL_URL = reverse("loans:excel")


def CREATE_LOAN_DETAIL_URL(id):
    return reverse("loans:loan-detail", args=[id])


def create_sample_user():
    return get_user_model().objects.create_user("onni@gmail.com", "onni", "1234")


def create_sample_super_user():
    return get_user_model().objects.create_superuser("riyad@gmail.com", "riyad", "1234")


def create_super_user(email, name, password):
    return get_user_model().objects.create_superuser(email, name, password)


def create_user(email, name, password):
    return get_user_model().objects.create_user(email, name, password)


def create_sample_book_with_author():
    body1 = {
        "name": "michael jackson",
        "location": "america"
    }
    author = Author.objects.create(**body1)

    body2 = {
        "name": "ramakanto kamar",
        "description": "Lorem ipsum, or lipsum as it is sometimes known, is dummy text used in laying out print, graphic or web designs. The passage is attributed to an unknown typesetter in the 15th century who is thought to have scrambled parts of Cicero's De Finibus Bonorum et Malorum for use in a type specimen book. It usually begins with",
        "author": author
    }
    return Book.objects.create(**body2)


class ModelTest(TestCase):

    def test_create_loan_successfully(self):
        book = create_sample_book_with_author()
        member = create_sample_user()
        body = {
            "member": member,
            "book": book,
        }
        loan = Loan.objects.create(**body)

        self.assertEqual(loan.member.id, body["member"].id)
        self.assertEqual(loan.book.id, body["book"].id)
        self.assertEqual(loan.is_accepted, False)
        self.assertEqual(loan.is_returned, False)
        self.assertEqual(loan.is_rejected, False)

    def test_create_loan_check_list(self):
        book = create_sample_book_with_author()
        member = create_sample_user()
        body = {
            "member": member,
            "book": book,
        }
        Loan.objects.create(**body)
        Loan.objects.create(**body)
        Loan.objects.create(**body)

        loans = Loan.objects.all()

        self.assertEqual(len(loans), 3)

    def test_create_and_update_loan_successfully(self):
        book = create_sample_book_with_author()
        member = create_sample_user()
        body = {
            "member": member,
            "book": book,
        }
        loan = Loan.objects.create(**body)
        loan.is_accepted = True
        loan.is_returned = True
        loan.is_rejected = True
        loan.save()

        self.assertEqual(loan.is_accepted, True)
        self.assertEqual(loan.is_returned, True)
        self.assertEqual(loan.is_rejected, True)


class PublicApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_loan_list_unauthorized(self):
        res = self.client.get(LOAN_LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateApiList(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = create_sample_super_user()
        self.client.force_authenticate(self.user)

    def test_get_download_excel_link(self):
        res = self.client.get(EXCEL_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("download_link",
                      res.data)

    def test_update_loan_succesfully_authorized_admin(self):
        book = create_sample_book_with_author()
        member = create_sample_user()
        body = {
            "member": member,
            "book": book,
        }
        loan = Loan.objects.create(**body)

        payload = {
            "is_accepted": True,
            "is_rejected": True,
            "is_returned": True
        }

        res = self.client.patch(CREATE_LOAN_DETAIL_URL(loan.id), payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["is_accepted"], payload["is_accepted"])
        self.assertEqual(res.data["is_rejected"], payload["is_rejected"])
        self.assertEqual(res.data["is_returned"], payload["is_returned"])

    def test_update_loan_forbidden_authorized_member(self):
        self.user = create_sample_user()
        self.client.force_authenticate(self.user)
        book = create_sample_book_with_author()
        member = self.user
        body = {
            "member": member,
            "book": book,
        }
        loan = Loan.objects.create(**body)

        payload = {
            "is_accepted": True,
            "is_rejected": True,
            "is_returned": True
        }

        res = self.client.patch(CREATE_LOAN_DETAIL_URL(loan.id), payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
