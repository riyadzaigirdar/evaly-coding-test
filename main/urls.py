
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include("user.urls")),
    path('browse/', include("books.urls")),
    path('loans/', include("loans.urls"))
] + static("media", document_root=settings.MEDIA_ROOT)
