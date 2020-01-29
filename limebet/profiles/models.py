from django.contrib.auth.models import AbstractUser, UserManager


class ProfileManager(UserManager):
    pass


class Profile(AbstractUser):
    objects = ProfileManager()
