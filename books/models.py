from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=400)
    location = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"


class Book(models.Model):
    name = models.CharField(max_length=400)
    description = models.TextField(blank=True, null=True)
    author = models.ForeignKey("Author", on_delete=models.CASCADE)
    is_publised = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} by {self.author.name}"
