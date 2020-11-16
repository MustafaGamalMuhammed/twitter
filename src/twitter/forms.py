from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from twitter.models import Tweet


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class TweetForm(ModelForm):
    class Meta:
        model = Tweet
        fields = ['author', 'content']