from django.urls import path
from twitter import views


authentication_urlpatterns = [
    path('signup/', views.signup_view, name="signup"),
    path('signin/', views.SigninView.as_view(), name="signin"),
    path('logout/', views.logout_view, name="logout"),
]

tweet_urlpatterns = [
    path('post_tweet/', views.post_tweet, name="post_tweet"),
    path('search_handlers/<str:query>/', views.search_handlers, name="search_handlers"),
    path('search_hashtags/<str:query>/', views.search_hashtags, name="search_hashtags"),
    path('get_tweets/', views.get_tweets, name="get_tweets"),
    path('get_tweets/<str:view>/', views.get_tweets, name="get_tweets"),
    path('retweet/', views.retweet, name="retweet"),
    path('like/', views.like, name="like"),
]

home_urlpatterns = [
    path('', views.home_view, name="home")
]

profile_urlpatterns = [
    path('profile/', views.profile_view, name="profile")
]

urlpatterns = []
urlpatterns.extend(authentication_urlpatterns)
urlpatterns.extend(tweet_urlpatterns)
urlpatterns.extend(home_urlpatterns)
urlpatterns.extend(profile_urlpatterns)