from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    handler = models.CharField(max_length=15, unique=True)
    followers = models.ManyToManyField("Profile", related_name="f1", blank=True)
    following = models.ManyToManyField("Profile", related_name="f2", blank=True)
    image = models.ImageField(upload_to="profile_pics", default="default.jpg")

    def follow(self, profile):
        if profile not in self.following.all():
            self.following.add(profile)
            profile.followers.add(self)

    def get_following_tweets(self):
        tweets = None

        for f in self.following.all():
            following_tweets = f.tweets.all()[:10]
            
            if tweets == None:
                tweets = following_tweets
            else:
                tweets = tweets.union(following_tweets)
            
        return tweets

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        
        im = Image.open(self.image)
        width, height = im.size
        
        if width > 200 or height > 200:
            im.thumbnail((200, 200), Image.ANTIALIAS)
            im.save(self.image.path)
