from django.db import models
from .profile import Profile


class Tweet(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="tweets")
    mentions = models.ManyToManyField(Profile, related_name="mentions")
    retweeters = models.ManyToManyField(Profile, related_name="retweets")
    likers = models.ManyToManyField(Profile, related_name="likes")
    content = models.CharField(max_length=400)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.created_at}: {self.author.handler}: {self.content[:50]}..."
