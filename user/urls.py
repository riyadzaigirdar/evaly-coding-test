from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('login', views.login, name="login"),
    path('signup', views.signup, name="signup"),
    path('me', views.me, name="me"),
    path('upload-profile-photo', views.upload_profile_photo, name="photo-upload")
]
