from django.shortcuts import render


def index(request):
    return render(request, "main/blank.html")

def signup(request):
    return render(request, "main/signup.html")

def signin(request):
    return render(request, "main/signin.html")
