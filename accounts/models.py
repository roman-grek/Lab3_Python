from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(blank=True, null=True)
    avatar = models.ImageField(upload_to="user_avatars/%Y/%m/%d", default="user_avatars/default.png")

    def __str__(self):
        return "Профиль пользователя %s" % self.user.username

