import bcrypt
from . import user_manager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=254)
    profile_photo = models.ImageField(
        blank=True, null=True, upload_to="user_photos")
    is_member = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = user_manager.UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def set_password(self, password):
        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt())
        self.password = hashed_password.decode("utf-8")
        return

    def check_password(self, password):
        check_correct = bcrypt.checkpw(password.encode(
            "utf-8"), self.password.encode("utf-8"))

        return check_correct

    def __str__(self):
        return self.email
