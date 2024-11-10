from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpRequest
from users.models import User


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "main/blank.html")


def profile(request: HttpRequest, username: str) -> HttpResponse:
    user = get_object_or_404(User, username=username)
    return render(request, "main/profile.html", {"user": user})


def posts_list(request: HttpRequest) -> HttpResponse:
    return render(request, "main/posts_list.html")
