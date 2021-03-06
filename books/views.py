from books.models import Book, Author
from books import serializers
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework import status, viewsets


class BookView(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    filter_backends = [SearchFilter]
    # ?search= will search in this fields
    search_fields = ['id', 'name', 'description']

    # no authentication required for browsing list of books
    def list(self, request, *args, **kwargs):
        books = Book.objects.filter(is_publised=True)
        serializer = serializers.BookListSerializer(
            self.filter_queryset(books), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # only admin can create books
    def create(self, request):
        if not request.user.is_superuser:
            return Response({"message": "only admin can create books"}, status=status.HTTP_403_FORBIDDEN)
        serializer = serializers.BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # onle admin can update books
    def update(self, request, pk, partial=False):
        if not request.user.is_superuser:
            return Response({"message": "only admin can update books"}, status=status.HTTP_403_FORBIDDEN)
        book = Book.objects.filter(id=pk)
        if not book:
            return Response({"message": "book with that id not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.BookSerializer(
            book[0], data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return Response({"message": "only admin can update books"}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)


class AuthorView(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = serializers.AuthorSerializer
    filter_backends = [SearchFilter]
    search_fields = ['id', 'name', 'location']

    # no authentication required for browsing list of authors and their published books
    def list(self, request, *args, **kwargs):
        books = Author.objects.filter(is_publised=True)
        serializer = serializers.AuthorSerializer(
            self.filter_queryset(books), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # only admin can create authors
    def create(self, request):
        if not request.user.is_superuser:
            return Response({"message": "only admin can create authors"}, status=status.HTTP_403_FORBIDDEN)
        serializer = serializers.AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # onle admin can update author
    def update(self, request, pk, partial=False):
        if not request.user.is_superuser:
            return Response({"message": "only admin can update authors"}, status=status.HTTP_403_FORBIDDEN)
        author = Author.objects.filter(id=pk)
        if not author:
            return Response({"message": "author with that id not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.BookSerializer(
            author[0], data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # only admin can delete a author
    def destroy(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return Response({"message": "only admin can delete author"}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
