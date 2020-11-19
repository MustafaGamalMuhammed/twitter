from django.shortcuts import reverse
from django.db import models


class Hashtag(models.Model):
    name = models.CharField(max_length=125)
    usage_count = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('hashtag', args=(self.id,))

    def __str__(self):
        return self.name