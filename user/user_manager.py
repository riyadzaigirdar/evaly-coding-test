from django.contrib.auth.models import BaseUserManager
from django.utils import tree


class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, email, name, password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """Create and save a new superuser with given details"""

        admin_user = self.create_user(email, name, password)

        admin_user.is_superuser = True
        admin_user.is_staff = True
        admin_user.is_member = False
        admin_user.save(using=self._db)

        return admin_user
