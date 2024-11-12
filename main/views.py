from django.shortcuts import render, get_object_or_404
from users.models import User


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
