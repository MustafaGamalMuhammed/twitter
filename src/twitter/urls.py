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
    path('get_tweets/', views.get_home_tweets, name="get_home_tweets"),
    path('get_tweets/profile/', views.get_my_tweets, name="get_my_tweets"),
    path('get_tweets/profile/<int:id>/', views.get_profile_tweets, name="get_profile_tweets"),
    path('retweet/', views.retweet, name="retweet"),
    path('like/', views.like, name="like"),
]

home_urlpatterns = [
    path('', views.home_view, name="home")
]

profile_urlpatterns = [
    path('profile/', views.profile_view, name="profile"),
    path('profile/<int:id>/', views.profile_view, name="profile"),
    path('follow/', views.follow_view, name="follow"),
    path('search/<str:query>/', views.search, name="search"),
]

hashtag_urlpatterns = [
    path('get_most_used_hashtags/', views.get_most_used_hashtags),
]

urlpatterns = []
urlpatterns.extend(authentication_urlpatterns)
urlpatterns.extend(tweet_urlpatterns)
urlpatterns.extend(home_urlpatterns)
urlpatterns.extend(profile_urlpatterns)
urlpatterns.extend(hashtag_urlpatterns)