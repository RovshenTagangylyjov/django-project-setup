from django.contrib.auth.models import AbstractUser

from .managers import UserManager
from .models import User


@admin.register(User)
class User(AbstractUser):
    objects = UserManager()
