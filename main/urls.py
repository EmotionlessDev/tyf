from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("edit/", views.edit_profile, name="edit_profile"),
    path("categories/", views.categories, name="categories"),
    path("categories/<slug:slug>/", views.category, name="category"),
    path("collections/", views.collections, name="collections"),
    path("collections/<slug:slug>/", views.collection, name="collection"),
    path("load_posts/", views.load_posts, name="load_posts"),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("login/reset_password/", views.resetPassword, name="reset_password"),
    path("logout/", views.logout, name="logout"),
    path(
        "verification/<str:uidb64>/<str:token>/",
        views.verification,
        name="verification",
    ),
    path(
        "login/set_password/<str:uidb64>/<str:token>/",
        views.setPassword,
        name="set_password",
    ),
    path("posts/add/", views.post_add, name="post_add"),
    path("post/<str:identifier>/", views.PostDetailView.as_view(), name="post_detail"),
    path("post/<str:identifier>/edit/", views.post_edit, name="post_edit"),
    # path("post/<str:identifier>/delete/", views.post_delete, name="post_delete"),
    path("post/<str:identifier>/bookmark/", views.post_bookmark, name="post_bookmark"),
    path("<str:username>/", views.profile, name="profile"),
    path("follow/<str:username>/", views.follow, name="follow"),
    path("unfollow/<str:username>/", views.unfollow, name="unfollow"),
]
