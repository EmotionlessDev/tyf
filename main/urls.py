from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.index, name="index"),
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
    path("<str:username>/", views.profile, name="profile"),
]
