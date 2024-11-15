from .models import Post, Comment
from django.http import HttpResponse, HttpRequest
from users.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from users.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login as login_user, logout as logout_user
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from .models import Profile, Follow


def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect("#")
        else:
            if "email" in form.errors.keys():
                messages.error(request, form.errors["email"][0])
            elif "password1" in form.errors.keys():
                messages.error(request, form.errors["password1"][0])
            elif "password2" in form.errors.keys():
                messages.error(request, form.errors["password2"][0])
            print(form.errors.as_text())

    context = {"form": form}
    return render(request, "main/register.html", context)


def login(request):
    if request.method == "POST":
        email = request.POST.get("email").lower()
        password = request.POST.get("password")

        if not User.objects.filter(email=email).exists():
            messages.error(request, "Invalid Email")
            return HttpResponseRedirect("")

        user = authenticate(email=email, password=password)

        if user is None:
            messages.error(request, "Invalid Password")
            return HttpResponseRedirect("")
        else:
            login_user(request, user)
            return HttpResponseRedirect("/")

    return render(request, "main/login.html")


def logout(request):
    logout_user(request)
    return HttpResponseRedirect("/login/")


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "main/blank.html", {"user": request.user})


def profile(request: HttpRequest, username: str) -> HttpResponse:
    profile = get_object_or_404(Profile, username=username)
    following = request.user.profile.following.filter(following_id=profile.id).exists()
    context = {
        "profile": profile, 
        "following": following,
        }
    return render(
        request, "main/profile.html", context
    )


class PostDetailView(DetailView):
    model = Post
    template_name = "main/post_detail.html"
    context_object_name = "post"
    slug_field = "identifier"
    slug_url_kwarg = "identifier"


@login_required
def follow(request, username):
    next = request.GET.get("next", "/")
    following = get_object_or_404(Profile, username=username)
    follower = request.user.profile
    if not follower.following.filter(following_id=following.id).exists():
        Follow.objects.create(follower=follower, following=following)
    return redirect(next)

@login_required
def unfollow(request, username):
    next = request.GET.get("next", "/")
    following = get_object_or_404(Profile, username=username)
    follower = request.user.profile
    follower.following.filter(following_id=following.id).delete()
    return redirect(next)