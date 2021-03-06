from books import models
from rest_framework import serializers


class AuthorSerializer(serializers.ModelSerializer):
    publised_books = serializers.SerializerMethodField()

    class Meta:
        model = models.Author
        fields = ["id", "name", "location", "publised_books"]

    def get_publised_books(self, obj):
        objs = models.Book.objects.filter(author__id=obj.id)
        arr = []
        for i in objs:
            arr.append({
                "book_id": i.id,
                "book_name": i.name
            })
        return arr


class BookListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = models.Book
        fields = ["id", "name", "description",
                  "author", "created_at", "last_update", "is_publised"]


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Book
        fields = ["id", "name", "description",
                  "author", "created_at", "last_update", "is_publised"]
        read_only_fields = ["id", "created_at", "last_update"]
        extra_kwargs = {'author': {'required': False},
                        'name': {'required': False}}
