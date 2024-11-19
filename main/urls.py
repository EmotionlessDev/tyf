from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
<<<<<<< HEAD
    path("edit/", views.edit_profile, name="edit_profile"),
=======
    path("load_posts/", views.load_posts, name="load_posts"),
>>>>>>> 1dbe4c38d2d2defeea62523951ad3b9848a266d1
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
    path("posts/add/", views.post_new, name="post_add"),
    path("post/<str:identifier>/", views.PostDetailView.as_view(), name="post_detail"),
    path("<str:username>/", views.profile, name="profile"),
    path("follow/<str:username>/", views.follow, name="follow"),
    path("unfollow/<str:username>/", views.unfollow, name="unfollow"),
]
