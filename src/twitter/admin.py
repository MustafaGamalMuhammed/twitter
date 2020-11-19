from django.contrib import admin
from twitter import models
# Register your models here.

admin.site.register([models.Profile, models.Tweet, models.Hashtag])