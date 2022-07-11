from django.contrib.auth import get_user_model
from django.db import models


class Profile(models.Model):
    image = models.ImageField(upload_to='profile/user/%y/%m/%d/', blank=True, null=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
