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
    path('get_tweets/', views.get_tweets, name="get_tweets"),
    path('retweet/', views.retweet, name="retweet"),
    path('like/', views.like, name="like"),
]

home_urlpatterns = [
    path('', views.home_view, name="home")
]

urlpatterns = authentication_urlpatterns + tweet_urlpatterns + home_urlpatterns