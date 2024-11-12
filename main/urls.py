from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("post/<str:identifier>/", views.PostDetailView.as_view(), name="single-post"),
    path("<str:username>/", views.profile, name="profile"),
]
