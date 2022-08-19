from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    image = models.ImageField(upload_to='profile/user/%y/%m/%d/', blank=True, null=True,
                              default='http://127.0.0.1:8000/static/img/index.png')

