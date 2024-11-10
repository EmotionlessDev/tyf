from django.http import HttpResponse, HttpRequest
from users.models import User
from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from users.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login as login_user, logout as logout_user


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
    return render(request, "main/blank.html")


def profile(request: HttpRequest, username: str) -> HttpResponse:
    cards = [
        {
            "title": "Название работы 1",
            "description": "Конспект по математическому анализу",
            "language": "LaTeX",
            "stars": 5,
            "author": "Иван Иванов",
            "date": "2024-10-01",
        },
        {
            "title": "Название работы 2",
            "description": "Теория вероятностей. Введение",
            "language": "Python",
            "stars": 8,
            "author": "Мария Петрова",
            "date": "2024-09-15",
        },
        {
            "title": "Название работы 3",
            "description": "Математическая логика",
            "language": "Java",
            "stars": 12,
            "author": "Алексей Смирнов",
            "date": "2024-08-20",
        },
        {
            "title": "Название работы 4",
            "description": "Алгоритмы и структуры данных",
            "language": "C++",
            "stars": 15,
            "author": "Светлана Кузнецова",
            "date": "2024-07-30",
        },
        {
            "title": "Название работы 5",
            "description": "Модели машинного обучения",
            "language": "R",
            "stars": 7,
            "author": "Дмитрий Федоров",
            "date": "2024-06-15",
        },
        {
            "title": "Название работы 6",
            "description": "Курс по сетям и базам данных",
            "language": "PHP",
            "stars": 5,
            "author": "Елена Волкова",
            "date": "2024-05-10",
        },
        {
            "title": "Название работы 7",
            "description": "Разработка веб-приложений",
            "language": "JavaScript",
            "stars": 10,
            "author": "Константин Чернов",
            "date": "2024-04-25",
        },
    ]
    user = get_object_or_404(User, username=username)
    return render(request, "main/profile.html", {"user": user, "cards": cards})


# def posts_list(request: HttpRequest) -> HttpResponse:
#
#     return render(request, "main/posts_list.html", {"cards": cards})
