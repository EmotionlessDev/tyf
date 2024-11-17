from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("posts/add/", views.post_new, name="post_add"),
    path("post/<str:identifier>/", views.PostDetailView.as_view(), name="post_detail"),
    path("<str:username>/", views.profile, name="profile"),
    path("follow/<str:username>/", views.follow, name="follow"),
    path("unfollow/<str:username>/", views.unfollow, name="unfollow"),
]
