
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("index", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newpost", views.newpost, name="newpost"),
    path('getposts', views.getposts, name='getposts'),
    path('likemanager', views.likeManager, name='likemanager'),
    path('following', views.following, name='following'),
    path('profile/<str:username>', views.profile, name='profile'),
    path('post/<int:id>', views.getOnePost, name='post')
]
