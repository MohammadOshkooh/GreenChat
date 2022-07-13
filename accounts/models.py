from django.contrib.auth import get_user_model
from django.db import models


class Profile(models.Model):
    image = models.ImageField(upload_to='profile/user/%y/%m/%d/', blank=True, null=True,
                              default='http://127.0.0.1:8000/static/img/index.png')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='profile')

    def __str__(self):
        return self.user.username
