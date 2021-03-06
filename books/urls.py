from books import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

app_name = 'books'

router = DefaultRouter()

router.register("books", views.BookView, basename="books")
router.register("author", views.AuthorView, basename="author")

urlpatterns = [
    path('', include(router.urls))
]
