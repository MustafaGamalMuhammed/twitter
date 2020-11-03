from django.urls import path
from twitter import views


urlpatterns = [
    path('signup/', views.signup_view, name="signup"),
    path('signin/', views.SigninView.as_view(), name="signin"),
    path('logout/', views.logout_view, name="logout"),
    path('', views.home_view, name="home")
]