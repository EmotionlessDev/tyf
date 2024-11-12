from users.models import User
from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from users.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login as login_user, logout as logout_user
from django.apps import apps
from django.views.generic import DetailView


def index(request):
    return render(request, "main/blank.html")


def profile(request, username):
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
    user_posts = Post.objects.filter(author__username=username)
    user = get_object_or_404(User, username=username)
    return render(request, "main/profile.html", {"user": user, "posts": user_posts})


def single_post(request: HttpRequest) -> HttpResponse:
    return render(request, "main/single-post.html")


class PostDetailView(DetailView):
    model = Post
    template_name = 'main/single-post.html'
    context_object_name = 'post'
    slug_field = 'identifier'
    slug_url_kwarg = 'identifier'
