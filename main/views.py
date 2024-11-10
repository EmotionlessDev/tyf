from users.models import User
from django.shortcuts import render
from django.contrib import messages
from users.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login as login_user, logout as logout_user


def index(request):
    return render(request, "main/blank.html")


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

def profile(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'main/profile.html', {"user": user})
