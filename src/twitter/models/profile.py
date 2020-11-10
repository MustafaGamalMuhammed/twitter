from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    handler = models.CharField(max_length=15, unique=True)
    image = models.ImageField(upload_to="profile_pics", default="default.jpg")
    followers = models.ManyToManyField("Profile", related_name="f1", blank=True)
    following = models.ManyToManyField("Profile", related_name="f2", blank=True)

    def __str__(self):
        return self.user.username