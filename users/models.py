from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shop_name = models.CharField(default='Not Specified', max_length=50)
    shop_category = models.CharField(default='Not Specified', max_length=50)

    def __str__(self):
        return f'{self.user.username} Profile'
