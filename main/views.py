from django.shortcuts import render


def index(request):
    return render(request, 'main/blank.html')

def profile(request):
    return render(request, 'main/profile.html')
