from django.db import models


class Hashtag(models.Model):
    name = models.CharField(max_length=125)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name