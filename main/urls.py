from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("posts/", views.posts_list, name="posts_list"),
    path("<str:username>/", views.profile, name="profile"),
]
