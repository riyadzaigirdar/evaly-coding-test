from django.db import models
from books.models import Book
from django.contrib.auth import get_user_model

User = get_user_model()


class Loan(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.DO_NOTHING)
    is_accepted = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.member.name} requested for {self.book.name}"
